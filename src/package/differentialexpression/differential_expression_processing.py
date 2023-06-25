"""
A collection of classes or functions that performs differential expression processing
"""


from typing import Optional

import pandas as pd

from src.package.enumsoperations.numerical_enums import POSITIONS
from src.package.enumsoperations.string_enums import WORDS
from src.package.listoperations.list_operations import get_at_least_fifth_element
from scipy.stats import ttest_ind


class DifferentialExpressionProcessor:
    """ class that performs differential  expression calculations. """

    clinical_data = None
    target_variable_column_name = None

    def __init__(self, complete_clinical_dataframe: pd.DataFrame,  target_variable_column_name: str) -> None:
        """  Set the dataframe for differential expression calculation """

        DifferentialExpressionProcessor.clinical_data = complete_clinical_dataframe
        DifferentialExpressionProcessor.target_variable_column_name = target_variable_column_name

        self.__target_variable_column_name = target_variable_column_name
        self.__complete_clinical_dataframe = complete_clinical_dataframe
        self.__differential_expression_data: Optional[pd.DataFrame] = None

    def differential_expression_calculation(self, p_value_threshold: float) -> None:
        """ calculates differential expression """

        try:

            self.__differential_expression_data: Optional[pd.DataFrame] = \
                DifferentialExpressionProcessor.__process_differential_expression()

            self.__differential_expression_data: pd.DataFrame = self.__differential_expression_data[
                self.__differential_expression_data[WORDS.P_VALUE] <= p_value_threshold]

        except ValueError as e:
            raise ValueError("an {} error has occurred".format(e))

        except TypeError as e:
            raise TypeError("an {} error has occurred".format(e))

    @classmethod
    def __process_differential_expression(cls) -> pd.DataFrame:
        """ process differential expression """

        biomarker_measures_columns = get_at_least_fifth_element(list(cls.clinical_data.columns))

        compute_differential_expression = \
            lambda col: ttest_ind(
                cls.clinical_data[cls.clinical_data[
                    cls.target_variable_column_name] == WORDS.TREATMENT_COLUMN_ROW_VALUE_DRUG][col],
                cls.clinical_data[cls.clinical_data[cls.target_variable_column_name] ==
                    WORDS.TREATMENT_COLUMN_ROW_VALUE_PLACEBO][col], equal_var=True)

        differential_analysis_outcome = pd.DataFrame({
            feature_column_name: compute_differential_expression(feature_column_name)
            for feature_column_name in biomarker_measures_columns})

        return differential_analysis_outcome.T.reset_index().rename(
            columns={
                WORDS.INDEX: WORDS.IDENTIFIED_MARKER_COLUMN_NAME,
                POSITIONS.FIRST_POSITION: WORDS.T_STATISTICS,
                POSITIONS.SECOND_POSITION: WORDS.P_VALUE})

    def get_identified_biomarkers(self) -> pd.DataFrame:
        """ returns the dataframe of identified or differentially expressed biomarkers """

        return self.__differential_expression_data

    def get_complete_clinical_dataframe(self) -> pd.DataFrame:
        """  returns the dataframe of the patients' data """

        return self.__complete_clinical_dataframe

    def get_target_variable_column_name(self) -> str:
        """  returns the name of the target variable """

        return self.__target_variable_column_name

