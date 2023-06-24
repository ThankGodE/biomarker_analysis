from typing import Optional

import pandas as pd


class CsvReader:
    """ a reader for csv files """

    csv_file = None

    def __init__(self, csv_file_path: str) -> None:
        """  Set the  CSV file for conversion to a dataframe """

        CsvReader.csv_file = csv_file_path

        self.__clinical_csv_dataframe: Optional[pd.DataFrame] = None

    def generate_dataframe(self, delimiter: str) -> None:
        """ generates dataframe by running the generate_dataframe method. """

        try:

            self.__clinical_csv_dataframe: Optional[pd.DataFrame] = pd.read_csv(self.csv_file, sep=delimiter)

        except FileNotFoundError:
            raise FileNotFoundError("{} files do not exist or is not readable".format(self.csv_file))

    def get_processed_dataframe(self) -> pd.DataFrame:
        """ returns the dataframe """

        return self.__clinical_csv_dataframe



