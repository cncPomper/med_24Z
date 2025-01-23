from apriori import *
import argparse
from time import time
from utils import *

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "-f",
        "--input-file",
        dest="input_file",
        help="filename",
        default="data/tesco.csv",
    )

    parser.add_argument(
        "-s",
        "--min-support",
        dest="min_support",
        help="Min support (float)",
        default=0.5,
        type=float,
    )

    parser.add_argument(
        "-c",
        "--min-confident",
        dest="min_confident",
        help="Min confident (float)",
        default=0.5,
        type=float,
    )

    args = parser.parse_args()

    start = time()
    global_freq_item_set, rules = wrapper_appriori(
        df_path=args.input_file,
        min_support=args.min_support,
        min_confident=args.min_confident,
    )
    end = time()
    print(global_freq_item_set)
    print()
    print(f"{end - start} s")
    print()
    print(rules)
