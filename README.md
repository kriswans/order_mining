# order_mining
Project started as a toll to mine data from historical order indormation, hence the name.

SNORTST.py is meant to read raw data as a tab delimited table and output based on desired columns and search variables.

features:
1. takes multiple files in the same format/layout, concatenates them, and reads the column labels from the first row.
2. searches all columns and rows in concatenated file/table based in include and exclude search list.
3. outputs selected columns based on positive hits in search inside of all columns
4. outputs selected columns based on positive hits in recursive search in selected columns
5. outputs selected columns with duplicate lines eliminated and counted.

roadmap items:

1. 3 tier in put selection (Customer, subgroup/cell, time(by FY)
2. predefined search types
3. persistent default values.
4. column consistency check for concatenated files
5. batch search input (i.e search a list of part numbers from input file)
6. range by date (i.e. using 'ship date' column to define range)
7. Web front end
8. NoSQL backend DB
