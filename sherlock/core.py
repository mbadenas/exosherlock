import numpy as np
import pandas as pd

__all__ = ["get_min_value", "update_columns_with_min_err"]

def get_min_value(col_name, df):
    ref_colname = "{}_refname".format(col_name.split("_")[0])
    cols = ["pl_name"] + [tmp.format(col_name) for tmp in ("{}", "{}err1", "{}err2")] + [ref_colname]
    df_aux = df[cols].copy()
    err_col = "{}_err".format(col_name)
    df_aux = df_aux.assign(**{err_col: (df_aux[cols[2]] + df_aux[cols[3]]) / 2})
    df_aux = df_aux.rename(columns={ref_colname: "{}_ref".format(col_name)})
    idxs = df_aux.groupby("pl_name")[err_col].idxmin().dropna()
    df_aux = df_aux.loc[idxs].drop(err_col, axis=1)
    return df_aux

def _update_column_with_min_err(col_name, df_orig, df_fin):
    df_aux = get_min_value(col_name, df_orig).set_index("pl_name")
    *cols, ref_col = df_aux.columns
    df_fin.loc[df_aux.index, cols] = df_aux[cols]
    df_fin[ref_col] = ""
    df_fin.loc[df_aux.index, ref_col] = df_aux[ref_col]
    return df_fin

def update_columns_with_min_err(col_names, df_orig, df_fin, queries=None):
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
    if queries is None:
        queries = {}
    for col_name in col_names:
        df_aux = df_orig
        if col_name in queries:
            df_fin[col_name] = np.nan
            df_aux = df_orig.query(queries[col_name])
        df_fin = _update_column_with_min_err(col_name, df_aux, df_fin)
    if queries:
        return df_fin.dropna(subset=list(queries.keys()), how="any")
    return df_fin
