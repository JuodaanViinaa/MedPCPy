from medpcpy import *

file = "get_cols.xlsx"
temp_directory = "../Raw/"
perm_directory = "../Permanent/"
conv_directory = "../Converted/"
subjects = ["SC"]
measure1_cols = {"SC": 2}
sheets = []

analysis_list = [
    # Response column
    {"get_cols": {
        "source": "K",
        "column": 1,
        "header": "Responses",
    }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_GET_COLS_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="O", markColumn="P", relocate=False)
# analyzer.convert()
analyzer.complete_analysis()
