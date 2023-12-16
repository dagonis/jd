import argparse
import os

from core import JohnDecimal

def main() -> None:
    # Top level argument parser
    parser = argparse.ArgumentParser(description="JD Librarian - A command line tool for managing Johnny Decimal libraries!")
    parser.add_argument("--jd_root", 
                        help="The root of the Johnny Decimal library. This is can also be set with the environment variable JD_ROOT", 
                        default=os.getenv("JD_ROOT", "~/jd"))
    subparsers = parser.add_subparsers(help="Johnny Decimal command help")
    # Subparser for searching JD
    search_parser = subparsers.add_parser("search", help="Search Johnny Decimal")
    search_parser.add_argument("search_term", help="The search term to use")
    # search_parser.add_parser("search_term", help="The search term to use")
    args = parser.parse_args()
    print(args)
    jd = JohnDecimal(args.jd_root)
    if hasattr(args, 'search_term'):
        print(jd.search_johnny_decimal_category(args.search_term))
    else:
        print(jd)
    print("Areas")
    for area in jd.areas:
        print(area.name)
    print("Categories")
    for category in jd.categories:
        print(category.name)


if __name__ == '__main__':
    main()