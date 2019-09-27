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

import re
import csv

import requests
from bs4 import BeautifulSoup

from .config import Config

class Grade3000:
    def __init__(self, args):
        self.assignment = args.assignment
        self.random = args.random
        self.sync = args.sync

        # login to culearn
        self.session = requests.session()
        login_data = {'username': Config.username, 'password': Config.password}
        res = self.session.post('https://culearn.carleton.ca/moodle/login/index.php', data=login_data)

        # parse comp3000 page
        res = self.session.get(Config.course_page_url)
        self.course_page = BeautifulSoup(res.content, 'html.parser')

        self.tas_file = Config.tas_file

        self.maybe_sync()

    def maybe_sync(self):
        if not self.sync:
            return

        data = {'separator': 'comma'}

        # export grades
        res = self.session.post(Config.export_grades_url, data=data, allow_redirects=True)
        with open(self.tas_file, 'wb') as f:
            f.write(res.content)

    def randomly_assign_students(self):
        pass

    def download_student_submissions(self):
        pass

    def organize_student_submissions(self):
        pass
