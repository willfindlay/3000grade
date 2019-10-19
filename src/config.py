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

class Config:
    hard_divider = "="
    soft_divider = "-"

    next_after_deduct = True

    encouragement = ["Awesome!","Great!","Good job!",
            "Fantastic!","Keep it up!","Great job!",
            "Perfect!","Perfect answer!","Great work!",
            "A cogent response!","Well said!","Full marks!",
            "Well done!","Superb!","Excellent!",
            "Excellent job!","Good work!"]

    class Colors:
        black   = u"\u001b[30m"
        red     = u"\u001b[31m"
        green   = u"\u001b[32m"
        yellow  = u"\u001b[33m"
        blue    = u"\u001b[34m"
        magenta = u"\u001b[35m"
        cyan    = u"\u001b[36m"
        white   = u"\u001b[37m"
        end     = u"\u001b[0m"

    @staticmethod
    def setup():
        pass
