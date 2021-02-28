import csv
import os


def csv_fp(file: str):
    """

    :param file: a valid path to a csv file
    :return: csv file pointer
    """
    assert os.path.isfile(file), f"{file} is not a path to a valid file"
    fp = open(file)
    try:
        fp = csv.reader(fp)
    except Exception as e:
        raise Exception("file not a csv file")
    return fp
