"""CSV upload, validation, and formula injection defense."""

import pandas as pd


_INJECTION_PREFIXES = ("=", "+", "-", "@")


def sanitize_cell(value: str) -> str:
    """Strip leading characters that could trigger formula injection."""
    if isinstance(value, str) and value and value[0] in _INJECTION_PREFIXES:
        return "'" + value
    return value


def load_csv(path: str) -> pd.DataFrame:
    """Read a CSV and apply basic validation.

    Parameters
    ----------
    path : str
        Path to the uploaded CSV file.

    Returns
    -------
    pd.DataFrame with sanitized string cells.
    """
    df = pd.read_csv(path)
    # Sanitize every object (string) column
    for col in df.select_dtypes(include="object").columns:
        df[col] = df[col].apply(sanitize_cell)
    return df
