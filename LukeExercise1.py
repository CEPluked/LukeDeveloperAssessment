from os import path
import pandas as pd
from numpy import nan

# Use the following lines to test the script in iPython
#import os
#os.chdir("Documents/Code/DeveloperAssessment")
#curr_dir = os.getcwd()


def replace_dkna(df, exc_list=[77, 88]):
    """Takes in a dataframe and replaces the values given in
    exc_list with NAs. By default exc_list contains 'don't know'
    responses (coded as 77 and 88).
    """
    meaningless_placeholder = -1.0
    df = df.replace(exc_list, meaningless_placeholder)
    df = df.replace(meaningless_placeholder, nan)
    return df


def main():
    curr_dir = path.abspath(path.dirname(__file__))
    ex1_input_dir = path.join(curr_dir, "exercise1", "input")

    # Read in the data file
    xl = pd.read_csv(path.join(ex1_input_dir, "xl.csv"))

    xl = replace_dkna(xl)

    # Compute the mean response on each question for each client
    question_names = ["fldimp", "undrfld", "advknow", "pubpol",
                      "comimp", "undrwr", "undrsoc", "orgimp",
                      "impsust"]
    xl_questions = xl[["fdntext"] + question_names]
    xl_q_means = xl_questions.groupby("fdntext").mean()

    # Output the file of means
    xl_q_means.to_csv("mean.csv")

    # Create a table of summary stats for each question
    xl_summary = xl_q_means.describe()
    # Output a csv with these summary stats
    xl_summary.to_csv("stats.csv")

if __name__ == "__main__":
    main()
