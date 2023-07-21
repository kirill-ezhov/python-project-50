#!/usr/bin/env python3
import argparse

def main():
    parser = argparse.ArgumentParser(description='Compares two configuration files and shows a difference.')
    parser.add_argument('first_file')
    parser.add_argument('second_file')
    parser.add_argument('-f', '--format', metavar='FORMAT',
                        help = 'set format of output')
    return parser

if __name__ == "__main__":
    parser = main()
    args = parser.parse_args()

    parser.print_help()
