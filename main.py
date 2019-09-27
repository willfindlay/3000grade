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

import argparse
import re

# This has to be before any other local modules are loaded
from src.config import Config
Config.setup()

from src.grade3000 import Grade3000

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-r', '--random', help='Distribute students randomly instead of by assigned TA', dest='random', action='store_true')
    parser.add_argument('-s', '--sync', help='Update the list of assigned TAs', dest='sync', action='store_true')
    parser.add_argument('assignment', help='Which assignment to grade. Format like: A1, or T2, etc.', type=str)

    args = parser.parse_args()

    if not re.match(r"^[AT]\d+$", args.assignment):
        raise Exception("Please format your assignment name like A1, T2, etc.")

    grade3000 = Grade3000(args)
