#! /usr/bin/python3

import argparse
import re

EMPTY_RE = r"\s*>"
BOOL_RE = r"\s*(0|1)\s*>"
INT_RE = r"\s*(-|\+)?\d*\s*>"
FLOAT_RE = r"\s*(-|\+)?\d*\.?\d*\s*>"
STRING_RE = r"\s*(?:(?!>)(\S)*)\s*>"
STRING_RE_QUOTES = r"\s\"(?:(?!>)(.*))*\"\s"

parser = argparse.ArgumentParser(description='data adaptor')
parser.add_argument('-f', required=True, help="path to SoR file to be read", dest='sor_file')
parser.add_argument('-from', type=int, default=0, help="starting position in the file (in bytes)", dest="from")
parser.add_argument('-len', type=int, default=500, help="number of bytes to read", dest="len")
parser.add_argument('-print_col_type', type=int, help="print the type of a column: BOOL, INT, FLOAT, STRING", metavar=("col_idx"))
parser.add_argument("-print_col_idx", type=int, nargs=2, help="print the value at the column offset", metavar=("col_idx, col_offset"))
parser.add_argument('-is_missing_idx', type=int, nargs=2, help="is there a missing in the specific column offset", metavar=("col_idx, col_offset"))
args = parser.parse_args()

if not (args.print_col_type or args.print_col_idx or args.is_missing_idx):
    parser.error('No action requested, please use -print_col_type, -print_col_idx or is_missing_idx appropriately')

def find_tag(line, index):
    to_scan = line[index:]
    result = re.match(EMPTY_RE, to_scan)
    # tag is not empty
    if (not result):
        #print("hi")
        result = re.match(BOOL_RE, to_scan)
        # tag is not BOOL
        if (not result):
            #print("hi")
            result = re.match(INT_RE, to_scan)
            # tag is not INT
            if (not result):
                #print("hi")
                result = re.match(FLOAT_RE, to_scan)
                # tag is not FLOAT
                if (not result):
                    #print("hi")
                    result = re.match(STRING_RE_QUOTES, to_scan)
                    # tag is not a regular string
                    if (not result):
                        #print('hi')
                        result = re.match(STRING_RE, to_scan)
                        # tag cannot be matched, return None
                        if (not result):
                            return result
    # tag is empty
    else:
        return ""
    
    i, j = result.span()
    start = index + i
    end = index + j - 1
    return line[start:end]
    
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
                matched = find_tag(line, line_index + 1)
                if (matched):
                    entries.append(matched)
                    print(matched)
                else:
                    print("malformed entry")
                    break

                line_index += len(matched) + 2
            else:
                break

        rows.append(entries)
    
    return rows


def open_file(name):
    with open(name, "r") as file:
        content = file.read()
        lines = content.split("\n")
        return lines

lines = open_file(args.sor_file)
result = parse_lines(lines)
if (result == None):
    print("Invalid row format")
    exit(1)


