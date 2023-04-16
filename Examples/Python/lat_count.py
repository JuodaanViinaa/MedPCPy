from medpcpy import *

file = "lat_count.xlsx"
temp_directory = "../Raw/"
perm_directory = "../Permanent/"
conv_directory = "../Converted/"
subjects = ["R1"]
latencies_cols = {"R1": 2}
sheets = ["Latencies"]

analysis_list = [
    # Latencies
    {"lat_count": {"trial_start": 100, "response": 200,
                   "column": 2,
                   "header": "LL-Latencies",
                   "sheet": "Latencies",
                   "summary_distribution": latencies_cols,
                   "statistic": "median",  # Alternative value: "mean"
                   "unit": 10,  # Optional
                   }},
    # Latencies
    {"lat_count": {"trial_start": 300, "response": 400,
                   "column": 4,
                   "header": "SS-Latencies",
                   "sheet": "Latencies",
                   "summary_distribution": latencies_cols,
                   "statistic": "median",  # Alternative value: "mean"
                   "offset": 1,
                   "unit": 10,  # Optional
                   }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_LAT_COUNT_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="K", markColumn="L", relocate=False)
# analyzer.convert()
analyzer.complete_analysis()
