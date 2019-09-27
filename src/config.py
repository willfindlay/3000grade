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

from src import utils

class Config:

    # Your CuLearn username
    # Will try checking CULEARN_USER environment variable if not set
    username = ""
    # Your CuLearn password
    # Will try checking CULEARN_PASS environment variable if not set
    password = ""

    # Location of assinged TA folder
    # Defaults to /path/to/this/project/tas
    tas_file = "" or utils.project_path("tas")

    course_page_url = "https://culearn.carleton.ca/moodle/course/view.php?id=131843"
    export_grades_url = "https://culearn.carleton.ca/moodle/grade/export/txt/export.php?id=131843"

    @staticmethod
    def setup():
        try:
            from dotenv import load_dotenv
            load_dotenv()
        except ModuleNotFoundError:
            pass

        #utils.maybe_create(Config.students_file)

        if Config.username == "":
            Config.username = os.getenv('CULEARN_USER')
        if Config.password == "":
            Config.password = os.getenv('CULEARN_PASS')

        if not Config.username:
            raise Exception("Please set your cuLearn username as CULEARN_USER environment variable or in src/config.py")
        if not Config.password:
            raise Exception("Please set your cuLearn password as CULEARN_PASS environment variable or in src/config.py")
