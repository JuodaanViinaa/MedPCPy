"""
This is a generic script provided to facilitate the use of the MedPCPy library.
All needed variables are already declared. The user needs only substitute their values for something relevant to their
project.
Particular attention should be paid to the "measure_cols" and the "analysis_list" variables . They are the most
important part of the script. More (or less) "measure_cols" variables than those already declared may be needed, and it
is advised that they are renamed to something more easily understandable for the project at hand.
To add measures relevant to the project copy and paste the format of one of the already-declared measures in the
"analysis_list" variable and substitute the values of the arguments.
"""
from medpcpy import *

file = "your_summary_filename.xlsx"
temp_directory = "/path/to/your/temporary/directory"
perm_directory = "/path/to/your/permanent/raw/directory"
conv_directory = "/path/to/your/converted/directory"
subjects = ["Subject1", "Subject2", "Subject3"]
measure1_cols = {"Subject1": 2, "Subject2": 4, "Subject3": 6}
measure2_cols = {"Subject1": 2, "Subject2": 6, "Subject3": 10}
measure3_cols = {"Subject1": 2, "Subject2": 7, "Subject3": 12}
measure4_cols = {"Subject1": 2, "Subject2": 3, "Subject3": 4}
sheets = ["Measure1", "Measure2", "Measure3", "Measure4"]

analysis_list = [
    # Measure 1
    {"fetch": {"cell_row": 10,
               "cell_column": 10,
               "sheet": "Sheet_1",
               "summary_distribution": measure1_cols,
               "offset": 0,
               "write_rows": False,  # Optional
               }},
    # Measure 2
    {"count_resp": {"measures": 2,  # Optional argument. Default value: 1
                    "trial_start": 111, "trial_end": 222, "response": 333,
                    "trial_start2": 444, "trial_end2": 555, "response2": 666,
                    # Optional marks. Depends on the value of "measures"
                    "column": 2,
                    "header": "Generic_title",
                    "sheet": "Measure2",
                    "summary_distribution": measure2_cols,
                    "subtract": True,  # Optional argument. Default value: False
                    "statistic": "mean",  # Alternative value: "median"
                    "offset": 0,
                    "write_rows": False,  # Optional
                    }},
    # Measure 3
    {"total_count": {"measures": 2,  # Optional argument. Default value: 1
                     "response": 111,
                     "response2": 222,  # Optional mark. Depends on the value of "measures"
                     "column": 3,
                     "header": "Generic_title",
                     "sheet": "Measure3",
                     "summary_distribution": measure3_cols,
                     "offset": 0,
                     "write_rows": False,  # Optional
                     }},
    # Measure 4
    {"lat_count": {"measures": 2,  # Optional argument. Default value: 1
                   "trial_start": 111, "response": 222,
                   "trial_start2": 333, "response2": 444,  # Optional marks. Depends on the value of "measures"
                   "column": 4,
                   "header": "Generic_title",
                   "sheet": "Measure4",
                   "summary_distribution": measure4_cols,
                   "statistic": "mean",  # Alternative value: "median"
                   "offset": 0,
                   "unit": 20,  # Optional
                   "write_rows": False,  # Optional
                   }},
    # Response distribution
    {"resp_dist": {"trial_start": 111, "trial_end": 222, "response": 333,
                   "bin_size": 1,
                   "bin_amount": 15,
                   "label": "Generic_label",
                   "statistic": "median",  # Alternative value: "mean"
                   "unit": 20,  # Optional
                   }},
    # Copy array
    {"get_cols": {
        "source": "A",
        "column": 1,
        "header": "Generic_header",
    }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="O", markColumn="P", relocate=False)
analyzer.convert()
# analyzer.complete_analysis()
