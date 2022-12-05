from filter import filter
import sys
import subprocess
import importlib.util

def install(package):
    spec = importlib.util.find_spec(package)
    if spec is None:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package], 
                              stdout=subprocess.DEVNULL,
                              stderr=subprocess.STDOUT)

f = open('requirements.txt', 'r')
for package in f.readlines():
    install(package)

filter()