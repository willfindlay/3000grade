import os, sys

from dotenv import load_dotenv

class Config:

    # Your CuLearn username
    # Will try checking CULEARN_USER environment variable if not set
    username = ""
    # Your CuLearn password
    # Will try checking CULEARN_PASS environment variable if not set
    password = ""

    @staticmethod
    def setup():
        load_dotenv()
        if Config.username == "":
            Config.username = os.getenv('CULEARN_USER')
        if Config.password == "":
            Config.password = os.getenv('CULEARN_PASS')
