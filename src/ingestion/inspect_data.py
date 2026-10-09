
from pathlib import Path
import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = PROJECT_ROOT / "data" / "raw"


def inspect_movies() -> pd.DataFrame:
    """Load movies data and validate its basic structure."""
    path = RAW_DIR / "movies.csv"
    movies = pd.read_csv(path)

    required_columns = {"movieId", "title", "genres"}
    missing_columns = required_columns - set(movies.columns)

    if missing_columns:
        raise ValueError(f"Kolom movies hilang: {missing_columns}")

    if movies["movieId"].isna().any():
        raise ValueError("movies.csv memiliki movieId kosong")

    if movies["movieId"].duplicated().any():
        raise ValueError("movies.csv memiliki movieId duplikat")

    print(f"Movies berhasil diperiksa: {len(movies):,} baris")
    return movies


def inspect_ratings() -> pd.DataFrame:
    """Load ratings data and validate its basic structure."""
    path = RAW_DIR / "ratings.csv"

    ratings = pd.read_csv(
        path,
        usecols=["userId", "movieId", "rating", "timestamp"]
    )

    if ratings[["userId", "movieId", "rating", "timestamp"]].isna().any().any():
        raise ValueError("ratings.csv memiliki nilai kosong")

    if not ratings["rating"].between(0.5, 5.0).all():
        raise ValueError("Ada rating di luar rentang 0.5-5.0")

    print(f"Ratings berhasil diperiksa: {len(ratings):,} baris")
    return ratings


def validate_ratings(
    movies: pd.DataFrame,
    ratings: pd.DataFrame
) -> None:
    """Validate relationships and uniqueness in ratings."""

    # Pastikan pasangan userId-movieId unik
    duplicate_pairs = ratings.duplicated(
        subset=["userId", "movieId"]
    ).sum()

    if duplicate_pairs > 0:
        raise ValueError(
            f"Ditemukan {duplicate_pairs:,} pasangan userId-movieId duplikat"
        )

    # Pastikan setiap movieId di ratings tersedia di movies
    movie_ids = set(movies["movieId"])
    unknown_movies = ~ratings["movieId"].isin(movie_ids)
    unknown_count = int(unknown_movies.sum())

    if unknown_count > 0:
        raise ValueError(
            f"Ditemukan {unknown_count:,} rating dengan movieId tidak dikenal"
        )

    print("Pasangan userId-movieId: valid")
    print("Referensi movieId: valid")


if __name__ == "__main__":
    movies = inspect_movies()
    ratings = inspect_ratings()

    validate_ratings(movies, ratings)

    print("Seluruh pemeriksaan selesai.")