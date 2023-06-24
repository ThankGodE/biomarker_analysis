"""
A collection of classes or functions that performs distribution statistics and plots
"""
import os
import sys
import warnings
from typing import Optional

from src.package.differentialexpression.differential_expression_processing import DifferentialExpressionProcessor

import pandas as pd
import matplotlib.pyplot as plt

from src.package.enumsoperations.string_enums import WORDS


class DistributionOperations:
    """
    Class for distribution operations statistics
    """

    differential_expression_processor_object = None
    target_variable_column_name = None

    def __init__(self, differential_expression_processor: DifferentialExpressionProcessor) -> None:
        """  Set the dataframe for distribution operations """

        DistributionOperations.differential_expression_processor_object = differential_expression_processor


    def process_time_course_distribution(
            self, identified_markers: pd.DataFrame, absolute_path_to_distribution_output: str) -> None:
        """ processes time course distributions """

        try:

            DistributionOperations.__plot_time_course_distribution(
                identified_markers, absolute_path_to_distribution_output)

        except ValueError as e:
            raise ValueError("an {} error has occurred".format(e))

        except TypeError as e:
            raise TypeError("an {} error has occurred".format(e))

    @classmethod
    def __plot_time_course_distribution(cls, identified_markers: pd.DataFrame,
                                        absolute_path_to_distribution_output: str) -> None:
        """
        Time course distribution function.
        """

        complete_clinical_data = cls.differential_expression_processor_object.get_complete_clinical_dataframe()

        identified_markers_column = DistributionOperations.__get_identified_markers(identified_markers)

        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

        plt.figure(figsize=(8, 6))

        for treatment in complete_clinical_data[
            cls.differential_expression_processor_object.get_target_variable_column_name()].unique():

            complete_clinical_data_treatment = complete_clinical_data[complete_clinical_data[
                                                        WORDS.TREATMENT_COLUMN_NAME] == treatment]

            DistributionOperations.__process_biomarker_column(identified_markers_column,
                                                              complete_clinical_data_treatment, treatment)

        plt.title("Time course of biomarkers through D0, D1, and D2")
        plt.xlabel("Visits")
        plt.ylabel("Biomaker")
        plt.legend(loc='best')

        plt.savefig(absolute_path_to_distribution_output)

    @classmethod
    def __process_biomarker_column(cls, biomarkers: list, complete_clinical_data: pd.DataFrame, label: str):
        """ process per biomarker column"""

        return [plt.plot(complete_clinical_data[WORDS.VISIT],
                         complete_clinical_data[biomarker], label=f'{label} - {biomarker}') for biomarker in biomarkers]



    @classmethod
    def __get_identified_markers(cls, identified_markers: pd.DataFrame) -> list:
        """gets identified markers as a list """

        return list(set(list(identified_markers[WORDS.IDENTIFIED_MARKER_COLUMN_NAME])))
