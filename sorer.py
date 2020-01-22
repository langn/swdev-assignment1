#! /usr/bin/python3

import argparse
import re

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
