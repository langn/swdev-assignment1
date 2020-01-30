#!/usr/bin/env python3

import re
import enum
import os

SAMPLE_SIZE = 500
EMPTY_RE = r"\s*>"
BOOL_RE = r"(\s)*(0|1)(\s)*>"
INT_RE = r"(\s)*(-|\+)?\d*(\s)*>"
FLOAT_RE = r"(\s)*(-|\+)?\d*\.?\d*(\s)*>"
STRING_RE = r"(\s)*(?:(?!>)(\S))*(\s)*>"
STRING_RE_QUOTES = r"(\s)*\"(?:(?!>).)*\"(\s)*>"

class Types(enum.Enum):
    empty = "empty"
    boolean = "BOOL"
    integer = "INT"
    afloat = "FLOAT"
    string = "STRING"


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
            if i >= len(row):
                column.append("")
            elif row[i][0] != schema[i]:
                column.append(row[i][1])
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
        return Types.boolean, ""

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
                entry = find_tag(line, line_index + 1)
                if (entry):                
                    typeof, matched = entry
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
    try:
        with open(name, "rb") as file:        
            file.seek(offset)
            content = ""
            if (length):
                content = file.read(length)
            else:
                content = file.read()
            decoded = content.decode("utf-8")
            lines = decoded.split("\n")
            return lines
    except FileNotFoundError as e:
        print(e)
        exit(1)