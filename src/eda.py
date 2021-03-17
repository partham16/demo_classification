import pandas as pd
from autoviz.AutoViz_Class import AutoViz_Class

def get_data(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def run_eda(path: str):
    df = get_data(path)
    AV = AutoViz_Class()

    dftc = AV.AutoViz(
        filename='',
        sep='' ,
        depVar='Converted',
        dfte=df.fillna('-1'),
        header=0,
        verbose=2,
        lowess=False,
        chart_format='png',
        max_rows_analyzed=800000,
        max_cols_analyzed=35
    )

if __name__ == '__main__':
    run_eda("./data/Data.csv")
