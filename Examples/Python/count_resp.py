from medpcpy import *

file = "count_resp.xlsx"
temp_directory = "../Raw/"
perm_directory = "../Permanent/"
conv_directory = "../Converted/"
subjects = ["SC"]
responses_cols = {"SC": 2}
sheets = ["Responses"]

analysis_list = [
    # A-Responses
    {"count_resp": {"trial_start": 100, "trial_end": 500, "response": 110,
                    "column": 2,
                    "header": "A-Responses",
                    "sheet": "Responses",
                    "summary_distribution": responses_cols,
                    "subtract": False,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 0,
                    "write_rows": False,  # Optional
                    }},
    # B-Responses
    {"count_resp": {"trial_start": 100, "trial_end": 500, "response": 120,
                    "column": 4,
                    "header": "B-Responses",
                    "sheet": "Responses",
                    "summary_distribution": responses_cols,
                    "subtract": False,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 1,
                    "write_rows": False,  # Optional
                    }},
    # C-Responses
    {"count_resp": {"trial_start": 100, "trial_end": 500, "response": 130,
                    "column": 6,
                    "header": "C-Responses",
                    "sheet": "Responses",
                    "summary_distribution": responses_cols,
                    "subtract": False,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 2,
                    "write_rows": False,  # Optional
                    }},
    # D-Responses
    {"count_resp": {"trial_start": 100, "trial_end": 500, "response": 140,
                    "column": 8,
                    "header": "A-Responses",
                    "sheet": "Responses",
                    "summary_distribution": responses_cols,
                    "subtract": False,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 3,
                    "write_rows": False,  # Optional
                    }},
    # Total Responses
    {"count_resp": {"measures": 4,
                    "trial_start": 100, "trial_end": 500, "response": 110,
                    "trial_start2": 100, "trial_end2": 500, "response2": 120,
                    "trial_start3": 100, "trial_end3": 500, "response3": 130,
                    "trial_start4": 100, "trial_end4": 500, "response4": 140,
                    "column": 10,
                    "header": "Total-Responses",
                    "sheet": "Responses",
                    "summary_distribution": responses_cols,
                    "subtract": False,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 4,
                    "write_rows": False,  # Optional
                    }},
    # Total Responses
    {"count_resp": {"trial_start": 100, "trial_end": 500, "response": [110, 120, 130, 140],
                    "column": 10,
                    "header": "Total-Responses",
                    "sheet": "Responses",
                    "summary_distribution": responses_cols,
                    "subtract": False,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 4,
                    "write_rows": False,  # Optional
                    }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_COUNT_RESP_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="Q", markColumn="R", relocate=False)
# analyzer.convert()
analyzer.complete_analysis()
