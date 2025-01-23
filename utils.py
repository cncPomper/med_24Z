from itertools import chain, combinations
from collections import defaultdict
from csv import reader


# chain('ABC', 'DEF') → A B C D E F
# combinations('ABCD', 2) → AB AC AD BC BD CD
# combinations(range(4), 3) → 012 013 023 123


def get_from_file(fname="data/tesco.csv"):
    itemSets = []

    with open(fname, "r") as file:
        csv_reader = reader(file)
        for line in csv_reader:
            line = list(filter(None, line))
            record = set(line)
            itemSets.append(record)
    return itemSets


def power_set(set_):
    """
    Generates the power set of the input set `s`, excluding the empty set
    and including all non-empty subsets.

    Args:
        s (iterable): An iterable representing the original set.

    Returns:
        iterator: An iterator over all non-empty subsets of `set_` as tuples.
    """
    return chain.from_iterable(combinations(set_, r) for r in range(1, len(set_)))


def get_union(items_set, len_):
    """
    Generates a set of unions of pairs of sets from the input set,
    where the size of the resulting union matches the specified length.

    Args:
        items_set (set of frozenset): A set of frozensets to combine.
        len_ (int): The desired length of the union sets.

    Returns:
        set of frozenset: A set containing unions of pairs of sets from `items_set`
                          that have exactly `len_` elements.
    """
    return set(
        [i.union(j) for i in items_set for j in items_set if len(i.union(j)) == len_]
    )


def prunning(candidate_set, previous_frequent_set, len_):
    """
    Filters a candidate set by removing items that contain subsets
    not present in the previous frequent set.

    Args:
        candidate_set (set of frozenset): A set of candidate itemsets to be pruned.
        previous_frequent_set (set of frozenset): A set of previously identified frequent itemsets.
        len_ (int): The length of the subsets to consider for pruning.

    Returns:
        set of frozenset: A pruned set of candidate itemsets where all subsets of size `len_`
                          are present in the `previous_frequent_set`.
    """
    temporary_candidate_set = candidate_set.copy()

    for item in candidate_set:
        sub_sets = combinations(item, len_)

        for sub_set in sub_sets:
            if frozenset(sub_set) not in previous_frequent_set:
                temporary_candidate_set.remove(item)
                break

    return temporary_candidate_set


def get_above_minimum_support(
    item_set,
    items_set_list,
    minimum_support,
    globally_item_set_with_support,
):
    """
    Identifies the frequent itemsets from a candidate set that meet or exceed the minimum support threshold.

    Args:
        item_set (set of frozenset): A set of candidate itemsets to evaluate.
        items_set_list (set of frozenset): A collection of transaction sets.
        minimum_support (int): The minimum support threshold for an itemset to be considered frequent.
        globally_item_set_with_support (dict): A dictionary for global support counts of itemsets.

    Returns:
        set of frozenset: A set of itemsets from `item_set` that meet the minimum support threshold.
    """
    # print(item_set,
    # items_set_list,
    # minimum_support)
    # print(item_set, items_set_list, minimum_support, globally_item_set_with_support)
    frequent_set = set()
    local_item_set_with_support = defaultdict(int)

    for item in item_set:
        for item_s in items_set_list:
            if item.issubset(item_s):
                globally_item_set_with_support[item] += 1
                local_item_set_with_support[item] += 1

    for item, suport_count in local_item_set_with_support.items():
        support = float(suport_count / len(items_set_list))

        if support >= minimum_support:
            frequent_set.add(item)

    return frequent_set


def association_rule(freq_item_set, item_set_with_support, minimun_confidence):
    """
    Generates association rules from frequent itemsets based on a minimum confidence threshold.

    Args:
        freq_item_set (dict): A dictionary where keys are the sizes of itemsets (int)
                              and values are sets of frequent itemsets of that size (set of frozenset).
        item_set_with_support (dict): A dictionary mapping itemsets (frozenset) to their support counts (int).
        minimum_confidence (float): The minimum confidence threshold for generating rules.

    Returns:
        list: A list of association rules, where each rule is represented as
              [antecedent (set), consequent (set), confidence (float)].
    """
    rules = []

    for k, item_set in freq_item_set.items():
        # print(freq_item_set)
        for item in item_set:
            sub_sets = power_set(item)

            for s in sub_sets:
                confidence = (
                    item_set_with_support[item] / item_set_with_support[frozenset(s)]
                )

                if confidence >= minimun_confidence:
                    rules.append([set(s), set(item.difference(s)), confidence])

    return rules


def get_item_set_from_list(items_set_list):
    """
    Converts a list of sets containing items into a set of frozensets,
    where each frozenset contains a single item from the original sets.

    Args:
        items_set_list (list of set): A list of sets, where each set contains multiple items.

    Returns:
        set of frozenset: A set of frozensets, where each frozenset contains one item
                          from the original sets in `items_set_list`.
    """
    temporary_set = set()

    for items_set in items_set_list:
        # print(items_set)
        for item in items_set:
            # print(item)
            temporary_set.add(frozenset([item]))
    # print(temporary_set)
    return temporary_set
