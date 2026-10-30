from pathlib import Path
import pandas as pd

def load_data(path: str | Path) -> pd.DataFrame:
    """Load the raw retail transactions CSV."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Dataset not found: {path}")
    return pd.read_csv(path)
