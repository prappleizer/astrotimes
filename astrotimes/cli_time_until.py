"""
The command-line interface for the tool.
"""
import argparse
from astrotimes import astrotimes,time_until

def main():
    parser = argparse.ArgumentParser(
        description="A simple CLI tool for printing sunset-like times."
    )
    parser.add_argument(
        "--observatory",'-o', type=str,
        help="The observatory to calculate at."
    )
   
    args = parser.parse_args()

    time_until(args.observatory)
    

if __name__ == "__main__":
    main()