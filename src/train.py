import json

# import matplotlib.pyplot as plt
# import gc, os, math
import h2o
# , precision_score, plot_precision_recall_curve, roc_auc_score
from h2o.estimators import H2OXGBoostEstimator
from sklearn.metrics import (accuracy_score, classification_report, f1_score,
                             recall_score)

from .config import Config
from .eda import get_data
from .prepare_train_valid import prepare_train_valid
from .preprocess_data import get_categorical_cols, preprocess_data


def train_model():
    df = get_data(Config.data_path)
    df = preprocess_data(df)
    cat_cols = get_categorical_cols(df)
    (train, valid, test, train_df, valid_df, test_df), x, y = prepare_train_valid(
        df, cat_cols
    )

    m = H2OXGBoostEstimator(
        ntrees=Config.ntrees,
        seed=Config.model_seed,
        # score every 10 trees to make early stopping reproducible
        score_tree_interval=Config.score_tree_interval,
        stopping_rounds=Config.stopping_rounds,
        stopping_metric=Config.stopping_metric,
        stopping_tolerance=Config.stopping_tolerance,
        fold_assignment=Config.fold_assignment,
        nfolds=Config.nfolds,
        categorical_encoding=Config.categorical_encoding,
        col_sample_rate=Config.col_sample_rate,
        col_sample_rate_per_tree=Config.col_sample_rate_per_tree,
        learn_rate=Config.learn_rate,
        max_depth=Config.max_depth,
        min_rows=Config.min_rows,
        min_split_improvement=Config.min_split_improvement,
        sample_rate=Config.sample_rate,
    )

    m.train(x=x, y=y, training_frame=train)

    y_pred_all = m.predict(valid)
    y_test = valid_df[y].values
    y_pred = y_pred_all["predict"].as_data_frame().values

    _results = {
        "valid_accuracy": accuracy_score(y_test, y_pred),
        "valid_f1": f1_score(y_test, y_pred),
        "valid_f1_macro": f1_score(y_test, y_pred, average="macro"),
        "valid_classification_report": classification_report(y_test, y_pred),
        "valid_recall_score": recall_score(y_test, y_pred),
    }

    with open(f"{Config.info_save_path}valid_results.json", "w") as fp:
        json.dump(_results, fp)


if __name__ == "__main__":
    h2o.init(max_mem_size=Config.h2o_mem_size)
    train_model()
    print("****predict done****")
