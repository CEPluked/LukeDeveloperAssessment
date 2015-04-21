from os import path
import pandas as pd
from scipy.stats import percentileofscore


def pct_rank(data, score):
    if pd.isnull(score):
        return None
    else:
        return percentileofscore(data, score, kind="mean")


def main():
    curr_dir = path.abspath(path.dirname(__file__))
    ex2_input_dir = path.join(curr_dir, "exercise2", "input")

    # Read in the data file
    mean = pd.read_csv(path.join(ex2_input_dir, "mean.csv"),
                       index_col="fdntext")
    pct = mean.copy()
    # couldn't figure out if there was a way to do this with apply
    # as I wasn't sure how you'd pass the specific score to
    # the percentile function along with the column inside the
    # apply function call
    for col in pct.columns:
        pct[col] = pct[col].apply(lambda x: pct_rank(pct[col], x))

    # Output a csv with these percentiles
    pct.to_csv("pct.csv")

if __name__ == "__main__":
    main()
