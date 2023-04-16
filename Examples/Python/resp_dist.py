from medpcpy import *

file = "resp_dist.xlsx"
temp_directory = "../Raw/"
perm_directory = "../Permanent/"
conv_directory = "../Converted/"
subjects = ["S1"]
measure1_cols = {"S1": 2}
sheets = []

analysis_list = [
    # Lick distribution
    {"resp_dist": {"trial_start": 400, "trial_end": 300, "response": 100,
                   "bin_size": 1,
                   "bin_amount": 15,
                   "label": "LicksDist",
                   "statistic": "mean",  # Alternative value: "median"
                   "unit": 10,  # Optional
                   }},
    # Entry distribution
    {"resp_dist": {"trial_start": 400, "trial_end": 300, "response": 200,
                   "bin_size": 1,
                   "bin_amount": 15,
                   "label": "EntryDist",
                   "statistic": "mean",  # Alternative value: "median"
                   "unit": 10,  # Optional
                   }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_RESP_DIST_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="L", markColumn="M", relocate=False, colDivision=7)
# analyzer.convert()
analyzer.complete_analysis()
