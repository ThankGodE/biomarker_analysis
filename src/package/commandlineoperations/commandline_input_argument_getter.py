import argparse


class CliInputArgumentGetter:
    """Wrapper for argparse that returns an object of the class for ease of use"""

    @classmethod
    def get_cli_input_arguments(cls, args=None) -> argparse.Namespace:
        """gets input arguments from the commandline interface """

        parser = argparse.ArgumentParser(
            prog="identify_biomarkers.py",
            usage="""identify_biomarkers.py -h""",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            description=(
                """
                This script identifies biomarkers of interest associated with drug effect

                Required:
                    - Pandas
                    - Python >= 3.10
                    - python-dotenv>=1.0.0
                """
            ),
        )
        parser.add_argument(
            "-o",
            "--path2out",
            help="absolute directory path to processed output files ",
            required=True,
        )

        parser.add_argument(
            "-i",
            "--path2csv",
            help="""absolute path to biomarker measurement input CSV file """,
            required=True,
        )

        parser.add_argument(
            "-p",
            "--p_value",
            help="""p_value threshold to define statistically significance or differential expression""",
            default=0.05,
            type=float
        )

        return parser.parse_args(args)
