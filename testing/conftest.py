'''
Pytest template for automated tests
'''
import os
import sys


# Ensure project directory is included in system path
DIR = os.path.dirname(os.path.realpath(__file__))
TLD = os.path.abspath(os.path.join(DIR, os.pardir))
if TLD not in sys.path:
    sys.path.append(TLD)

colors = {
    'FAIL' : '\033[91m',
    'PASS' : '\033[92m',
    'WARN' : '\033[93m',
    'END' : '\033[0m',
    }


def red_text(string):
    '''Returns string wrapped in encodings to make it display red'''
    return f"{colors['FAIL']}{string}{colors['END']}"


def yellow_text(string):
    '''Returns string wrapped in encodings to make it display yellow'''
    return f"{colors['WARN']}{string}{colors['END']}"


def green_text(string):
    '''Returns string wrapped in encodings to make it display green'''
    return f"{colors['PASS']}{string}{colors['END']}"


def green_print(string):
    '''Prints the string in green'''
    print(green_text(string), "\n")


def red_print(string):
    '''Prints the string in red'''
    print(red_text(string))


def yellow_print(string):
    '''Prints the string in yellow'''
    print(yellow_text(string))


def pytest_runtest_setup(item):
    '''Write the test's docstring to make test output more readable'''
    yellow_print("\n\n\n***** TEST DESCRIPTION: *****")
    yellow_print(item.function.__doc__)
    yellow_print("*****************************\n\n")
