import argparse
import csv
import os
from pathlib import Path

import psycopg


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed"

MOVIES_FILE = DATA_DIR / "movies_clean.csv"
RATINGS_FILE = DATA_DIR / "ratings_clean.csv"

EXPECTED_MOVIES = 87_585
EXPECTED_RATINGS = 32_000_204

DB_CONFIG = {
    "host": os.getenv("PGHOST", "localhost"),
    "port": os.getenv("PGPORT", "5432"),
    "dbname": os.getenv("PGDATABASE", "cinestream"),
    "user": os.getenv("PGUSER", "postgres"),
    "password": os.environ.get("PGPASSWORD"),
}


def validate_files():
    """Pastikan file input tersedia sebelum terhubung ke database."""
    for file_path in (MOVIES_FILE, RATINGS_FILE):
        if not file_path.is_file():
            raise FileNotFoundError(
                f"File tidak ditemukan: {file_path}"
            )

    if not DB_CONFIG["password"]:
        raise ValueError(
            "Environment variable PGPASSWORD belum diatur."
        )


def main():
    validate_files()

    print("Menghubungkan ke PostgreSQL...")

    # Semua perubahan database berada dalam satu transaksi.
    # Jika terjadi error sebelum commit, perubahan akan di-rollback.
    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:

            print("Mengosongkan tabel target...")
            cur.execute("""
                TRUNCATE TABLE
                    ratings,
                    movie_genres,
                    movies,
                    staging_movies
            """)

            # ------------------------------------------------
            # LOAD STAGING MOVIES
            # ------------------------------------------------
            print("Memuat movies_clean.csv...")

            with MOVIES_FILE.open(
                "r", encoding="utf-8", newline=""
            ) as file:
                with cur.copy("""
                    COPY staging_movies (movieId, title, genres)
                    FROM STDIN WITH (FORMAT CSV, HEADER TRUE)
                """) as copy:
                    for line in file:
                        copy.write(line)

            # ------------------------------------------------
            # TRANSFORM MOVIES
            # ------------------------------------------------
            print("Membentuk tabel movies...")

            cur.execute("""
                INSERT INTO movies (movie_id, title)
                SELECT movieId, MIN(title)
                FROM staging_movies
                GROUP BY movieId
            """)

            print("Membentuk tabel movie_genres...")

            cur.execute("""
                INSERT INTO movie_genres (movie_id, genre)
                SELECT DISTINCT movieId, TRIM(genres)
                FROM staging_movies
                WHERE NULLIF(TRIM(genres), '') IS NOT NULL
            """)

            # ------------------------------------------------
            # LOAD RATINGS
            # ------------------------------------------------
            print("Memuat ratings_clean.csv...")

            with RATINGS_FILE.open(
                "r", encoding="utf-8", newline=""
            ) as file:
                reader = csv.reader(file)
                header = next(reader, None)

                expected_header = [
                    "userId", "movieId", "rating", "timestamp"
                ]

                if header != expected_header:
                    raise ValueError(
                        f"Header ratings tidak sesuai: {header}"
                    )

                with cur.copy("""
                    COPY ratings
                        (user_id, movie_id, rating, timestamp)
                    FROM STDIN WITH (FORMAT CSV)
                """) as copy:
                    writer = csv.writer(copy)

                    for row in reader:
                        writer.writerow(row)

            # ------------------------------------------------
            # VALIDATION
            # ------------------------------------------------
            print("Memvalidasi hasil load...")

            cur.execute("SELECT COUNT(*) FROM movies")
            movie_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM movie_genres")
            genre_count = cur.fetchone()[0]

            cur.execute("SELECT COUNT(*) FROM ratings")
            rating_count = cur.fetchone()[0]

            if movie_count != EXPECTED_MOVIES:
                raise ValueError(
                    f"Jumlah film salah: {movie_count:,}"
                )

            if rating_count != EXPECTED_RATINGS:
                raise ValueError(
                    f"Jumlah rating salah: {rating_count:,}"
                )

            cur.execute("""
                SELECT COUNT(*)
                FROM ratings r
                LEFT JOIN movies m ON m.movie_id = r.movie_id
                WHERE m.movie_id IS NULL
            """)
            orphan_ratings = cur.fetchone()[0]

            if orphan_ratings != 0:
                raise ValueError(
                    f"Ada {orphan_ratings:,} rating tanpa film."
                )

            # ------------------------------------------------
            # UPDATE STATISTICS
            # ------------------------------------------------
            cur.execute("ANALYZE ratings")
            cur.execute("ANALYZE movies")
            cur.execute("ANALYZE movie_genres")

            print("\n=== VALIDASI BERHASIL ===")
            print(f"Movies       : {movie_count:,}")
            print(f"Movie genres : {genre_count:,}")
            print(f"Ratings      : {rating_count:,}")
            print(f"Orphan ratings: {orphan_ratings:,}")

        # Keluar dari blok koneksi akan commit jika tidak ada error.
    print("\nTransaksi berhasil di-commit.")
    
def check_database():
    """Memeriksa koneksi dan jumlah data tanpa mengubah database."""
    validate_files()

    print("Memeriksa koneksi PostgreSQL...")

    with psycopg.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT
                    (SELECT COUNT(*) FROM movies),
                    (SELECT COUNT(*) FROM movie_genres),
                    (SELECT COUNT(*) FROM ratings),
                    (SELECT COUNT(*) FROM staging_movies)
            """)

            movies, genres, ratings, staging = cur.fetchone()

    print("\n=== CHECK BERHASIL ===")
    print(f"File movies tersedia : {MOVIES_FILE.is_file()}")
    print(f"File ratings tersedia: {RATINGS_FILE.is_file()}")
    print(f"Movies               : {movies:,}")
    print(f"Movie genres         : {genres:,}")
    print(f"Ratings              : {ratings:,}")
    print(f"Staging movies       : {staging:,}")
    print("Database tidak diubah.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Cinestream PostgreSQL loader"
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Periksa file dan database tanpa mengubah data",
    )
    args = parser.parse_args()

    if args.check:
        check_database()
    else:
        main()
