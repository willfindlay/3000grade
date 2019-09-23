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

from config import Config

class Student:
    def __init__(self, student_number, surname, firstname, email, section, ta):
        self.student_number = student_number
        self.surname = surname
        self.firstname = firstname
        self.email = email
        self.section = section
        self.ta = ta

    def __repr__(self):
        return f"{self.firstname} {self.surname} ({self.student_number})"

class CuLearn:
    def __init__(self):
        self.students = []

        with open(Config.students_file, 'r') as f:
            for line in f:
                if line.strip() == '':
                    continue
                matches = re.findall(r"(\d*)\s+([a-zA-Z]*)\s+([a-zA-Z]*)\s+(.*@.*\.ca)\s+([A-Z]\d)\s+([a-zA-Z]*)", line)
                student_number, surname, firstname, email, section, ta = tuple(matches[0])
                self.students.append(Student(int(student_number), surname, firstname, email, section, ta))

        for student in self.students:
            print(student)
