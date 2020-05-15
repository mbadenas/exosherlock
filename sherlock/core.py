import numpy as np

__all__ = ["get_min_value", "update_columns_with_min_err"]

def get_min_value(col_name, df):
    ref_colname = "{}_refname".format(col_name.split("_")[0])
    cols = ["pl_name"] + [tmp.format(col_name) for tmp in ("{}", "{}err1", "{}err2")] + [ref_colname]
    df_aux = df[cols].copy()
    err_col = "{}_err".format(col_name)
    df_aux = df_aux.assign(**{err_col: np.sqrt(df_aux[cols[2]]**2 + df_aux[cols[3]]**2)})
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

def update_columns_with_min_err(col_names, df_orig, df_fin):
    for col_name in col_names:
        df_fin = _update_column_with_min_err(col_name, df_orig, df_fin)
    return df_fin
