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
import seaborn as sns

from src.package.enumsoperations.string_enums import WORDS
from src.package.listoperations.list_operations import get_first_element, get_second_element


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
            self, identified_markers: pd.DataFrame, absolute_path_to_distribution_output_directory: str) -> None:
        """ processes time course distributions... """

        try:

            identified_markers_column: list = DistributionOperations.__get_identified_markers(identified_markers)

            complete_clinical_data: pd.DataFrame = \
                self.differential_expression_processor_object.get_complete_clinical_dataframe()

            unique_treatments: list = complete_clinical_data[
                self.differential_expression_processor_object.get_target_variable_column_name()].unique()

            DistributionOperations.__plot_time_course_line_distribution(
                identified_markers_column, absolute_path_to_distribution_output_directory,
                unique_treatments, complete_clinical_data)

            DistributionOperations.__plot_heatmap_time_course_distribution(
                identified_markers_column, absolute_path_to_distribution_output_directory,
                unique_treatments, complete_clinical_data)

        except ValueError as e:
            raise ValueError("an {} error has occurred".format(e))

        except TypeError as e:
            raise TypeError("an {} error has occurred".format(e))

    @classmethod
    def __plot_heatmap_time_course_distribution(cls, identified_markers_columns: list,
                                                absolute_path_to_distribution_output_directory: str,
                                                unique_treatments: list, complete_clinical_data: pd.DataFrame) -> None:
        """ generates heatmap distribution """

        clinical_data_with_treatments_of_interest: pd.DataFrame = complete_clinical_data[complete_clinical_data[
            WORDS.TREATMENT_COLUMN_NAME].str.contains(get_first_element(unique_treatments)) |
            complete_clinical_data[WORDS.TREATMENT_COLUMN_NAME].str.contains(get_second_element(unique_treatments))]

        encoded_dummy_time = pd.get_dummies(clinical_data_with_treatments_of_interest[WORDS.VISIT])

        clinical_data_with_treatments_of_interest = pd.concat([clinical_data_with_treatments_of_interest[
            identified_markers_columns], encoded_dummy_time], axis=1)

        correlation_matrix = clinical_data_with_treatments_of_interest.corr()

        plt.figure(figsize=(22, 20))

        sns.heatmap(correlation_matrix, cmap='coolwarm',  vmax=0.8, vmin=0.8, square=True, center=0)

        plt.title("Correlation time course of biomarkers through D0, D1, and D2")
        plt.xlabel("Biomaker + Visits")
        plt.ylabel("Biomaker + Visits ")
        plt.legend(fontsize="small")

        plt.savefig(os.path.join(absolute_path_to_distribution_output_directory, "time_series_of_biomaker_heatmap.pdf"))


    @classmethod
    def __plot_time_course_line_distribution(cls, identified_markers_columns: list,
                                             absolute_path_to_distribution_output_directory: str, unique_treatments: list,
                                             complete_clinical_data: pd.DataFrame) -> None:
        """
        Time course distribution function.
        """

        warnings.filterwarnings("ignore", category=UserWarning, module="matplotlib")

        plt.figure(figsize=(26, 24))

        for treatment in unique_treatments:

            complete_clinical_data_treatment: pd.DataFrame = complete_clinical_data[complete_clinical_data[
                                                        WORDS.TREATMENT_COLUMN_NAME] == treatment]

            DistributionOperations.__process_biomarker_column(identified_markers_columns,
                                                              complete_clinical_data_treatment, treatment)

        plt.title("Time course of biomarkers through D0, D1, and D2")
        plt.xlabel("Visits")
        plt.ylabel("Biomaker")
        plt.legend(fontsize="small")

        plt.savefig(os.path.join(absolute_path_to_distribution_output_directory, "time_series_of_biomaker.pdf"))

    @classmethod
    def __process_biomarker_column(cls, biomarkers: list, complete_clinical_data: pd.DataFrame, label: str):
        """ process per biomarker column"""

        return [plt.plot(complete_clinical_data[WORDS.VISIT],
                         complete_clinical_data[biomarker], label=f'{label} - {biomarker}') for biomarker in biomarkers]



    @classmethod
    def __get_identified_markers(cls, identified_markers: pd.DataFrame) -> list:
        """gets identified markers as a list """

        return list(set(list(identified_markers[WORDS.IDENTIFIED_MARKER_COLUMN_NAME])))
