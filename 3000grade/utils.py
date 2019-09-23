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

PROJECT_DIR = os.path.dirname(__file__)

# Return absolute path to a file within this project directory
def project_path(p):
    return os.path.realpath(os.path.join(PROJECT_DIR, '..', p))

def maybe_create_directory(p):
    if not os.path.exists(os.path.realpath(p)):
        os.makedirs(os.path.realpath(p))

# Create file if it doesn't exist
def maybe_create(p):
    if not os.path.exists(os.path.realpath(p)):
        maybe_create_directory(os.path.join(p, '..'))
        f = open(p, 'w')
        f.close()
