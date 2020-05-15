from pathlib import Path
import pandas as pd

__all__ = ["get_exoarchive", "get_local_exoarchive"]

def get_local_exoarchive(fname=None):
    if fname is None:
        dirname = Path(__file__).parent / "data"
        files = [item for item in dirname.iterdir() if item.is_file()]
        if files:
            fname = files[0]
    df = pd.read_csv(fname, comment="#")
    return df


def get_exoarchive(table="exomultpars"):
    query = f"https://exoplanetarchive.ipac.caltech.edu/cgi-bin/nstedAPI/nph-nstedAPI?table={table}"
    df = pd.read_csv(query, comment="#")
    return df
