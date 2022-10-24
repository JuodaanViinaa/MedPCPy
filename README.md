# MedPCPy

The purpose of this library is to provide an easy and accesible way to convert MedPC files to .xlsx (Excel, LibreOffice Calc) format; and then to extract and organize the relevant data (response frequencies, latencies, and distributions) without the need of much programming abilities. After proper setup the entirety of the analysis of one or more sessions of experiments and one or more subjects can be done with a single click. The library scans a temporary directory in search of data to analyze. It determines the subjects that are in the directory and the sessions associated with each of them, counts the responses, latencies, and/or response distributions declared by the user, and delivers both individual files and a summary file: the individual files contain complete and properly labeled lists of all variables of interest (one individual xlsx file is created per subject per session); the summary file contains central tendency measures (either mean or median) for each variable written on the sheets and columns which the user indicates.

By default, the declared variables are written on the summary file vertically. That is, each measure of each subject occupies a column, and each session is written on a different row dictated by the session number and a [spacing argument](#spacing) in the `Analyzer` object declaration. It is possible, however, to write measures horizontally (each measure of each subject will occupy a row, and each session will be written on a column). This is done per-measure with the [`"write_rows"`](#write-rows) argument.

Files are organized in three separate directories:
1. A temporary directory in which raw files are stored before analysis.
2. A permanent directory to which raw files are automatically moved after analysis.
3. A converted directory in which processed individual .xlsx files and the summary file are stored after analysis.

This library uses functions from both [Openpyxl](https://openpyxl.readthedocs.io/en/stable/index.html) and [Pandas](https://pandas.pydata.org/pandas-docs/stable/). As such, it is advisable to be familiarized with them in order to understand the inner workings of some of its functions. It is, however, not necessary to know either of them to use this library.

## Quick Start

A quick start script named `quick_start.py` is provided with all relevant variables already declared. The user needs only change the values of all variables to something relevant to their project. That is, it will be necessary to change the summary filename, directory paths, subject names, column/row dictionaries, sheet names, all measures of the analysis list, as well as the `suffix`, `markColumn`, and `timeColumn` arguments of the `Analyzer` object.

To get the actual values of the `markColumn` and `timeColumn` arguments (instead of the placeholder values provided) it is necessary to first run the script with the `analyzer.convert()` line _uncommented_. Then one ought to manually inspect one of the produced files and look for the columns in which the time and marks ([explained below](#marks)) are written. Those are the values needed for `markColumn` and `timeColumn`. After that, the user must _comment_ the `analyzer.convert()` line, and _uncomment_ the `analyzer.complete_analysis()` line and run again the script. If everything goes as planned, the full analysis should run with no further interaction. If the user is satisfied with the process, then they can delete the `relocate = False` argument of the analyzer object and run the script again. This will make the code move the already-processed files from the temporary directory to the permanent one.

## Introduction

Once the python script is properly set, an example workflow could be as follows:

1. Run experiments on a MedPC interface.
2. Transfer the raw MedPC files to a temporary directory which the script will read.
3. Run the python script. The script will automatically read the files, convert them, extract all declared measures, write them on individual files as well as on a summary file, and move the raw files to a permanent directory so that the temporary directory is empty once again.

No other interaction is needed as long as the files are properly located and named.
_____

### Requirements

1. Python must be installed on the machine which will be used. _Note:_ If the user is not familiar with Python, then it is advised to first check the [Python introduction](https://github.com/JuodaanViinaa/MedPCPy/blob/main/briefIntroToPython/introPython.pdf) contained in this repository.
2. All files to analyze must be named using the format `"[subject name][spacing character][session number]"` so that the library can properly read them. The spacing character can be composed of more than one character, e.g.: `"Rat1_pretraining_1"`, where `"_pretraining_"` is the spacing character. Its importance will be explained shortly.
3. Three directories must exist in the system in which the analysis will take place. Their names are not important, but their functions will be: (1) temporary storage of raw files, (2) permanent storage or raw files, and (3) storage of converted .xlsx files.
4. All files must be placed inside the temporary directory (explained below) before the analysis.

<a id="marks"></a>
On a special note, this library can function on either the assumption that the user has set their MedPC configuration so that all measures of interest are printed on known places in their specific array(s) (in which case only the [fetch](#fetch) function will be needed); or on the assumption that the user has declared an array in their MedPC configuration which contains both the time of occurrence of each event, and the numbers which represent the events themselves in the format "XXX.XXX", where the number before the decimal point represents the time, and the number after represents the signal associated with the event (e.g., "100.111" would represent an event whose associated signaling number is "111" and which occurred at time "100"). In the latter case, these two numbers will be referred to as "time" and "marks", respectively.

_____

The first step is to install the library with the command

```python
pip install medpcpy
```

(or using the tools provided by an [Integrated Development Environment](https://www.redhat.com/en/topics/middleware/what-is-ide) such as [Pycharm](https://www.jetbrains.com/pycharm/)), and then import it to the working script with

```python
from medpcpy import *
```

to get access to all the necessary functions without the need to call `medpcpy.` on every use.

All of the work is performed by a single [object](https://www.geeksforgeeks.org/python-object/) of class `Analyzer` which contains [methods](https://www.w3schools.com/python/gloss_python_object_methods.asp) to convert MedPC files to .xlsx and then extract and summarize the relevant data. The `Analyzer` object requires several arguments to be initialized. These arguments are:

1. `fileName`, the name of the summary file. The file is created automatically if it does not exist yet. There is no need to manually create it.
2. `temporaryDirectory`, a [string](https://www.geeksforgeeks.org/python-strings/) indicating the directory in which raw MedPC files are stored before the analysis. All back slashes `"\"`, if any, must be replaced with forward slashes `"/"`, and the last character of the _string_ must be a forward slash. e.g.: `"C:/Users/Admin/Desktop/Path/To/Your/Directory/"`
3. `permanentDirectory`, the directory to which raw MedPC files will be moved after analysis. Must follow the same rules as the temporary directory.
4. `convertedDirectory`, the directory in which individual .xlsx files and the summary file will be stored after the analysis. Must follow the same rules as the temporary directory.
5. `subjectList`, a [list](https://www.w3schools.com/python/python_lists.asp) of _strings_ with the names of all subjects.
6. `suffix`, a _string_ which indicates the character or characters which separate the subject name from the session number in the raw MedPC filenames (e.g.: if raw files are named "subject1_1", "subject2_1", etc., then the value for the `suffix` argument should be `"_"`). This is how the library determines the sessions to analyze for each subject.
	* The filenames must follow the format `"[subject name][spacing character][session number]"` so that the library can properly read them. e.g.: `"Rat1_pretraining_1"`, where `"_pretraining_"` is the spacing character and, thus, the value for the `suffix` argument.
7. `sheets`, a list of _strings_ which represent the names of each individual sheet which will be created in the summary file. Much like the summary file, sheets are automatically created. This argument simply states the names each sheet should have.
8. `analysisList`, a list of [dictionaries](https://www.w3schools.com/python/python_dictionaries.asp) which declares the details of every relevant measure to extract. The template for this list can be printed with the `template()` function. A more in depth explanation is provided [further down](#analysis_list) this file.
9. `markColumn`, a _string_ stating the column in which the marks are written in the individual .xlsx files. This is only known _after_ converting at least one file, since the position of the column changes depending on the number of arrays used in MedPC for that particular experiment/condition.
10. `timeColumn`, a _string_ stating the column in which the time is written in the individual .xlsx files. This is only known _after_ converting at least one file, since the position of the column changes depending on the number of arrays used in MedPC for that particular experiment/condition.
11. `relocate`, a boolean (that is, it takes only values of `True` and `False`) which indicates whether or not the raw MedPC files should be moved from the temporary directory to the permanent one after the analysis. This is useful so as to avoid having to manually move the files back to the temporary directory while the code is being tested and debugged.
12. `colDivision`, an optional argument needed only in cases in which the MedPC files are divided in more than 6 columns (each column being represented by a set of characters divided by one or more white spaces). If more than 6 columns are present, then this argument must take as value the number of columns needed. E.g., `colDivision = 9`.
<a id="spacing"></a>
13. `spacing`, an optional argument which determines the amount of whitespace left in the summary file either at the top of the sheet (if working in columns) or at the left (if working in rows). By default, two rows or two columns are left blank to accommodate for the subject names and measure labels. If more (or less) space is needed, the needed amount of empty rows or columns must be stated as the value for this argument. E.g., `spacing = 5`.

The `timeColumn` and `markColumn` arguments are not needed to initialize the `Analyzer` object. The values for these arguments are obtained after first initializing the object without them and using the `.convert()` method to convert at least one file to .xlsx format:

```python
analyzer = Analyzer(fileName=summary_file, temporaryDirectory=temporary_directory, permanentDirectory=raw_directory,
                    convertedDirectory=converted_directory, subjectList=subjects, suffix="_", sheets=sheets,
                    analysisList=analysis_list, relocate=False)

analyzer.convert()
```


Then, this file must be manually inspected in order to get the letters of the columns which contain both the marks and the time registry. These columns are next to each other, are the same length, and are likely to be the longest columns in the entire file. 

![get_columns](https://user-images.githubusercontent.com/87039101/154622118-d96b7011-21d8-4414-87b0-9b2fa7c5df6f.png)

After the column letters are obtained, the `timeColumn` and `markColumn` arguments can be provided and the `Analyzer` object is now ready to extract data.


```python
analyzer = Analyzer(fileName=summary_file, temporaryDirectory=temporary_directory, permanentDirectory=raw_directory,
                    convertedDirectory=converted_directory, subjectList=subjects, suffix="_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="O", markColumn="P", relocate=False)
```

In the case in which the user has set their MedPC configuration so that all measures of interest are printed on known places in their specific array(s), declaring the `timeColumn` and `markColumn` arguments is not necessary since they are useful when working with a "TIME.EVENT" format.

Besides these arguments, some other variables containing dictionaries that relate subjects to columns need to be declared before the main analysis takes place. Their use is explained below.

## Analysis list <a id="analysis_list"></a>

The analysis list is a list of an arbitrary number of nested dictionaries. Each dictionary declares the function which will be used to extract data, and the relevant arguments to determine the data to be extracted and the way in which it will be written on both the individual and summary files. Each of the dictionaries must be separated with a comma from the others, and key:value pairs inside the dictionary must also be separated by commas. The recommended format to increase readability is provided in each function's description as well as on the `template()` function.

The syntax for the analysis list is provided per-function below.

The library contains several functions to extract and summarize data in common ways. Specifically, the library can:
* Grab a value from a specific cell in the individual .xlsx files given a row and column number ([`"fetch"`](#fetch)).
* Count all occurrences of a response per trial ([`"count_resp"`](#count-resp)).
* Count all occurrences of a response in a session ([`"total_count"`](#total-count)).
* Count the latencies from the beginning of each trial to the first occurrence of the response of interest ([`"lat_count"`](#lat-count)).
* Count the responses occurred per user-defined time-bin per trial ([`"resp_dist"`](#resp-dist)).
* Copy an entire array from the individual files and paste it as a column in the summary file ([`"get_cols"`](#get-cols)).
<a id="summary-distribution"></a>

Most of these functions need the declaration of a special dictionary which relates each subject with a specific column (if data is written vertically) or row (if data is written horizontally) in which its data will be written. That is, we may be interested in getting more than one measure from each subject (e.g., lever presses, nosepoke entries, latencies, etc.), and different measures may have different sub-divisions (e.g., there may be four levers, but two nosepokes). Thus, if we want to keep each type of response in its own separate sheet, we may need a format that is similar to this for the lever presses:

![image](https://user-images.githubusercontent.com/87039101/155408994-7b69ecd9-94dc-49ee-9af8-6b9d14cc4d11.png)

While for the nosepokes we may need a format that is similar to this:

![image](https://user-images.githubusercontent.com/87039101/155409189-dc7d0a95-0f9e-4028-b380-2d0634fd1934.png)

As it can be seen, distinct measures for a single subject require a different amount of columns in different sheets. For this reason in this particular example it will be necessary to declare at least two dictionaries: one which relates each subject with the space it occupies in the lever-response sheet, and another one which relates them with the space they occupy in the nosepoke-response sheet. These two dictionaries only need to declare the first column occupied by the subject, and substitute the column letter for its equivalent number (A = 1, B = 2, etc.). All other columns are dealt with later with the [`"offset"`](#offset) argument. Then, the dictionaries needed for this example would be:

```python
lever_cols = {"Rat1": 2, "Rat2": 7, "Rat3": 12,}
nosepoke_cols = {"Rat1": 2, "Rat2": 5, "Rat3": 8,}
```

Pay special attention to the correspondence between the number declared for each subject and the first column they occupy in the example.

### Functions
#### Fetch <a id="fetch"></a>
```python
analysis_list = [
{"fetch": {"cell_row": 10,
           "cell_column": 10,
           "sheet": "Sheet_1",
           "summary_distribution": column_dictionary,
           "offset": 0,  # Optional
           "write_rows": True,  # Optional. Default: False
           }},
]
```

This function allows the extraction of a single data point from the .xlsx individual files. It is useful to quickly extract measures such as the number of completed trials (if such data is available in one of the MedPC arrays). The arguments `"cell_row"` and `"cell_column"` dictate the position of the cell whose data will be extracted: if the data point is located, say, in cell "C16", then the required arguments will be `"cell_row": 16` and `"cell_column": 3`. 

![image](https://user-images.githubusercontent.com/87039101/156443205-6d34bb18-650d-4d2e-b47b-fbc3daa04899.png)

In order to get the location of the data point of interest the user may run the `.convert()` method and manually inspect one of the produced files.

The `"sheet"` and `"summary_distribution"` arguments determine the way in which the extracted data point will be written on the summary file. `"sheet"` indicates the name of the sheet in which the data point will be written. This name must correspond with one of the elements of the sheet list given as an argument to the `Analyzer` object. [`"summary_distribution"`](#summary-distribution) is the dictionary that relates each subject with the column or row in which their data will be written.

<a id="offset"></a>
The `offset` argument helps deal with situations in which similar measures for a single subject need to be written in adjacent columns in a single sheet (e.g., presses to different levers). In such cases it is not necessary to declare several dictionaries that relate each subject with a single column and then use those dictionaries as values for each `"summary_distribution"` argument. A more economic way to do it will be to use a single "base" dictionary for all similar measures, and then incrementally add units to the `"offset"` argument. Each unit in `"offset"` will move the measure in question one column to the right. E.g.:

```python
analysis_list = [
{"fetch": {"cell_row": 10,
           "cell_column": 10,
           "sheet": "Levers",
           "summary_distribution": lever_cols,
           "offset": 0  # Unnecessary
           }},
{"fetch": {"cell_row": 20,
           "cell_column": 20,
           "sheet": "Levers",
           "summary_distribution": lever_cols,
           "offset": 1  # <------
           }},
{"fetch": {"cell_row": 30,
           "cell_column": 30,
           "sheet": "Levers",
           "summary_distribution": lever_cols,
           "offset": 2  # <------
           }},
]
```

This will result in three columns. The first will be in the position declared by the `lever_cols` dictionary. The second and third will be one and two positions to the right.

If the `"offset"` argument is not declared, it will take a default value of `0`.

<a id="write-rows"></a>
Finally, the `"write_rows"` argument determines whether the measure will be written vertically (along a single column with one row per session), or horizontally (along a single row with one column per session). If its value is set to `True`, then the measure will be written horizontally. Otherwise it will take the default value of `False` and the measure will be written vertically. This argument is available for all functions except for `"resp_dist"` and `"get_cols"`.

#### Count_resp <a id="count-resp"></a>

```python
analysis_list = [
    {"count_resp": {"measures": 2, # Optional
                    "trial_start": 111, "trial_end": 222, "response": 333,
                    "trial_start2": 444, "trial_end2": 555, "response2": 666, # Optional
                    "column": 1,
                    "header": "Generic_title",
                    "sheet": "Sheet_2",
                    "summary_distribution": column_dictionary2,
                    "subtract": True, # Optional
                    "statistic": "mean",  # Optional. Alternative: "median"
                    "offset": 0,  # Optional
                    "write_rows": True,  # Optional. Default: False
                    }},
]
```

This function counts the amount of responses of interest that occurred between the start and the end of each trial in a session. It writes a list with all the responses per trial in the individual .xlsx file, and a measure of central tendency (either mean or median) in the summary file.

The arguments `"trial_start"`, `"trial_end"`, and `"response"` are the marks for the start of the trial, end of the trial, and response of interest, respectively.

The `"subtract"` argument is optional, and deals with the special case in which the response of interest is also the response that signals the start of the trial, and one desires not to count that first "starting" response as a part of the per-trial count. In such a situation, counting that additional response would overestimate the total responses per trial. To accommodate for that situation, adding the optional argument `"subtract": True` will subtract one unit from all non-zero response counts, which will result in an accurate measure. If one does not desire to subtract any units, then simply not declaring the argument will make it take a default value of `False`, and the subtraction will not be carried out.

The `"column"`and `"header"`arguments determine the way in which the complete list of responses per trial will be written on the individual .xlsx file. `"column"` indicates the column in which the list will be written (being that 1 = A, 2 = B, 3 = C, etc.). The `"header"`argument determines the title which the column will have in its first cell. In order to not overwrite any data, each declared dictionary from the analysis list must have a different value for `"column"`, and it is recommended to use an incremental order.

The `"sheet"`, `"summary_distribution"`, `"offset"`, and `"write_rows"` arguments work the same as in the `Fetch` function.

This function, alongside `"lat_count"`, `"total_count"`, and `"resp_dist"`, offers the possibility of making multiple or "aggregated" counts: on certain occasions it is advantageous to aggregate in a single measure responses or latencies from two or more sources. As an example one may think of a situation in which there are responses to a single lever in two different types of trials, and those responses have two different marks to identify them. One may wish to aggregate the responses or latencies from both types of trials so that they are represented by a single measure of central tendency. In such cases the library offers two ways to aggregate data.

First, the user can declare more than one mark as the trial start, trial end, and/or response, in the form of a list. That is, if instead of writing `111` as the `"trial_start"` mark, `333` as the `"trial_end"` mark, and `555` as the `"response"` mark, the user writes `[111, 222]` for `"trial_start"`, `[333, 444]` for `"trial_end"`, and `[555, 667]` for `"response"`, then the program will count all of the occurrences of either `555` or `667` that happen after either `111` or `222`, and before either `333` or `444` as part of a single measure. E.g.:

```python
analysis_list = [
    {"count_resp": {"trial_start": [111, 222], "trial_end": [333, 444], "response": [555, 667],
    ...
```

Note that it is not necessary for all lists to have the same amount of elements. If, say, two different responses which occur in a single type of trial are to be counted, then it is enough that the value for the `"response"` argument is declared as a list with both response marks (`[555, 667]`, for example) while leaving both `"trial_start"` and `"trial_end"` as single marks.

However, a situation may arise in which there are marks for different events which must be aggregated but which run the risk of being confused. For example, trial start `111` could correspond exclusively with trial end `333`, but not `444`, and with response `555` but not response `667`. If, still, both counts have to be aggregated, then the library offers a solution via the `"measures"` argument: `"measures"` will indicate how many different sources must be aggregated into the same measure of central tendency. For each additional source the necessary marks must be declared following the logical numbering. For example, for three sources aggregated into a single measure the arguments would be:

```python
analysis_list = [
    {"count_resp": {"measures": 3,
                    "trial_start": 123, "trial_end": 124, "response": 125,
                    "trial_start2": 223, "trial_end2": 224, "response2": 225, 
                    "trial_start3": 323, "trial_end3": 324, "response3": 325, 
                    ...
```
Attention must be paid to the "2" and "3" digits following the argument names, noting that the numbering is consecutive and that for the first source the redundant number "1" must not be written. This allows an unlimited amount of sources to be incorporated into a single measure. This second way, however, is not available for the `"resp_dist"` function.

In this way the different responses will be counted individually, and only at the end will they be aggregated, all without running the risk of being confused. However, the user must be aware that, if for any of the declared measures no responses are found, then a zero (`0`) will be written in its place in the list of total responses per trial. This could slightly throw off measures of central tendency, especially if few responses are recorded.

Be mindful of the difference between both ways of aggregating data and choose the one that better suits your needs. If doubts arise, try counting both individually and using either of these aggregate ways, seeing the complete lists on the individual files, and then deciding which, if any, is more convenient. In most cases their results will be identical.

<!-- This function, alongside `lat_count` and `total_count`, offers the possibility of making multiple or "aggregated" counts via the `"measures"` argument: on certain occasions it is advantageous to aggregate in a single measure the responses or latencies from two or more sources. As an example one may think of a situation in which there are responses to a single lever in two different types of trials, and those responses have two different marks to identify them. One may wish to aggregate the responses or latencies from both types of trials so that they are represented by a single measure of central tendency. In such cases the `"measures"` argument permits the incorporation of several information sources in a single measure. `"measures"` will indicate how many different sources must be aggregated into the same measure. For each additional source the necessary marks must be declared following the logical numbering. For example, for three sources aggregated into a single measure the arguments would be: -->
<!-- ```python -->
<!-- analysis_list = [ -->
<!--     {"count_resp": {"measures": 3, -->
<!--                     "trial_start": 123, "trial_end": 124, "response": 125, -->
<!--                     "trial_start2": 223, "trial_end2": 224, "response2": 225, --> 
<!--                     "trial_start3": 323, "trial_end3": 324, "response3": 325, --> 
<!--                     ... -->
<!-- ``` -->

<!-- Attention must be paid to the "2" and "3" digits following the argument names, noting that the numbering is consecutive and that for the first source the redundant number "1" must not be written. This allows an unlimited amount of sources to be incorporated into a single measure. This second way, however, is not available for the `resp_dist` function. -->

Finally, the `"statistic"` argument determines the measure of central tendency (mean or median) that will be written on the summary file. Its default value is `"mean"`, thus, if no value is declared, the written measure will be the mean.

#### Total_count <a id="total-count"></a>

```python
 analysis_list = [
    {"total_count": {"measures": 2, # Optional
                     "response": 111,
                     "response2": 222, # Optional
                     "column": 3,
                     "header": "Generic_title",
                     "sheet": "Sheet_4",
                     "summary_distribution": column_dictionary4,
                     "offset": 0,  # Optional
                     "write_rows": True,  # Optional. Default: False
                     }},
]
```

This function counts the amount of responses of interest occurred during the entire session without differentiating trial. It writes the resulting count in both the individual .xlsx file and the summary file.

Its arguments are identical to those of `"count_resp"` with two exceptions: it has got a single mark argument (`"response"`) since it does not need to know where trials begin and end; and it lacks the `"subtract"` argument since there are no extra responses to account for. 

Aggregate measures are allowed, just as in `"count_resp"`, with the same requirements of declaring either lists of marks, or the `"measures"` argument with incremental numbering for the `"response"` argument.

#### Lat_count <a id="lat-count"></a>

```python
analysis_list = [
    {"lat_count": {"measures": 2, # Optional
                   "trial_start": 111, "response": 222,
                   "trial_start2": 333, "response2": 444, # Opcional
                   "column": 2,
                   "header": "Generic_title",
                   "sheet": "Sheet_3",
                   "summary_distribution": column_dictionary3,
                   "statistic": "mean",  # Optional. Alternative: "median"
                   "offset": 0,  # Optional
                   "unit": 20,
                   "write_rows": True,  # Optional. Default: False
                   }},
]
```

This function computes the latencies per trial measured in seconds from the beginning of the trial to the first occurrence of the response of interest. The complete list of latencies per trial is written on the individual xlsx file, and the chosen measure of central tendency (mean or median) is written on the summary file.

The arguments are the same as those already described for the previous functions with one exception: this function has a `"unit"` argument which determines the temporal resolution that will be used to count the latencies. The value of the argument is the amount by which seconds are divided. This is dependent on the user's MedPC setup. For example, if the temporal resolution that the user's MedPC setup has is twentieths of a second, then the value for `"unit"` shall be `20`; else, if the temporal resolution is just seconds, the value should be `1`.

This function also allows aggregate measures with the same requirements as both `"count_resp"` and `"total_count"`.

#### Resp_dist <a id="resp-dist"></a>


```python
analysis_list = [
    {"resp_dist": {"trial_start": 111, "trial_end": 222, "response": 333,
                   "bin_size": 1,
                   "bin_amount": 15,
                   "label": "Generic_title",  # Optional
                   "statistic": "mean",  # Optional. Alternative: "median"
                   "unit": 20,
                   }},
]
```

This function can determine the temporal distribution of a response of interest along each trial of the session. The function will divide each trial in _bins_ whose size (in seconds) and amount is determined by the user with the `"bin_size"` and `"bin_amount"` arguments, and then will count the occurrences of the response or responses of interest during each bin. For each trial a separate list will be generated, and all lists will be written on a separate sheet of the individual xlsx file. A list with either the mean, median, or sum of responses per bin will be written on a column on a separate sheet of the summary file, one sheet per subject and one column per session. These sheets are created automatically and take the name of each subject; thus, it is not necessary to declare these sheets in the `sheets` argument of the `Analyzer` object.

If it is desired to aggregate more than one response on the same distribution, then the value for the `"trial_start"`, `"trial_end"`, and/or `"response"` arguments must be provided in the form of a list, e.g.,

```python
analysis_list = [
    {"resp_dist": {"trial_start": 111, "trial_end": 222, "response": [333, 444, 555],
    ...
```
Note that it is not necessary that the values for each argument have the same number of elements.

Since the distributions are written on separate columns per session and separate sheets per subject, the `"column"`, `"header"`, `"sheet"`, and `"summary_distribution"` arguments are not needed.

In those cases in which there is no Inter-Trial-Interval and there is no end-of-trial mark, and thus the end of a trial is only signaled by the beginning of the next, it will be enough to declare the same mark for both `"trial_start"` and `"trial_end"`.

The `"bin_size"` and `"bin_amount"` arguments determine the duration in seconds of each _bin_ and the amount of bins in which the trial will be divided, respectively. A 15 second trial with one-second _bins_ should have the values of `"bin_size": 1` and `"bin_amount": 15`.

The program creates one additional _bin_ beyond those declared by `"bin_amount"` in which all responses that occurred beyond the last declared _bin_ are aggregated. If no such responses exist, the final _bin_ will be empty.

If it is required to obtain more than one response distribution in a single experiment then the optional argument `"label"` shall be declared with a name that identifies each of the measures that are needed. The function will create a separate sheet for each measure of each subject, and give it a name composed of the subject name followed by the string used as value for the `"label"` argument. For example, if one desires to obtain response distributions for lever presses and nosepoke entries, the necessary dictionaries could take a format like this:

```python 
analysis_list = [
    {"resp_dist": {"trial_start": 111, "trial_end": 222, "response": 333,
        "bin_size": 1,
        "bin_amount": 15,
        "label": "Levers",
        "statistic": "mean",
        "unit": 20,
        }},

    {"resp_dist": {"trial_start": 444, "trial_end": 555, "response": 666,
        "bin_size": 1,
        "bin_amount": 15,
        "label": "Nosepokes",
        "statistic": "mean",
        "unit": 20,
        }},
]
```

The resulting summary file would have two sheets for each subject: one assigned to the lever response distributions, and another assigned to the nosepoke response distributions. If the subjects were `"Rat1"` and `"Rat2"`, the resulting sheets would have the names of `"Rat1_Levers"`, `"Rat1_Nosepokes"`, `"Rat2_Levers"`, and `"Rat2_Nosepokes"`. Furthermore, the individual xlsx files would also have separate sheets for each response distribution. These sheets are also automatically created and have as name the value of the `"label"` argument.

If the `"label"` argument is not declared then a single sheet per subject will be created in the summary file. If multiple response distributions are declared in the analysis list and the `"label"` argument is omitted in all of them, the distributions will overwrite one another and only the last declared distribution will prevail.

This function includes the `"statistic"` argument to determine whether a measure of central tendency (mean or median) or the sum of the values will be written, and the `"unit"` argument to specify the temporal resolution declared in the MedPC setup.

#### Get_cols <a id="get-cols"></a>


```python
analysis_list = [
    {"get_cols": {
        "source": "A",
        "column": 1,
        "header": "Generic_header",
        }},

]
```

This function can copy an entire array from the individual xlsx files and paste it on a specific column of the individual file and on a dedicated sheet on the summary file. Much like the ["resp_dist"](#resp-dist) function, this function automatically creates the necessary sheets for each subject on the summary file. Each subject will have one dedicated sheet named `[subject name]_[label]`, and each session will be written on a different column.

The `"source"` argument indicates the column from the individual xlsx file which will be copied. This is known after converting at least one file and manually determining the position of the column of interest. The `"column"` argument determines the position in which the column will be pasted in the sheet in which all full-lists are written in the individual file (1 = A, 2 = B, etc). Finally, the `"header"` argument determines both the title which the column will have on the individual xlsx file and the title of the dedicated sheet which will be created on the summary file.

___
___
## Example script and workflow

First the library is imported and all variables are declared:

```python
from medpcpy import *

file = "your_summary_filename.xlsx"
temp_directory = "/path/to/your/temporary/directory/"
perm_directory = "/path/to/your/permanent/raw/directory/"
conv_directory = "/path/to/your/converted/directory/"
subjects = ["Subject1", "Subject2", "Subject3"]
measure1_cols = {"Subject1": 2, "Subject2": 4, "Subject3": 6}
measure2_cols = {"Subject1": 2, "Subject2": 6, "Subject3": 10}
measure3_cols = {"Subject1": 2, "Subject2": 7, "Subject3": 12}
measure4_cols = {"Subject1": 2, "Subject2": 3, "Subject3": 4}
sheets = ["Measure1", "Measure2", "Measure3", "Measure4"]

analysis_list = [
    # Measure 1
    {"fetch": {"cell_row": 1,
               "cell_column": 1,
               "sheet": "Measure1",
               "summary_distribution": measure1_cols,
               "offset": 0,
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
                   }},
    # Response distribution
    {"resp_dist": {"trial_start": 111, "trial_end": 222, "response": 333,
                   "bin_size": 1,
                   "bin_amount": 15,
                   "label": "Generic_label",
                   "statistic": "median",  # Alternative value: "mean"
                   "unit": 20,  # Optional
                   }},

    # Entire column
    {"get_cols": {
        "source": "O",
        "column": 1,
        "header": "Generic_header",
    }},
]
```

Then the `Analyzer` object is created with all necessary arguments and assigned to a variable.

```python
analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_", sheets=sheets,
                    analysisList=analysis_list, relocate=False)
```

By this point, the `Analyzer` object is not yet ready to analyze data since it lacks the `timeColumn` and `markColumn` arguments. For this purpose the `.convert()` method is used:

```python
analyzer.convert()
```

This will create .xlsx files for each file in the temporary directory, and save them in the converted directory. Any one of these files must then be opened with a spreadsheet editor (such as Microsoft Excel or LibreOffice Calc) so as to manually inspect and determine the columns in which the time and marks are written. After doing so, the `Analyzer` object declaration can be edited to include the `timeColumn` and `markColumn` arguments:

```python
analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="O", markColumn="P", relocate=False)
```

Then the `.convert()` method can be commented out or deleted and the `.complete_analysis()` method can be used to extract and write all the declared measures:

```python
analyzer.complete_analysis()
```

If the user is satisfied with the result, they can then remove the `relocate` argument from the `Analyzer` object declaration and run again the code so that all raw files are moved from the temporary directory to the permanent one. Alternatively, this can be done manually.

An example of a complete script would be as follows:

```python
from medpcpy import *

file = "your_summary_filename.xlsx"
temp_directory = "/path/to/your/temporary/directory/"
perm_directory = "/path/to/your/permanent/raw/directory/"
conv_directory = "/path/to/your/converted/directory/"
subjects = ["Subject1", "Subject2", "Subject3"]
measure1_cols = {"Subject1": 2, "Subject2": 4, "Subject3": 6}
measure2_cols = {"Subject1": 2, "Subject2": 6, "Subject3": 10}
measure3_cols = {"Subject1": 2, "Subject2": 7, "Subject3": 12}
measure4_cols = {"Subject1": 2, "Subject2": 3, "Subject3": 4}
sheets = ["Measure1", "Measure2", "Measure3", "Measure4"]

analysis_list = [
    # Measure 1
    {"fetch": {"cell_row": 1,
               "cell_column": 1,
               "sheet": "Measure1",
               "summary_distribution": measure1_cols,
               "offset": 0,
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
                   }},
    # Response distribution
    {"resp_dist": {"trial_start": 111, "trial_end": 222, "response": 333,
                   "bin_size": 1,
                   "bin_amount": 15,
                   "label": "Generic_label",
                   "statistic": "median",  # Alternative value: "mean"
                   "unit": 20,  # Optional
                   }},
		   
    # Entire column
    {"get_cols": {
        "source": "O",
        "column": 1,
        "header": "Generic_header",
    }},
]

analyzer = Analyzer(fileName=file, temporaryDirectory=temp_directory, permanentDirectory=perm_directory,
                    convertedDirectory=conv_directory, subjectList=subjects, suffix="_", sheets=sheets,
                    analysisList=analysis_list, timeColumn="O", markColumn="P", relocate=False, spacing=5)
# analyzer.convert()
analyzer.complete_analysis()
```
