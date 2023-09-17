import argparse
import logging
import os

import funion

from funion.contract_dependency import combine_involved_contracts
from dacon.traverse_data_collection import data_collection

logger = logging.getLogger(__name__)



def register_basic_arguments(parser: argparse.ArgumentParser):
    # Define command-line arguments
    parser.add_argument('-p','--solidity_file_path', type=str, default="",
                        help="specify the path where Solidity files are held.")
    parser.add_argument('-n','--solidity_file_name', type=str, default="",
                        help="specify the name of the solidity file of the target contract.")

    parser.add_argument('--contract_name', type=str, help="specify the name of the target contract")
    parser.add_argument('-v','--log_level', type=int, default=3)
    parser.add_argument('--solv', type=str, default="0.5.0", help="the compiler version of the target contract")
    parser.add_argument('--imports', nargs="+", type=str, default=["."],
                        help="specify the paths that the dependent solidity files reside")

    parser.add_argument('-rp','--result_path', type=str, default="", help="the directory to save the merged solidity file.")

    parser.add_argument('--remove_comments', default=False, action='store_true')

    return parser


def set_logging_level(args):
    if args.log_level == 4:
        logging.basicConfig(
            level=logging.DEBUG,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s',  # Define the log message format
            datefmt='%Y-%m-%d %H:%M:%S'  # Define the date-time format
        )
    elif args.log_level == 5:
        logging.basicConfig(
            level=logging.ERROR,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s',  # Define the log message format
            datefmt='%Y-%m-%d %H:%M:%S'  # Define the date-time format
        )
    elif args.log_level==3:
        logging.basicConfig(
            level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
            format='%(asctime)s [%(filename)s:%(lineno)d] [%(levelname)s]: %(message)s',  # Define the log message format
            datefmt='%Y-%m-%d %H:%M:%S'  # Define the date-time format
        )
    else:
        pass


def main():
    # Create an ArgumentParser object
    parser = argparse.ArgumentParser(description="A simple script with command-line arguments.")

    parser = register_basic_arguments(parser)

    # Parse the command-line arguments
    args = parser.parse_args()
    if args.remove_comments:
        funion.contract_dependency.flag_remove_comments=True

    set_logging_level(args)

    solidity_file_path_name = args.solidity_file_path + args.solidity_file_name
    if os.path.exists(solidity_file_path_name):
        try:

            data_collection(args)

        except Exception as e:
            logger.error("{}".format(e.with_traceback()))


    else:
        logger.error("file does not exit: {}".format(solidity_file_path_name))


