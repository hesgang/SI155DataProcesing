import os
import argparse
import importlib
import sys
import pip


parser = argparse.ArgumentParser(description='install requirements')
parser.add_argument('--cuda', default=None, type=str)
args = parser.parse_args()

comm_pkgs = f'''
pandas
numpy
lxml
pyasn1
xlrd==1.2.0
tkinter
openpyxl
PyQt5
PySide2
html5lib
beautifulsoup4
PyWavelets
matplotlib
scikit-learn
sympy
tqdm
'''

# git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI


def run_install(pkgs):
    if pkgs:
        try:
            # out = __import__(f"{library}")
            importlib.import_module(pkgs)
        except ImportError:
            print(f"Error: {pkgs} library not found. Please install this library before running the script.")
            os.system('pip install -i https://pypi.douban.com/simple/ %s' % pkgs.split()[0])


version = sys.version[:6]
if version[:3] != '3.9':
    key = input("""The current python version is {}, which is best used 3.9\nContinue[Y\\N]:""".format(version[:3]))
    while True:
        if key == 'n' or key == 'N':
            sys.exit()
        elif key == 'y' or key == 'Y':
            for line in comm_pkgs.split('\n'):
                run_install(line)
            break
        else:
            key = input('Continue[Y\\N]')
else:
    for line in comm_pkgs.split('\n'):
        run_install(line)








