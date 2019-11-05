# InsightDE
 My solution to Insight's Data Engineering challenge

# Insight Data Engineering coding challenge
This GitHub repository contains my solution to the [coding challenge](https://github.com/InsightDataScience/border-crossing-analysis) for the [Insight Data Engineering Fellows Program](https://www.insightdataengineering.com/).

Given a comma separated input file with 8 columns, e.g.,

```
iPort Name,State,Port Code,Border,Date,Measure,Value,Location
Derby Line,Vermont,209,US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,POINT (-72.09944 45.005)
Norton,Vermont,211,US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,POINT (-71.79528000000002 45.01)
Calexico,California,2503,US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,POINT (-115.49806000000001 32.67889)
Hidalgo,Texas,2305,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,156891,POINT (-98.26278 26.1)
Frontier,Washington,3020,US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,POINT (-117.78134000000001 48.910160000000005)
Presidio,Texas,2403,US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,15272,POINT (-104.37167 29.56056)
Eagle Pass,Texas,2303,US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,POINT (-100.49917 28.70889)
```
For this challenge, we want to you to calculate the total number of times vehicles, equipment, passengers and pedestrians cross the U.S.-Canadian and U.S.-Mexican borders each month. We also want to know the running monthly average of total number of crossings for that type of crossing i.e. `measure` and `border`. For example, the output will be the following for the above file.
```
Border,Date,Measure,Value,Average
US-Mexico Border,03/01/2019 12:00:00 AM,Pedestrians,346158,114487
US-Canada Border,03/01/2019 12:00:00 AM,Truck Containers Full,6483,0
US-Canada Border,03/01/2019 12:00:00 AM,Trains,19,0
US-Mexico Border,02/01/2019 12:00:00 AM,Pedestrians,172163,56810
US-Canada Border,02/01/2019 12:00:00 AM,Truck Containers Empty,1319,0
US-Mexico Border,01/01/2019 12:00:00 AM,Pedestrians,56810,0
```
## Design

* Solver class has been defined whose objects will contain all the functionality in Solver.py

* The data structure is a nested hashmap using python dictionaries

* Assuming O(1) for fetching values from the data structure and `measure` and `border` fields to be finite, the running time of the solution is O(N)

* The written rows have to sorted in the descending order in the field order: `Date` `Value` `Measure` `Border`

## Class Method Definition

### is_date:

This method checks if the `Date` value is of format `%m/%d/%Y %I:%M:%S %p`

Input: String

Output: True/False

### read:

This method checks for `Empty File`, `CSV file format` and `Valid Path of File`.
Date format is validated and if any field value is `missing` or `''` that row is skipped.
If there are no valid rows, then the method raises `Empty Dataset` exception.

Input: Input file path of csv file, Columns of interested

Output: Dataset as a list of lists

### process:

This method creates a nested dictionary with the following `Key` heirarchy:
* Border
* Measure
* Year
* Month

The value is `Value` if the key is created for the first time.
The value is `+=Value` if the key already exists.

Stored in `self.data_dict`

Input: Dataset as list of lists

Output: Nested dictionary

### get_all:

This method gets all the unique values for the following fields:
* Border
* Measure
* Year
* Month

Input: Nested dictionary

Output: lists

### solve:

This method calculates the `monthly average` and `cumulative` values uptil that month. 
Each month adds value from it's previous month.
Hence, only a reference to preceeding month is required to calculate these values.
The first month of the year uses the last month of previous year.
The `monthly average` and `cumulative` values are stored in a nested dictionary with same key heirarchy as `self.data_dict`.

Input: Nested dictionary

Output: Nested dictionaries

### flip_dicts:

This method flips the `self.data_dict` to the following order:

* Year 

* Month

* Value

* Measure

The value is `Border`

Input: Nested dictionary

Output: Nested dictionary

### write:

This method calls the method `flip_dicts`.
This method writes the rows to the file `report.csv` or whichever output file path given.

It traverses the flipped dictionary with the following fields in `Descending Order`:

* Year
 
* Month 

* Value 

* Measure 

* Border

and uses these values to get the `monthly average` from `self.mavg_dict` computed in `solve` method.

The output is written as a csv file.

Input: Nested dictionaries

Output: CSV File

## Instructions
To execute the script move to the main directory of the project and run the following in the terminal:

```
python ./src/main.py ./input/Border_Crossing_Entry_Data.csv ./output/report.csv
```

Alternatively, you can execute `./run.sh` script to run the code, move to the insight_testsuite and execute `./run_tests.sh` script to run all the test cases.