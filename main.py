#! /usr/bin/env python3

# A CLI script to help with COMP3000-related grading.
# Copyright (C) 2019  William Findlay
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

import os, sys
import argparse
import re

# This has to be before any other local modules are loaded
from src.config import Config
Config.setup()

from src import utils
from src.grade3000 import Grade3000

EXAMPLES = f"""{Config.Colors.magenta}
Example Usage:
    grade3000 -s ~/teaching/a1/Findlay-William_36687205_assignsubmission_file_ -a ~/assignments/a1 -t William
{Config.Colors.end}
"""

INSTRUCTIONS = f"""{Config.Colors.cyan}Instructions:
    When you run the script, pass the student's submission directory with the -s flag,
    the assignment format file with the -a flag, and your first name with the -t flag.

    To create an assignment format file, just make a plaintext file with the point total
    of each question on separate lines. For example, if I had an assignment with 5 questions,
    worth 1, 1, 3, 4, and 3 points, I would do the following:

    1
    1
    3
    4
    3

    When you run the script, you will be prompted for an action for each question.
    Typically, you want to either make a deduction, or move on if the student got full
    marks for the question.

    To make a deduction, type 1, and then enter the points to be deducted when prompted.
    Once you make a deduction, you will be prompted for feedback. Enter as many lines
    of feedback as you like, and commit by entering a blank line at the end.

    By default, the script will move to the next question immediately after a deduction.
    To change this, edit Config.py.

    When you are finished grading, you will be shown an overview of the resulting
    feedback file and asked to either commit the changes or go back to the last question.
    If you commit the changes, the script will create a feedback file in the student's directory
    which you can then upload to cuLearn.

    Good luck, and happy grading!{Config.Colors.end}
"""

if __name__ == "__main__":

    parser = argparse.ArgumentParser(prog='grade3000', formatter_class=argparse.RawDescriptionHelpFormatter,
            epilog=INSTRUCTIONS+EXAMPLES)

    parser.add_argument('-s', '--student',
            dest='student',
            metavar='directory',
            help="Directory containing student's assignment",
            type=utils.dir_path)

    parser.add_argument('-a', '--assignment',
            dest='assignment',
            metavar='format-file',
            help="File containing question numbers separated by line breaks",
            type=str)

    parser.add_argument('-t', '--ta',
            dest='ta',
            metavar='your-name',
            help="Your (TA's) name",
            type=str)

    parser.add_argument('--no-color',
            dest='show_color',
            action='store_false',
            help='Disable colored output to terminal')

    parser.add_argument('--instructions',
            dest='instructions',
            action='store_true',
            help='Print detailed instructions and exit')

    args = parser.parse_args()

    if not args.show_color:
        Config.Colors.black   = ''
        Config.Colors.red     = ''
        Config.Colors.green   = ''
        Config.Colors.yellow  = ''
        Config.Colors.blue    = ''
        Config.Colors.magenta = ''
        Config.Colors.cyan    = ''
        Config.Colors.white   = ''
        Config.Colors.end     = ''

    if args.instructions:
        print(INSTRUCTIONS)
        sys.exit()

    if not args.student or not args.assignment or not args.ta:
        parser.error("You must specify a submission directory (-s), an assignment format file (-a), and your first name (-t)")

    grade3000 = Grade3000(args)
    grade3000.grade()
