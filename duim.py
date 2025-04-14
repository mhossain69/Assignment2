#!/usr/bin/env python3

import subprocess
import sys
import os
import argparse

'''
OPS445 Assignment 2 - Winter 2022
Program: duim.py 
Author: Mohd Abrar Hossain
The python code in this file (duim.py) is original work written by Mohd Abrar Hossain. No code in this file is copied from any other source 
except those provided by the course instructor, including any person, 
textbook, or on-line resource. I have not shared this python script 
with anyone or anything except for submission for grading.  
I understand that the Academic Honesty Policy will be enforced and 
violators will be reported and appropriate action will be taken.

Description: This script improves upon the standard `du` command by providing
a visual representation of disk usage in the form of bar graphs for each 
subdirectory within a specified directory.

Date: 13th April 2025
'''

def parse_command_args():
    parser = argparse.ArgumentParser(description="DU Improved -- See Disk Usage Report with bar charts", epilog="Copyright 2022")
    parser.add_argument("-l", "--length", type=int, default=20, help="Specify the length of the graph. Default is 20.")
    parser.add_argument("-H", "--human-readable", action='store_true', help="Print sizes in human readable format.")
    parser.add_argument("target", nargs='?', default=os.getcwd(), help="The directory to scan.")
    args = parser.parse_args()
    return args

def percent_to_graph(percent, total_chars):
    if not (0 <= percent <= 100):
        raise ValueError("Percent must be between 0 and 100.")
    
    num_equals = round(percent / 100 * total_chars)
    num_spaces = total_chars - num_equals
    return '=' * num_equals + ' ' * num_spaces

def call_du_sub(location):
    command = ['du', '-d', '1', location]
    result = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, _ = result.communicate()
    output = output.decode('utf-8').strip().split('\n')
    return [line for line in output if line]  # Filter out any empty lines

def create_dir_dict(alist):
    dir_dict = {}
    for entry in alist:
        size, path = entry.split(maxsplit=1)
        dir_dict[path] = int(size)
    return dir_dict

def human_readable_size(size):
    for unit in ['B', 'K', 'M', 'G']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} T"

if __name__ == "__main__":
    args = parse_command_args()
    
    if not os.path.isdir(args.target):
        print(f"Error: The target '{args.target}' is not a valid directory.")
        sys.exit(1)

    du_output = call_du_sub(args.target)
    dir_dict = create_dir_dict(du_output)

    # Calculate total size
    total_size = sum(dir_dict.values())

    for path, size in dir_dict.items():
        percent = (size / total_size) * 100
        bar_graph = percent_to_graph(percent, args.length)
        size_display = human_readable_size(size) if args.human_readable else str(size)
        print(f"{percent:3.0f} % [{bar_graph}] {size_display} {path}")

    total_size_display = human_readable_size(total_size) if args.human_readable else str(total_size)
    print(f"Total: {total_size_display} {args.target}")
