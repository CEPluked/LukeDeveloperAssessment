from os import path
import pandas as pd
from json import dump
from collections import OrderedDict

# Use the following two lines to interactively test the script
# in iPython
#os.chdir("C:/Users/luked/Documents/Code/pyCEP/DeveloperAssessment")
#curr_dir = os.getcwd()

def ex3_joiner(filename):
    """Helper function that joins filenames with the input directory
    for this exercise."""
    curr_dir = path.abspath(path.dirname(__file__))
    ex3_input_dir = path.join(curr_dir, "exercise3", "input")
    return path.join(ex3_input_dir, filename)

# Read in the files we'll need
mean = pd.read_csv(ex3_joiner("mean.csv"), index_col=0)
stats = pd.read_csv(ex3_joiner("stats.csv"), index_col=0)
pct = pd.read_csv(ex3_joiner("pct.csv"), index_col=0)

# For this exercise we're only using this one foundation / round
# for the output data
client_name = "Tremont 14S"

def elements_maker(client_name):
    """Given the name of a client looks up their relevant data in
    the input files and returns the 'elements' key ready for 
    insertion into the JSON ouput file."""

    # Initialize the elements dict
    elements = OrderedDict()
    # Loop through each question to fill out the elements dict.
    questions = mean.columns
    for question in questions:
        # Subset each of our input tables to only include the
        # current question
        q_stats = stats[question]
        q_mean = mean[question]
        q_pct = pct[question]

        # Set up the list of "absoulutes" (percentile values)
        # across all the clients for this question 
        q_absolutes = q_stats.ix["min"] + q_stats.ix["25%"] +\
                      q_stats.ix["50%"] + q_stats.ix["75%"] +\
                      q_stats.ix["max"]
        # Set up the "current" dict with basic information on the
        # current client
        q_current = {
            "name": "2014",
            "value": q_mean.ix[client_name],
            "percentage": q_pct.ix[client_name]
        }
        # Put the above variables and some hardcoded values into
        # the elements dict
        elements[question] = {
            "type": "percentileChart",
            "absolutes": q_absolutes,
            "current": q_current,
            "cohorts": [],
            "past_results": [],
            "segmentations": []
        }
    return elements

# If we wanted to do this for every client we could loop through
# this function call for each client.
client_elements = elements_maker(client_name)

json_output = OrderedDict(
    {
    "version": "1.0",
    "reports": [
        OrderedDict(
            {
            "name": client_name,
            "title": client_name,
            "cohorts": [],
            "segmentations": [],
            "elements": client_elements
            }
            )
        ]
    }
)

out_file = open("output.json", "w")
dump(json_output, out_file, indent=4)
out_file.close()