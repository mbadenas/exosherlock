"""Core selection functions."""
from typing import Iterable, Optional, Union, Mapping
import numpy as np
from pandas import DataFrame

from .database import get_exoarchive

__all__ = ["update_columns_with_min_err", "get_from_exoarchive"]


def _get_min_value(col_name, df):
    ref_colname = "{}_refname".format(col_name.split("_")[0])
    cols = (
        ["pl_name"]
        + [tmp.format(col_name) for tmp in ("{}", "{}err1", "{}err2")]
        + [ref_colname]
    )
    df_aux = df[cols].copy()
    err_col = "{}_err".format(col_name)
    df_aux = df_aux.assign(**{err_col: (df_aux[cols[2]] + df_aux[cols[3]]) / 2})
    df_aux = df_aux.rename(columns={ref_colname: "{}_ref".format(col_name)})
    idxs = df_aux.groupby("pl_name")[err_col].idxmin().dropna()
    df_aux = df_aux.loc[idxs].drop(err_col, axis=1)
    return df_aux


def _update_column_with_min_err(col_name, df_orig, df_fin):
    df_aux = _get_min_value(col_name, df_orig).set_index("pl_name")
    *cols, ref_col = df_aux.columns
    df_fin.loc[df_aux.index, cols] = df_aux[cols]
    df_fin[ref_col] = ""
    df_fin.loc[df_aux.index, ref_col] = df_aux[ref_col]
    return df_fin


def update_columns_with_min_err(
    col_names: Union[str, Iterable[str]],
    df_orig: DataFrame,
    df_fin: DataFrame,
    pre_queries: Optional[Mapping[str, str]] = None,
    post_query: Optional[str] = None,
) -> DataFrame:
    """Update columns of dataframe to a unique value per planet.

    For every column in the ``col_names`` the selected value will be the one with
    minimum error.

    Parameters
    ----------
    col_names : str of list of str
    df_orig : pandas.Dataframe
    df_fin : pandas.Dataframe
    queries : dict of {str: str}, optional

    Returns
    -------
    pandas.Dataframe

    """
    if pre_queries is None:
        pre_queries = {}
    for col_name in col_names:
        df_aux = df_orig
        if col_name in pre_queries:
            df_fin[col_name] = np.nan
            df_aux = df_orig.query(pre_queries[col_name])
        df_fin = _update_column_with_min_err(col_name, df_aux, df_fin)
    if pre_queries:
        df_fin = df_fin.dropna(subset=list(pre_queries.keys()), how="any")
    if post_query:
        return df_fin.query(post_query)
    return df_fin


def get_from_exoarchive(
    col_names: Union[str, Iterable[str]],
    pre_queries: Optional[Mapping[str, str]] = None,
    post_query: Optional[str] = None,
) -> DataFrame:
    """Download dataframe NASA Exoplanet Archive and query it.

    Parameters
    ----------
    col_names : str of list of str
    pre_queries : dict of {str: str}, optional
    post_query : str, optional
    """
    exoarchive = get_exoarchive()
    df_final = (
        exoarchive.query("default_flag == 1")
        .drop("default_flag", axis=1)
        .set_index("pl_name")
        .copy(deep=True)
    )
    df_final = update_columns_with_min_err(
        col_names, exoarchive, df_final, pre_queries, post_query
    )
    return df_final
