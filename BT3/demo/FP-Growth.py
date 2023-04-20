from collections import defaultdict

class TreeNode:
    def __init__(self, item=None, count=0, parent=None):
        self.item = item
        self.count = count
        self.parent = parent
        self.children = {}

class FPTree:
    def __init__(self, transactions, min_support):
        self.min_support = min_support
        self.header_table = {}
        self.root = TreeNode()

        for transaction in transactions:
            filtered_transaction = [item for item in transaction if item in self.min_support]
            sorted_transaction = sorted(filtered_transaction, key=lambda x: self.min_support[x], reverse=True)
            self.insert_transaction(sorted_transaction)

    def insert_transaction(self, transaction):
        current_node = self.root
        for item in transaction:
            child_node = current_node.children.get(item)
            if not child_node:
                child_node = TreeNode(item, 1, current_node)
                current_node.children[item] = child_node
                if item in self.header_table:
                    self.header_table[item].append(child_node)
                else:
                    self.header_table[item] = [child_node]
            else:
                child_node.count += 1
            current_node = child_node

    def get_conditional_patterns(self, item):
        conditional_patterns = []
        nodes = self.header_table[item]
        for node in nodes:
            parent_items = []
            while node.parent.item is not None:
                parent_items.append(node.parent.item)
                node = node.parent
            if len(parent_items) > 0:
                conditional_patterns.append((parent_items[::-1], node.count))
        return conditional_patterns

def fp_growth(transactions, min_support):
    item_counts = defaultdict(int)
    for transaction in transactions:
        for item in transaction:
            item_counts[item] += 1

    frequent_items = {item: count for item, count in item_counts.items() if count >= min_support}
    sorted_frequent_items = sorted(frequent_items, key=frequent_items.get, reverse=True)

    fptree = FPTree(transactions, frequent_items)

    results = []

    for item in sorted_frequent_items:
        patterns = fptree.get_conditional_patterns(item)
        conditional_tree = FPTree([pattern[0] for pattern in patterns], frequent_items)
        if len(conditional_tree.root.children) > 0:
            subtree_results = fp_growth([pattern[0] for pattern in patterns], min_support)
            for result in subtree_results:
                result_list = list(result)
                result_list.insert(0, item)
                results.append(result_list)
        for pattern in patterns:
            #print(pattern)
            pattern = list(pattern)
            #pattern[0] = list(pattern[0])
            pattern[0].insert(0, item)
            results.append(pattern[0])

    return results


# Example usage

transactions = [['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
         ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
         ['b', 'f', 'h', 'j', 'o'],
         ['b', 'c', 'k', 's', 'p'],
         ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']]


min_support = 3

frequent_patterns = fp_growth(transactions, min_support)

print(frequent_patterns)