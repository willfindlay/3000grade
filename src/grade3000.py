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
import re
import csv
import random

from .config import Config

from .utils import warn, info, prompt, err

class Question:
    def __init__(self, number, points, deduction=0, message=''):
        self.number = number
        self.points = points
        self.deduction = deduction
        self.message = ''

    # total points earned for the question
    def total(self):
        return self.points - self.deduction

    # clear deductions and feedback from the question
    def clear(self):
        self.deduction = 0
        self.message = ''

    # add a deduction and feedback to the question
    def deduct(self, deduction, message):
        self.deduction = deduction
        self.message = message

    def __repr__(self):
        return f"Question {self.number} [{self.total():.2f} / {self.points:.2f}]"

    # detailed feedback for feedback file creation
    def feedback(self):
        lines = []
        lines.append(f"--- Question {self.number} [{self.points}] ---")
        # save length of header so we can format the footer
        head_len = len(lines[-1])
        # append deductions and feedback if they exist
        if self.deduction > 0:
            lines.append(f"Deductions: {self.deduction}")
            lines.append(self.message)
        else:
            # append encouragement for full marks
            lines.append(random.choice(Config.encouragement))
        lines.append('')
        # append question total
        lines.append(f"Total: {self.total():.2f} / {self.points:.2f}")
        lines.append(Config.soft_divider * head_len)

        return '\n'.join(lines)

class Grade3000:
    def __init__(self, args):
        self.assignment_dir = args.student
        # try to parse student name from directory, otherwise, warn the user
        try:
            self.student = re.search(r"^(.*?)_",
                    os.path.basename(os.path.normpath(self.assignment_dir))).group(1)
        except AttributeError:
            warn(f"Could not parse student name from assignment directory")
            self.student='student'
        # set path for feedback file creation
        self.feedback_file = os.path.join(self.assignment_dir,
                f'{self.student}-feedback.txt')
        # parse assignment format file
        self.questions = self.parse_assignment_info(args.assignment)
        self.actions = ["continue", "deduct", "back", "clear"]
        self.ta = args.ta

    # calculate assignment total and maximum
    def total(self):
        total = 0
        maximum = 0
        for question in self.questions:
            maximum += question.points
            total += question.total()
        return total, maximum

    # generate a feedback file for the student
    def generate_feedback_file(self):
        lines = []
        graded_by = f"GRADED BY: {self.ta}"
        lines.append(Config.hard_divider * len(graded_by))
        lines.append(graded_by)
        lines.append(Config.hard_divider * len(graded_by))
        lines.append('')

        for question in self.questions:
            lines.append(question.feedback())
            lines.append('')

        total, maximum = self.total()
        final_grade = f"FINAL GRADE: {total:.2f} / {maximum:.2f}"
        lines.append(Config.hard_divider * len(final_grade))
        lines.append(final_grade)
        lines.append(Config.hard_divider * len(final_grade))

        return lines

    # write feedback file to disk
    def write_feedback_file(self):
        lines = self.generate_feedback_file()
        feedback = '\n'.join(lines)

        with open(self.feedback_file, 'w') as f:
            f.write(feedback)

    # parse assignment format from file
    def parse_assignment_info(self, assignment):
        questions = []
        with open(assignment, 'r') as f:
            for number, line in enumerate(f):
                questions.append(Question(number + 1, int(line.strip())))
        return questions

    # prompt user for an action per question
    def prompt_for_action(self, question):
        while True:
            points = question.points
            earned = points - question.deduction
            info(f"About to grade {question}")
            print("Options:")

            for n, action in enumerate(self.actions):
                print(f"    {n}) {action} {'(default)' if n==0 else ''}")

            prompt(f"What would you like to do (enter number):")
            action = input().strip()
            try:
                action = int(action)
            except ValueError:
                pass
            if action == '':
                return self.actions[0]
            if action in range(len(self.actions)):
                return self.actions[int(action)]
            err(f"Invalid choice. Please select an option from 0-{len(self.actions) - 1} inclusive.")
            print()

    # prompt the user for a deduction
    def prompt_for_deduction(self, question):
        points = question.points
        warn(f"About to deduct from {question} (non-numeric input to cancel)")

        while True:
            prompt(f"Enter deduction [0 to {points} points]:")
            try:
                deduction = float(input().strip())
            except ValueError:
                return False
            if deduction <= 0:
                return False
            if deduction <= points:
                break
            err("Invalid deduction, not enough points in question")

        prompt(f"Please enter your feedback below (blank line to stop):", end='\n')
        feedback = []
        while True:
            line = input().strip()
            if line == '':
                break
            feedback.append(line)

        question.deduct(deduction, '\n'.join(feedback))
        return True

    # main grading logic
    def grade(self):
        i = 0
        while True:
            while i < len(self.questions):
                print()
                question = self.questions[i]
                action = self.prompt_for_action(question)

                if action == "continue":
                    print()
                    info("The following will be committed to the feedback file:")
                    print(Config.Colors.green, end='')
                    print(question.feedback())
                    print(Config.Colors.end, end='')
                    i += 1
                    continue

                if action == "deduct":
                    did_deduct = self.prompt_for_deduction(question)
                    if not did_deduct:
                        info("Deduction cancelled")
                        continue
                    if Config.next_after_deduct:
                        info("Moving to next question")
                        i += 1
                    continue

                if action == "back":
                    if i > 0:
                        i -= 1
                        continue
                    err("Can't go back beyond first question")
                    continue

                if action == "clear":
                    prompt("Clear deductions? [y/N]")
                    if input().strip().lower() in ['y', 'ye', 'yes']:
                        info("Deductions cleared")
                        question.clear()
                        continue
                    info("Deductions not cleared")
                    continue

            # Finished grading?
            info("Here is a preview of your feedback:")
            print('\n'.join(self.generate_feedback_file()))
            prompt("Would you like to save the changes? [y/N]")
            if input().strip().lower() in ['y', 'ye', 'yes']:
                self.write_feedback_file()
                break
            else:
                i -= 1
