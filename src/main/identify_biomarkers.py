"""
This script identifies biomarkers of interest associated with drug effect

Required:
    - Pandas
    - Python >= 3.10
    - python-dotenv>=1.0.0

"""

# -*- coding: utf-8 -*-
__author__ = "{ThankGod Ebenezer}"

import os
import sys

import pandas as pd

# Futures and third party libraries

# Futures local application libraries, source package
from addscriptdir2path import add_package2env_var

# re-define system path to include modules, packages
# and libraries in environment variable
add_package2env_var()


from src.package.commandlineoperations.commandline_input_argument_getter import CliInputArgumentGetter
from src.package.differentialexpression.differential_expression_processing import DifferentialExpressionProcessor
from src.package.enumsoperations.string_enums import WORDS
from src.package.fileoperations.csv_reader import CsvReader
from src.package.filewriteoperations.file_writer import FileWriter
from src.package.profiling.profiling import begin_profiling, end_profiling, ProfileLogger
from src.package.statisticsoperations.distribution_operations import DistributionOperations


# profiling begins ###
profiling_starting = begin_profiling("")


###################################################
# main function                               #####
###################################################
def main() -> None:
    """main function to run commandline arguments and call other functions to run."""

    args_cli_values = CliInputArgumentGetter.get_cli_input_arguments()

    path2output_dir = args_cli_values.path2out
    path2input_csv = args_cli_values.path2csv
    p_value_threshold = args_cli_values.p_value

    try:

        # load CSV and create dataframe
        csv_reader: CsvReader = CsvReader(path2input_csv)
        csv_reader.generate_dataframe(",")

        clinical_dataframe: pd.DataFrame = csv_reader.get_processed_dataframe()

        # drop missing values
        complete_clinical_dataframe = clinical_dataframe.dropna()

        # run differential expression
        differential_expression_processor: DifferentialExpressionProcessor = \
            DifferentialExpressionProcessor(complete_clinical_dataframe, WORDS.TREATMENT_COLUMN_NAME)

        differential_expression_processor.differential_expression_calculation(p_value_threshold)

        # distribution operations
        distribution_operation: DistributionOperations = DistributionOperations(differential_expression_processor)

    except ValueError as e:

        raise ValueError("Exception caught: {}".format(e))

    else:

        # output pre-filtering of missing values

        FileWriter(os.path.join(path2output_dir, "descriptive_statistics_all_columns.txt"), "w", ).write(
            clinical_dataframe.describe(), False, True)

        FileWriter(os.path.join(path2output_dir, "descriptive_statistics_treatment.txt"), "w",
                   ).write(clinical_dataframe[["TREATMENT"]].describe(), True, True)

        FileWriter(os.path.join(path2output_dir, "descriptive_statistics_gender.txt"), "w",
                   ).write(clinical_dataframe[["GENDER"]].describe(), True, True)

        FileWriter(os.path.join(path2output_dir, "descriptive_statistics_markertp53.txt"), "w",
                   ).write(clinical_dataframe[["MARKER_TP53"]].describe(), True, True)

        FileWriter(os.path.join(path2output_dir, "report_missing_values.txt"), "w",
                   ).write(clinical_dataframe["GENDER"].isna().describe(), True, False)

        # output post-filtering of missing values

        FileWriter(os.path.join(path2output_dir, "complete_data_with_biomarkers.txt"), "w",
                   ).write(complete_clinical_dataframe, False, True)

        FileWriter(os.path.join(path2output_dir, "complete_treatment_statistics.txt"), "w",
                   ).write(complete_clinical_dataframe[["TREATMENT"]].describe(), True, True)

        FileWriter(os.path.join(path2output_dir, "complete_gender_statistics.txt"), "w",
                   ).write(complete_clinical_dataframe[["GENDER"]].describe(), True, True)

        FileWriter(os.path.join(path2output_dir, "complete_gender_statistics.txt"), "w",
                   ).write(complete_clinical_dataframe[["MARKER_TP53"]].describe(), True, True)

        # output differential expression outputs
        FileWriter(os.path.join(path2output_dir, "differentially_expressed_biomarkers.txt"), "w",
                   ).write(differential_expression_processor.get_identified_biomarkers(), True, True)

        # distribution operations output
        distribution_operation.process_time_course_distribution(
            differential_expression_processor.get_identified_biomarkers(),
            path2output_dir)


###################################################################################
# run __main__ ####################################################################
###################################################################################

if __name__ == "__main__":
    main()


time_end = end_profiling()
ProfileLogger(profiling_starting, time_end).log_profiling()
