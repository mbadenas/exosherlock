"""I/O capabilites."""
from typing import Optional
from pathlib import Path
import pandas as pd
from pandas._typing import FilePathOrBuffer

__all__ = ["get_exoarchive", "get_local_exoarchive"]


def get_local_exoarchive(
    fname: Optional[FilePathOrBuffer] = None, default_pars: bool = False
) -> pd.DataFrame:
    """Load a local csv file downloaded from the NASA Exoplanet Archive.

    Parameters
    ----------
    fname : str, optional
        Name of the file to import as dataframe. By default, the csv file provided
        by the package is loaded.
    default_pars : bool, optional
        If True, returns only the subset with ``default_flag == 1``.

    Returns
    -------
    pandas.DataFrame
    """
    if fname is None:
        dirname = Path(__file__).parent / "data"
        files = [item for item in dirname.iterdir() if item.is_file()]
        if files:
            fname = files[0]
    df = pd.read_csv(fname, comment="#")
    if default_pars:
        return df.query("default_flag == 1")
    return df


def get_exoarchive(
    table: str = "exoplanets", extra_query: Optional[str] = None
) -> pd.DataFrame:
    """Download a table from the NASA Exoplanet Archive as a pandas.DataFrame.

    Parameters
    ----------
    table : str, optional
        Table to read from the NASA Exoplanet Archive.
    extra_query : str, optional
        String specifying a query in the format specified by the NASA Exoplanet
        Archive API documentation. Should not start with ``&``.

    Returns
    -------
    pandas.DataFrame
    """
    query = f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table={table}"
    if extra_query:
        query = "&".join((query, extra_query))
    df = pd.read_csv(query, comment="#")
    return df
