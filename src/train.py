import json

import h2o
from h2o.estimators import H2OXGBoostEstimator
from sklearn.metrics import (accuracy_score, classification_report, f1_score,
                             recall_score)

from .config import Config
from .eda import get_data
from .prepare_train_valid import (get_h2o_train_valid, get_train_valid,
                                  treat_categorical_cols)
from .preprocess_data import get_categorical_cols, preprocess_data


def train_model():
    """String everything together and train the model"""
    df = get_data(Config.data_path)
    df = preprocess_data(df)
    cat_cols = get_categorical_cols(df)
    full_train_df, train_df, valid_df, test_df = get_train_valid(df)
    train, valid, test = get_h2o_train_valid(
        (full_train_df, train_df, valid_df, test_df)
    )
    train, valid, test, x, y = treat_categorical_cols((train, valid, test), cat_cols)

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
    valid_df[y + "_predicted"] = y_pred
    valid_df["mispredict"] = (valid_df[y + "_predicted"] - valid_df[y]).abs()
    valid_df = valid_df.sort_values(by=["mispredict"], ascending=False)
    valid_df.head(Config.top_mispredict_rows).to_csv(
        f"{Config.info_save_path}mispredicts.csv", index=False
    )

    _results = {
        "valid_accuracy": accuracy_score(y_test, y_pred),
        "valid_f1": f1_score(y_test, y_pred),
        "valid_f1_macro": f1_score(y_test, y_pred, average="macro"),
        "valid_classification_report": classification_report(y_test, y_pred),
        "valid_recall_score": recall_score(y_test, y_pred),
    }

    with open(f"{Config.info_save_path}valid_results.json", "w") as fp:
        json.dump(_results, fp)

    with open(f"{Config.info_save_path}valid_classification_report.json", "w") as fp:
        json.dump(_results["valid_classification_report"], fp)

    exp = m.explain(valid, render=False)

    for i in exp.keys():
        for j in exp[i]["plots"].keys():
            try:
                if i in ["pdp", "ice"]:
                    exp[i]["plots"][j].savefig(f"{Config.info_save_path}{i}_{j}.png")
                else:
                    exp[i]["plots"][j].savefig(f"{Config.info_save_path}{i}.png")
            except AttributeError:
                print(f"Exception for {i} - {j}")


if __name__ == "__main__":
    h2o.init(max_mem_size=Config.h2o_mem_size)
    train_model()
    print("****predict done****")
