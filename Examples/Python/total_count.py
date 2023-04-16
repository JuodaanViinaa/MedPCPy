from medpcpy import *

file = "total_count.xlsx"
temp_directory = "../Raw/"
perm_directory = "../Permanent/"
conv_directory = "../Converted/"
subjects = ["S28"]
lick_cols = {"S28": 2}
sheets = ["Licks"]

analysis_list = [
    # Lick responses
    {"total_count": {"response": 100,
                     "column": 2,
                     "header": "LickResps",
                     "sheet": "Licks",
                     "summary_distribution": lick_cols,
                     "offset": 0,
                     "write_rows": False,  # Optional
                     }},
    # Feeder entries
    {"total_count": {"response": 200,
                     "column": 4,
                     "header": "FeederEntries",
                     "sheet": "Licks",
                     "summary_distribution": lick_cols,
                     "offset": 1,
                     "write_rows": False,  # Optional
                     }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_TOTAL_COUNT_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="L", markColumn="M", relocate=False, colDivision=7)
# analyzer.convert()
analyzer.complete_analysis()
