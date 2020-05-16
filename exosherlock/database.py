"""I/O capabilites."""
from typing import Optional
from pathlib import Path
import pandas as pd
from pandas._typing import FilePathOrBuffer

from ._dtypes import DTYPES_CONFIRMED, DTYPES_PS

__all__ = ["get_exoarchive"]


def get_exoarchive(
    table="exoplanets",
    fname: Optional[FilePathOrBuffer] = None,
    default_pars: bool = False,
    local: bool=False,
    **kwargs,
) -> pd.DataFrame:
    """Read a table form the NASA Exoplanet Archive as a pandas DataFrame.

    Parameters
    ----------
    table : str, optional
        Which table from the exoplanet archive will be read. Used for custom dtypes
        which reduce memory usage and allow extra functionalities compared to
        automatic dtype parsing.
    fname : str, optional
        Name of the file to import as dataframe. By default, the csv file provided
        by the package is loaded. Ignored if ``local==False``.
    default_pars : bool, optional
        If True, returns only the subset with ``default_flag == 1``.
    local : bool, optional
        When true, the local csv file at ``fname`` is read.
    kwargs
        Passed to :func:`pandas:pandas.read_csv`

    Returns
    -------
    pandas.DataFrame
    """
    if local:
        if fname is None:
            dirname = Path(__file__).parent / "data"
            files = [item for item in dirname.iterdir() if item.is_file()]
            if files:
                fname = files[0]
    else:
        fname = f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table={table}"
    kwargs.setdefault("comment", "#")
    if table.lower() == "ps":
        kwargs.setdefault("dtype", DTYPES_PS)
    elif table.lower() in ("confirmed", "exoplanets"):
        kwargs.setdefault("dtype", DTYPES_CONFIRMED)
    df = pd.read_csv(fname, **kwargs)
    if default_pars:
        return df.query("default_flag == 1")
    return df
