"""I/O capabilites."""
from typing import Optional
from pathlib import Path

import numpy as np
import pandas as pd
from pandas._typing import FilePathOrBuffer
from astroquery.utils.tap.core import TapPlus

from ._dtypes import DTYPES_CONFIRMED, DTYPES_PS

__all__ = ["get_exoarchive", "load_catalog"]

BASE_URL = "https://exoplanetarchive.ipac.caltech.edu"
OLD_API_TABLES = ("exoplanets", "compositepars", "exomultpars", "aliastable", "microlensing")

def _download_ps_table():
    exoarch = TapPlus(url="https://exoplanetarchive.ipac.caltech.edu/TAP")
    job = exoarch.launch_job_async("select * from ps")
    # TODO: fix dtype conversion
    df = job.get_results().to_pandas()
    setattr(df, "_is_ps_table", True)
    return df

def _download_old_api_table(table):
    dtype = None
    if table == "exoplanets":
        dtype = DTYPES_CONFIRMED
    fname = f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table={table}&select=*&formal=csv"
    df = pd.read_csv(fname, dtype=dtype)
    setattr(df, "_is_ps_table", False)
    return df

def _read_local_catalog(fname, **kwargs):
    aux_kwargs = kwargs.copy()
    aux_kwargs.pop("usecols")
    aux = pd.read_csv(fname, usecols=["pl_name"], **aux_kwargs)
    is_ps_table = np.unique(aux.pl_name) < len(aux.pl_name)
    if is_ps_table:
        kwargs.setdefault("dtype", DTYPES_PS)
        df = pd.read_csv(fname, **kwargs)
    else:
        try:
            #TODO: clever way to see if table is of confirmed planets?
            aux_kwargs = kwargs.copy()
            aux_kwargs.setdefault("dtype", DTYPES_CONFIRMED)
            df = pd.read_csv(fname, **aux_kwargs)
        except:
            # no dtype goodness, users are on their own, either they pass dtype info
            # as kwarg or get warnings and "bad" behaviour
            df = pd.read_csv(fname, **kwargs)
    setattr(df, "_is_ps_table", is_ps_table)
    return df

def _download_from_figshare():
    raise ValueError("_download_from_figshare() is not implemented yet")

def load_catalog(table: Optional[FilePathOrBuffer] = None, **kwargs):
    """Load a local or remote catalog as pandas DataFrame.

    Parameters
    ----------
    table : str, path object or file-like object, optional
    kwargs
        Passed to :func:`pandas:pandas.read_csv`


    Returns
    -------
    pandas.DataFrame
    """
    if table in ("ps", "planetary_systems"):
        return _download_ps_table()
    if table in OLD_API_TABLES:
        return _download_old_api_table(table)
    if table is None:
        return _download_from_figshare()
    return _read_local_catalog(table, **kwargs)

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
        #TODO: use astroquery
        if table == "ps":
            fname = f"{BASE_URL}/TAP/sync?query=select+*+from+ps&format=csv"
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
