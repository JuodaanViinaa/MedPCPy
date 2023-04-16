from medpcpy import *

file = "fetch.xlsx"
temp_directory = "../Raw/"
perm_directory = "../Permanent/"
conv_directory = "../Converted/"
subjects = ["R1"]
measure1_cols = {"R1": 2}
sheets = ["Reinforcers"]

analysis_list = [
    # Obtained reinforcers
    {"fetch": {"cell_row": 14,
               "cell_column": 2,
               "sheet": "Reinforcers",
               "summary_distribution": measure1_cols,
               "offset": 0,
               "write_rows": False,  # Optional
               }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_FETCH_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="K", markColumn="L", relocate=False)
# analyzer.convert()
analyzer.complete_analysis()
