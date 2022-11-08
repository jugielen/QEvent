from os.path import exists

from DBQE import create_db
from gui import start_gui


def main():
    if not exists("QE.db"):
        create_db()
    start_gui()


main()


