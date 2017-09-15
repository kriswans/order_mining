# order_mining
app which is meant to read raw data as a tab delimited table and output based on desired columns and search variables.

features:
1. takes multiple files in the same format/layout, concatenates them, and read the column labels from the first row.
2. searches all columns and rows in concatenated table
3. outputs selected columns based on positive hits in search inside of all columns
4. outputs selected columns based on positive hits in recursive search in selected columns
5. outputs selected columns with duplicate lines eliminated and counted.

roadmap items:
1. exclude in search
2. 3 tier in put selection (Customer, subgroup/cell, time(by FY)
3. predefined search types
4. default values.
