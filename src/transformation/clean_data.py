
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"
PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"



def clean_movies() -> pd.DataFrame:
    path = RAW_DIR / "movies.csv"
    movies = pd.read_csv(path)

    movies["title"] = movies["title"].str.strip()
    movies["genres"] = movies["genres"].str.strip()

    movies["genres"] = movies["genres"].replace(
        "(no genres listed)", pd.NA
    )

    movies["genres"] = movies["genres"].str.split("|")
    movies = movies.explode("genres")

    movies["genres"] = movies["genres"].str.strip()

    return movies


def validate_movies(movies: pd.DataFrame) -> None:
    print("\n=== VALIDASI MOVIES CLEAN ===")
    print(f"Total baris       : {len(movies):,}")
    print(f"Total movie unik  : {movies['movieId'].nunique():,}")
    print(f"Genre kosong      : {movies['genres'].isna().sum():,}")
    print(f"Duplikat baris    : {movies.duplicated().sum():,}")

    print("\nContoh hasil:")
    print(movies.head(10).to_string(index=False))


def clean_ratings(chunk_size: int = 500_000) -> None:
    input_path = RAW_DIR / "ratings.csv"
    output_path = PROCESSED_DIR / "ratings_clean.csv"

    if output_path.exists():
        output_path.unlink()

    total_rows = 0

    for chunk in pd.read_csv(
        input_path,
        usecols=["userId", "movieId", "rating", "timestamp"],
        chunksize=chunk_size,
    ):
        # Konversi Unix timestamp ke datetime UTC
        chunk["timestamp"] = pd.to_datetime(
            chunk["timestamp"],
            unit="s",
            utc=True,
            errors="coerce",
        )

        # Validasi nilai penting
        if chunk[["userId", "movieId", "rating", "timestamp"]].isna().any().any():
            raise ValueError("Ada nilai kosong atau timestamp tidak valid.")

        if not chunk["rating"].between(0.5, 5.0).all():
            raise ValueError("Ada rating di luar rentang 0.5–5.0.")

        # Tulis bertahap ke file output
        chunk.to_csv(
            output_path,
            mode="a",
            header=(total_rows == 0),
            index=False,
        )

        total_rows += len(chunk)
        print(f"Rating berhasil diproses: {total_rows:,}")

    print(f"\nTotal rating bersih: {total_rows:,}")
    print(f"File disimpan di: {output_path}")

# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    movies_clean = clean_movies()
    validate_movies(movies_clean)
    clean_ratings()

    output_path = PROCESSED_DIR / "movies_clean.csv"
    movies_clean.to_csv(output_path, index=False)

    print(f"\nJumlah baris hasil cleaning: {len(movies_clean):,}")
    print(f"Jumlah movie unik: {movies_clean['movieId'].nunique():,}")
    print(f"File berhasil disimpan ke: {output_path}")
