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

from dotenv import load_dotenv

import utils

class Config:

    # Your CuLearn username
    # Will try checking CULEARN_USER environment variable if not set
    username = ""
    # Your CuLearn password
    # Will try checking CULEARN_PASS environment variable if not set
    password = ""

    # Location of your students file
    # Defaults to /path/to/this/project/students
    students_file = "" or utils.project_path("students")

    @staticmethod
    def setup():
        load_dotenv()

        utils.maybe_create(Config.students_file)

        if Config.username == "":
            Config.username = os.getenv('CULEARN_USER')
        if Config.password == "":
            Config.password = os.getenv('CULEARN_PASS')
