'''
Pytest template for automated tests
'''
import os
import sys

import pytest


# Ensure project directory is included in system path
DIR = os.path.dirname(os.path.realpath(__file__))
TLD = os.path.abspath(os.path.join(DIR, os.pardir))
if TLD not in sys.path:
    sys.path.append(TLD)

class bcolors:
    FAIL = '\033[91m'
    PASS = '\033[92m'
    WARN = '\033[93m'
    ENDC = '\033[0m'


def red_text(string):
    return f"{bcolors.FAIL}{string}{bcolors.ENDC}"


def yellow_text(string):
    return f"{bcolors.WARN}{string}{bcolors.ENDC}"


def green_text(string):
    return f"{bcolors.PASS}{string}{bcolors.ENDC}"


def green_print(string):
	print(green_text(string), "\n")


def red_print(string):
	print(red_text(string))


def yellow_print(string):
	print(yellow_text(string))


def pytest_runtest_setup(item):
    yellow_print("\n\n\n***** TEST DESCRIPTION: *****")
    yellow_print(item.function.__doc__)
    yellow_print("*****************************\n\n")
