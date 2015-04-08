from os import path
import pandas as pd

curr_dir = path.abspath(path.dirname(__file__))
# Use the following two lines to interactively test the script
# in iPython
#os.chdir("C:/Users/luked/Documents/Code/pyCEP/DeveloperAssessment")
#curr_dir = os.getcwd()

ex2_input_dir = path.join(curr_dir, "exercise2", "input")

# Read in the data file
mean = pd.read_csv(path.join(ex2_input_dir, "mean.csv"))

# This works in the current version of pandas but not the old one
# we use for CREPE (because rank() didn't have the "pct" arg).
# pct = mean.drop("fdntext", axis=1).rank(pct=True)

# This way of calculating works in the old version of pandas
rank = mean.drop("fdntext", axis=1).rank(ascending=False)
fdn_count = len(mean["fdntext"])
pct = 1 - rank / fdn_count

pct.insert(0, "fdntext", mean["fdntext"])
pct = pct.set_index("fdntext")

# Output a csv with these percentiles
pct.to_csv("pct.csv")