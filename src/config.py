from typing import List


class Config:
    data_path: str = "./data/Data.csv"
    col_uniq_cutoff: float = 0.998
    primary_key: str = "Lead Number"
    info_save_path: str = "./AutoViz_Plots/"
    target_col: str = "Converted"
    h2o_mem_size: str = "12G"
    project_name: str = "v1_XGB"
    use_full_train: bool = False
    test_seed: int = 19
    test_percent: float = 0.09
    valid_seed: int = 11
    valid_percent: float = 0.1
    stratify_col: str = target_col
    model_seed: int = 42
    sort_metric: str = "aucpr"  # 'mean_per_class_error'
    cat_encoding: List[str] = ["target_encoding"]
    nfolds: int = 10
    class_sampling_factors: List[float] = [0.1, 1]
    ntrees: int = 10000
    score_tree_interval: int = 10
    stopping_rounds: int = 5
    stopping_metric: str = sort_metric
    stopping_tolerance: float = 1e-4
    fold_assignment: str = "Stratified"
    num_model: int = 25
    categorical_encoding: str = "SortByResponse"
    col_sample_rate: float = 0.68
    col_sample_rate_per_tree: float = 0.52
    learn_rate: float = 0.085
    max_depth: int = 5
    min_rows: int = 5
    min_split_improvement: float = 1e-5
    sample_rate: float = 0.89
