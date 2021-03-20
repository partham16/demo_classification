from typing import List, Tuple

import h2o
import pandas as pd
from sklearn.model_selection import train_test_split

from .config import Config


def get_train_valid(df: pd.DataFrame) -> Tuple[pd.DataFrame]:
    """Get train - valid - test"""
    full_train_df, test_df = train_test_split(
        df,
        test_size=Config.test_percent,
        random_state=Config.test_seed,
        stratify=df[Config.stratify_col].values,
    )
    train_df, valid_df = train_test_split(
        full_train_df,
        test_size=Config.valid_percent,
        random_state=Config.valid_seed,
        stratify=full_train_df[Config.stratify_col].values,
    )
    return full_train_df, train_df, valid_df, test_df


def get_h2o_train_valid(dfs: Tuple[pd.DataFrame]) -> Tuple[h2o.H2OFrame]:
    """Convert DataFrames to H2OFrames"""
    full_train_df, train_df, valid_df, test_df = dfs
    if not Config.use_full_train:
        train = h2o.H2OFrame(train_df)
    else:
        train = h2o.H2OFrame(full_train_df)
    valid = h2o.H2OFrame(valid_df)
    test = h2o.H2OFrame(test_df)
    return train, valid, test


def treat_categorical_cols(
    dfs: Tuple[h2o.H2OFrame], cat_cols: List[str]
) -> Tuple[h2o.H2OFrame, List[str], str]:
    """Set categorical columns as factor"""
    train, valid, test = dfs
    x = train.columns
    y = Config.target_col
    x.remove(y)

    train[y] = train[y].asfactor()

    for col in cat_cols:
        train[col] = train[col].asfactor()
        valid[col] = valid[col].asfactor()
        test[col] = test[col].asfactor()
    return train, valid, test, x, y
