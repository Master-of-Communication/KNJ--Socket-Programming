import os

from socket import *
import random
from datetime import datetime
import time
import threading
import json

def check_python_version_windows():
    try:
        os.system("python --version")
    except:
        print("Python is not installed.")

#check_python_version_windows()

def check_python_version_macos():
    try:
        os.system("python3 --version")
    except:
        print("Python is not installed.")

#check_python_version_macos()

def check_python_version_ubuntu():
    try:
        os.system("python3 --version")
    except:
        print("Python is not installed.")

check_python_version_ubuntu()

