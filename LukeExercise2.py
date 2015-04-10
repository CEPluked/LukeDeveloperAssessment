from os import path
import pandas as pd
from scipy.stats import percentileofscore

# Use the following lines to test the script in iPython
#import os
#os.chdir("Documents/Code/DeveloperAssessment")
#curr_dir = os.getcwd()


def pct_rank(data, score):
    if pd.isnull(score):
        return None
    else:
        return percentileofscore(data, score, kind="mean")


def main():
    curr_dir = path.abspath(path.dirname(__file__))
    ex2_input_dir = path.join(curr_dir, "exercise2", "input")

    # Read in the data file
    mean = pd.read_csv(path.join(ex2_input_dir, "mean.csv"))
    pct = mean
    # couldn't figure out if there was a way to do this with apply
    # as I wasn't sure how you'd pass the specific score to
    # the percentile function along with the column inside the
    # apply function call
    for col in pct.columns:
        if col == "fdntext":
            continue
        for row in pct.index:
            score = mean.ix[row, col]
            pct.ix[row, col] = pct_rank(mean[col], score)

    # I'm still getting different values in pct.csv than the
    # example output. 'mean' is the right kind to be using, right?

    pct = pct.set_index("fdntext")
    # Output a csv with these percentiles
    pct.to_csv("pct.csv")

if __name__ == "__main__":
    main()
