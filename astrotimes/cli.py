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
    parser.add_argument(
        "--date","-d",default='today',help=('Date to calculate times for. Defaults to the closest midnight from time run in users local time. Enter in YYYY-MM-DD')
    )
    args = parser.parse_args()

    astrotimes(args.observatory,tz_print=args.tz_print,date=args.date)
    

if __name__ == "__main__":
    main()