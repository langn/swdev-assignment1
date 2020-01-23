#! /usr/bin/python3

import argparse
import re
import enum
import os

SAMPLE_SIZE = 500
EMPTY_RE = r"\s*>"
BOOL_RE = r"\s*(0|1)\s*>"
INT_RE = r"\s*(-|\+)?\d*\s*>"
FLOAT_RE = r"\s*(-|\+)?\d*\.?\d*\s*>"
STRING_RE = r"\s*(?:(?!>)(\S))*\s*>"
STRING_RE_QUOTES = r"\s\"(?:(?!>)(.*))*\"\s"


def arg_parser():
    parser = argparse.ArgumentParser(description='data adaptor')
    parser.add_argument('-f', required=True,
                        help="path to SoR file to be read", dest='sor_file')
    parser.add_argument('-from', type=int, default=0,
                        help="starting position in the file (in bytes)", dest="from_index")
    parser.add_argument('-len', type=int, default=SAMPLE_SIZE,
                        help="number of bytes to read", dest="len")
    parser.add_argument('-print_col_type', type=int,
                        help="print the type of a column: BOOL, INT, FLOAT, STRING", metavar=("col_idx"))
    parser.add_argument("-print_col_idx", type=int, nargs=2,
                        help="print the value at the column offset", metavar=("col_idx, col_offset"))
    parser.add_argument('-is_missing_idx', type=int, nargs=2,
                        help="is there a missing in the specific column offset", metavar=("col_idx, col_offset"))
    args = parser.parse_args()

    if not (args.print_col_type or args.print_col_idx or args.is_missing_idx):
        parser.error(
            'No action requested, please use -print_col_type, -print_col_idx or is_missing_idx appropriately')

    return args


class Types(enum.Enum):
    empty = "empty"
    boolean = "boolean"
    integer = "integer"
    afloat = "float"
    string = "string"


def length_of_row(row):
    length = 0
    for entry in row:
        if entry[0] != Types.empty:
            length += 1

    return length


def construct_matrix(schema, rows):
    result = []
    for i in range(len(schema)):
        column = []
        for row in rows:
            if (i >= len(row) or row[i][0] != schema[i]):
                column.append("")
            else:
                column.append(row[i][1])

        result.append(column)

    return result


def find_schema(rows):
    sample = min(SAMPLE_SIZE, len(rows))
    longest = 0
    index_longest = 0
    for i in range(sample):
        current = rows[i]
        current_len = length_of_row(current)
        if (current_len > index_longest):
            longest = i
            index_longest = current_len

    schema = []
    for entry in rows[longest]:
        if (entry[0] != Types.empty):
            schema.append(entry[0])

    return schema


def remove_quotes(entry):
    if (len(entry) >= 2 and entry[0] == "\""):
        end = len(entry) - 1
        start = 1
        return entry[start:end]

    return entry


def find_tag(line, index):
    to_scan = line[index:]
    result = re.match(EMPTY_RE, to_scan)
    result_type = Types.empty
    # tag is not empty
    if (not result):
        result = re.match(BOOL_RE, to_scan)
        result_type = Types.boolean
        # tag is not BOOL
        if (not result):
            result = re.match(INT_RE, to_scan)
            result_type = Types.integer
            # tag is not INT
            if (not result):
                result = re.match(FLOAT_RE, to_scan)
                result_type = Types.afloat
                # tag is not FLOAT
                if (not result):
                    result = re.match(STRING_RE, to_scan)
                    result_type = Types.string
                    # tag is not a regular string
                    if (not result):
                        result = re.match(STRING_RE_QUOTES, to_scan)
                        # tag cannot be matched, return None
                        if (not result):
                            return result
    # tag is empty
    else:
        return result_type, ""

    i, j = result.span()
    start = index + i
    end = index + j - 1
    result = line[start:end]
    return result_type, result


def parse_lines(lines):
    rows = []

    for line in lines:
        line_index = 0
        entries = []
        while(line_index < len(line)):
            current = line[line_index]
            if (current == " "):
                line_index += 1
                continue
            elif (current == "<"):
                # find end of tag
                typeof, matched = find_tag(line, line_index + 1)
                if (matched):
                    result = remove_quotes(matched.strip())
                    entries.append((typeof, result))
                else:
                    entries = []
                    break

                line_index += len(matched) + 2
            else:
                entries = []
                break

        rows.append(entries)

    return rows

def print_col_type(schema, index):
    return schema[index].value

def is_missing_idx(matrix, column, offset):
    if (matrix[column][offset] == ""):
        return "1"
    else:
        return "0"

def print_col_idx(matrix, column, offset):
    return matrix[column][offset]

def open_file(name, length, offset):
    with open(name, "rb") as file:
        file.seek(offset)
        content = file.read(length)
        decoded = content.decode("utf-8")
        lines = decoded.split("\n")
        return lines

def incorrect_index():
    print("Incorrect indices")
    exit(1)

def main():
    args = arg_parser()

    lines = open_file(args.sor_file, args.len, args.from_index)

    if (len(lines) < 1):
        print("Empty file")
        exit(0)

    if (args.from_index != 0 and len(lines) > 0):
        lines.pop(0)

    if (args.len < os.path.getsize(args.sor_file) and len(lines) > 0):
        lines.pop()
    
    if (len(lines) < 1):
        print("Invalid file or offset")
        exit(0)

    collection = parse_lines(lines)
    schema = find_schema(collection)

    matrix = []
    if (args.print_col_idx or args.is_missing_idx):
        matrix = construct_matrix(schema, collection)

    print_type = args.print_col_type
    print_idx = args.print_col_idx
    print_missing = args.is_missing_idx

    print_format = (print_type and print_idx) or (print_type and print_missing) or (print_idx and print_missing)

    if(print_type >= len(schema) or print_type < 0):
        incorrect_index()
    
    if (print_idx):
        column, offset = print_idx
        if (column > len(schema) or column < -1 or offset >= len(matrix[column]) or offset < 0):
            incorrect_index()

    if(print_missing):
        column, offset = print_missing
        if (column > len(schema) or column < -1 or offset >= len(matrix[column]) or offset < 0):
            incorrect_index()
    
    if print_type:
        if print_format:
            print("Column type:")
        print(print_col_type(schema, args.print_col_type))
    
    if print_idx:
        if print_format:
            print("Column value at offset:")
        column, offset = args.print_col_idx
        print(print_col_idx(matrix, column, offset))

    if print_missing:
        if print_format:
            print("Is value missing at offset?")
        column, offset = args.is_missing_idx
        print(is_missing_idx(matrix, column, offset))

main()
