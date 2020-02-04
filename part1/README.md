# Assignment 1 Part 1

### Overview:
The `sorer` program takes in a sor_file to parse and create a columnar representation of data. First all the data (or the length/offset specified) is read into a 2D list where each entry represents a row of data. We use regular expressions to tokenize each entry in a row. It then determines the schema from the first 500 lines of the file or of the offset and length passed in. To find the schema we traverse each column and take the highest precedence type (String, float, integer, bool) in that column. We then create a columnar representation of the rows, filling in any missing fields with empty `<>`. Any malformed rows will be discarded.

### USAGE:

sorer [-h] -f SOR_FILE [-from FROM_INDEX] [-len LEN]
             [-print_col_type col_idx]
             [-print_col_idx col_idx, col_offset col_idx, col_offset]
             [-is_missing_idx col_idx, col_offset col_idx, col_offset]

required arguments:
  -f SOR_FILE           path to SoR file to be read

optional arguments:
  -h, --help            show this help message and exit
  -f SOR_FILE           path to SoR file to be read
  -from FROM_INDEX      starting position in the file (in bytes), default is 0
  -len LEN              number of bytes to read, default is 500
  -print_col_type col_idx
                        print the type of a column: BOOL, INT, FLOAT, STRING
  -print_col_idx col_idx, col_offset col_idx, col_offset
                        print the value at the column offset
  -is_missing_idx col_idx, col_offset col_idx, col_offset
                        is there a missing in the specific column offset

** One of the following must be passed into the program **
    -print_col_type
    -print_col_idx 
    -is_missing_idx 

### BEHAVIOR:
- If LEN is shorter than the file length, the program will ignore the last line, as it could be malformed
- If FROM_LENGTH is not zero, the program will ignore the first line, as it could be malformed
- If the program finds an malformed elements, it will ignore the entire row
- The program will infer row schema from longest row
- If a row is missing values for a column, an empty value will replace it
- Program will terminate if arguments are incorrect
- Program will terminate if column indices or offsets are passed in and do not exist
- Program will terminate if SOR_FILE is empty or cannot be read
- Program will terminate if the FROM_INDEX is incorrect or returns zero valid rows
