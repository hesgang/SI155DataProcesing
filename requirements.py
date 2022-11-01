import os
import argparse
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
PyQt5-tools
'''

# git+https://github.com/philferriere/cocoapi.git#subdirectory=PythonAPI

version = sys.version[:6]
if version[:3] != '3.9':
    key = input("""The current python version is {}, which is best used 3.6\nContinue[Y\\N]:""".format(version[:3]))
    while True:
        if key == 'n' or key == 'N':
            sys.exit()
        elif key == 'y' or key == 'Y':
            for line in comm_pkgs.split('\n'):
                if len(line) > 0:
                    os.system('pip install -i https://pypi.douban.com/simple/ %s' % line.split()[0])
            break
        else:
            key = input('Continue[Y\\N]')
else:
    for line in comm_pkgs.split('\n'):
        if len(line) > 0:
            os.system('pip install -i https://pypi.douban.com/simple/ %s' % line.split()[0])

