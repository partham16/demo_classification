from typing import List

import numpy as np
import pandas as pd

from .config import Config


def drop_cols(df: pd.DataFrame) -> pd.DataFrame:
    """Drop columns which are worthless because 99.8% of the rows are same"""
    print(
        f"Drop column if only < {int(len(df) * (1-Config.col_uniq_cutoff))} rows are different from most common"
    )
    for i in df.columns:
        _ratio = df.groupby(i)[Config.primary_key].count().max() / len(df)
        if _ratio > Config.col_uniq_cutoff:
            print(f"column = {i}, ratio= {_ratio:.5f}")
            df = df.drop(columns=[i])
    return df


def check_unique(df: pd.DataFrame) -> pd.DataFrame:
    """Check if all rows are unique,
    Also, change binary classes to 0/1"""
    for i in df.columns:
        print(f"col={i}, num_unique={df[i].nunique()}, df_shape={len(df)}")
        if (df[i].nunique() == len(df)) or (df[i].nunique() == 1):
            df = df.drop(columns=[i])
        elif (df[i].nunique() == 2) and (set(df[i].unique()) == {"No", "Yes"}):
            df.loc[df[i] == "No", i] = 0
            df.loc[df[i] == "Yes", i] = 1
            df[i] = df[i].astype("int8")
    return df


def check_na(df: pd.DataFrame) -> pd.DataFrame:
    """check all the columns with NA values"""
    isna_df = (
        df.dtypes.loc[df.isna().sum() > 0]
        .to_frame()
        .reset_index()
        .rename(columns={"index": "column", 0: "dtype"})
        .merge(
            df.isna()
            .sum()
            .loc[df.isna().sum() > 0]
            .to_frame()
            .reset_index()
            .rename(columns={"index": "column", 0: "#missing"})
        )
    )
    isna_df.to_csv(f"{Config.info_save_path}isna.csv", index=False)
    return isna_df


def fill_na(df: pd.DataFrame, isna_df: pd.DataFrame) -> pd.DataFrame:
    """Fill missing numerics with median, add `missing` for categories"""
    for i in isna_df.loc[isna_df["dtype"] == "float64", "column"].tolist():
        df[i + "_missing"] = 0
        df.loc[df[i].isna(), i + "_missing"] = 1
        df.loc[df[i].isna(), i] = df[i].median()

    for i in isna_df.loc[isna_df["dtype"] == "object", "column"].tolist():
        df.loc[df[i].isna(), i] = "missing"
    return df


def preprocess_data(df: pd.DataFrame) -> pd.DataFrame:
    """String all these together"""
    df = check_unique(drop_cols(df))
    isna_df = check_na(df)
    df = fill_na(df, isna_df)
    return df


def get_categorical_cols(df: pd.DataFrame) -> List[str]:
    """Define which columns should be categorical"""
    cat_cols = [i for i in df.columns if df[i].dtype == np.dtype("O")]
    return cat_cols
