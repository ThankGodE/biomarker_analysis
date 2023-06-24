"""
A collection of functions that performs file writing operations.
"""

__name__ = "__main__"

import logging

import pandas as pd


class FileWriter:
    """ The FileWriter class handles the writing of the data to a file. """

    def __init__(self, file_path, mode):
        """
        Creates a new FileWriter object.

        :param file_path: Path to the file.
        :param mode: Mode of the file.
        """
        self.file_path = file_path
        self.mode = mode

    def write(self, data: pd.DataFrame, write_index: bool, write_header: bool):
        """
        Writes data to a file. Data here is a DataFrame

        :param data: DataFrame to write.
        """

        data.to_csv(self.file_path, sep="\t", mode=self.mode, index=write_index, header=write_header)

        logging.info(" writing dataframe to file: {}".format(self.file_path))
