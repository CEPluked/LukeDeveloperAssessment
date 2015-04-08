from os import path
import pandas as pd
from numpy import mean, nan

curr_dir = path.abspath(path.dirname(__file__))
# Use the following two lines to interactively test the script
# in iPython
#os.chdir("C:/Users/luked/Documents/Code/pyCEP/DeveloperAssessment")
#curr_dir = os.getcwd()

ex1_input_dir = path.join(curr_dir, "exercise1", "input")

# Read in the data file
xl = pd.read_csv(path.join(ex1_input_dir, "xl.csv"))

# Replace "77" and "88" entries with NaN
# Numpy (old version) doesn't support using NaN with ints
# so evidently we have to do this ridiculous intermediate step.
# The issue is nan is a float and numpy.putmask
# (called in pandas.replace) tries to convert it to int.
meaningless_placeholder = -1.0
xl = xl.replace([77, 88], meaningless_placeholder)
xl = xl.replace(meaningless_placeholder, nan)

# Compute the mean response on each question for each client
question_names = ["fldimp", "undrfld", "advknow", "pubpol",
                  "comimp", "undrwr", "undrsoc", "orgimp",
                  "impsust"]
xl_questions = xl[["fdntext"] + question_names]
xl_qs_by_fdn = xl_questions.groupby("fdntext")
xl_q_means = xl_qs_by_fdn.aggregate(mean)

# Output the file of means
xl_q_means.to_csv("mean.csv")

# Create a table of summary stats for each question
xl_summary = xl_q_means.describe()
# Output a csv with these summary stats
xl_summary.to_csv("stats.csv")