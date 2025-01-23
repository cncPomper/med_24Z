import numpy as np
from utils import *


def apriori_(item_set_list, min_support, min_confident):
    """
    Implements the Apriori algorithm for frequent itemset generation and association rule mining.

    Args:
        item_set_list : list of lists
            A list where each element is a transaction represented as a list of items.
        min_support : float
            Minimum support threshold for an itemset to be considered frequent.
        min_confident : float
            Minimum confidence threshold for an association rule to be generated.

    Returns:
        global_freq_item_set : dict
            A dictionary where the keys are the size of the itemsets (e.g., 1, 2, 3, ...) and the values are sets of frequent itemsets of that size.
        rules : list of tuples
    """
    # print(item_set_list, min_support, min_confident)
    # item_set_list = item_set_list[:100]

    frozen_item_set = get_item_set_from_list(item_set_list)
    # print(frozen_item_set)
    # Final result global frequent itemset
    global_freq_item_set = dict()
    # Storing global itemset with support count
    global_set_item_support = defaultdict(int)

    current_set = get_above_minimum_support(
        frozen_item_set, item_set_list, min_support, global_set_item_support
    )

    # print(current_set)
    k = 2
    # Calculating frequent item set
    while current_set:
        # Storing frequent itemset
        global_freq_item_set[k - 1] = current_set
        # Self-joining Lk
        candidate_set = get_union(current_set, k)
        # Perform subset testing and remove pruned supersets
        candidate_set = prunning(candidate_set, current_set, k - 1)
        # Scanning itemSet for counting support
        current_set = get_above_minimum_support(
            candidate_set, item_set_list, min_support, global_set_item_support
        )
        k += 1

    rules = association_rule(
        global_freq_item_set, global_set_item_support, min_confident
    )
    rules.sort(key=lambda x: x[2])

    return global_freq_item_set, rules


def wrapper_appriori(df_path, min_support, min_confident):
    """
    Wrapper function to load dataset and execute the Apriori algorithm.

    Args:
        df_path : str
            Path to the file containing the dataset. The file should be a binary file
            containing a pickled list of transactions (list of lists).
        min_support : float
            Minimum support threshold for an itemset to be considered frequent.
        min_confident : float
            Minimum confidence threshold for an association rule to be generated.

    Returns:
        global_freq_item_set : dict
            A dictionary where the keys are the size of the itemsets (e.g., 1, 2, 3, ...) and the values are sets of frequent itemsets of that size.
        rules : list of tuples
    """

    if df_path.endswith('csv'):
        item_set_list = get_from_file(df_path)
    else:
        with open(df_path, "rb") as f:
            item_set_list = np.load(f, allow_pickle=True)
        # print(item_set_list[:5])

    # print(item_set_list[:10], min_support, min_confident)
    # print(item_set_list)
    global_freq_item_set, rules = apriori_(item_set_list, min_support, min_confident)
    return global_freq_item_set, rules
