"""
The command-line interface for the tool.
"""
import argparse
from astrotimes import astrotimes

def main():
    parser = argparse.ArgumentParser(
        description="A simple CLI tool for printing sunset-like times."
    )
    parser.add_argument(
        "--observatory",'-o', type=str,
        help="The observatory to calculate at."
    )
    parser.add_argument(
        "--tz_print", "-t",default='observatory',
        help=("Name of timezone to print the times for (i.e., your own local timezone). Otherwise, will be observatory's timezone.")
    )
    args = parser.parse_args()

    astrotimes(args.observatory,tz_print=args.tz_print)
    

if __name__ == "__main__":
    main()