
"""
Binary Tree Mock Data Module
Provides example binary tree structures for testing and demonstration purposes.
Maximum depth: 6
"""


class Node:
    """Represents a single node in a binary tree."""

    def __init__(self, value, left=None, right=None):
        """
        Initialize a tree node.

        Args:
            value: The data stored in the node
            left: Left child node (default: None)
            right: Right child node (default: None)
        """
        self.value = value
        self.left = left
        self.right = right

    def __repr__(self):
        return f"Node({self.value})"


# Example 1: Balanced Binary Tree (depth = 4)
def create_balanced_tree():
    """
    Creates a balanced binary tree.

    Tree structure:
               1
             /   \
            2     3
           / \   / \
          4   5 6   7
         / \
        8   9
    """
    return Node(
        1,
        left=Node(
            2,
            left=Node(4, left=Node(8), right=Node(9)),
            right=Node(5)
        ),
        right=Node(
            3,
            left=Node(6),
            right=Node(7)
        )
    )


# Example 2: Left-skewed Tree (depth = 5)
def create_left_skewed_tree():
    """
    Creates a left-skewed binary tree where each node has only a left child.

    Tree structure:
        1
       /
      2
     /
    3
   /
  4
 /
5
    """
    return Node(
        1,
        left=Node(
            2,
            left=Node(
                3,
                left=Node(
                    4,
                    left=Node(5)
                )
            )
        )
    )


# Example 3: Right-skewed Tree (depth = 5)
def create_right_skewed_tree():
    """
    Creates a right-skewed binary tree where each node has only a right child.

    Tree structure:
    1
     \
      2
       \
        3
         \
          4
           \
            5
    """
    return Node(
        1,
        right=Node(
            2,
            right=Node(
                3,
                right=Node(
                    4,
                    right=Node(5)
                )
            )
        )
    )


# Example 4: Full Binary Tree (depth = 3)
def create_full_binary_tree():
    """
    Creates a full binary tree where every node has either 0 or 2 children.

    Tree structure:
           1
         /   \
        2     3
       / \   / \
      4   5 6   7
    """
    return Node(
        1,
        left=Node(2, left=Node(4), right=Node(5)),
        right=Node(3, left=Node(6), right=Node(7))
    )


# Example 5: Complex Tree with depth = 6
def create_complex_tree():
    """
    Creates a more complex binary tree with varying structure and depth = 6.

    Tree structure:
                  10
               /      \
              5        15
            /  \      /  \
           3    7   12    20
          / \  /   /  \    \
         1  4 6   11  13   25
                             /
                            24
    """
    return Node(
        10,
        left=Node(
            5,
            left=Node(3, left=Node(1), right=Node(4)),
            right=Node(7, left=Node(6))
        ),
        right=Node(
            15,
            left=Node(
                12,
                left=Node(11),
                right=Node(13)
            ),
            right=Node(
                20,
                right=Node(
                    25,
                    left=Node(24)
                )
            )
        )
    )


# Example 6: Sparse Tree (depth = 4)
def create_sparse_tree():
    """
    Creates a sparse binary tree with gaps in the structure.

    Tree structure:
        1
       /
      2
       \
        3
       /
      4
    """
    return Node(
        1,
        left=Node(
            2,
            right=Node(
                3,
                left=Node(4)
            )
        )
    )


# Dictionary for easy access to all mock trees
MOCK_TREES = {
    'balanced': create_balanced_tree,
    'left_skewed': create_left_skewed_tree,
    'right_skewed': create_right_skewed_tree,
    'full': create_full_binary_tree,
    'complex': create_complex_tree,
    'sparse': create_sparse_tree,
}


def get_tree(tree_name):
    """
    Get a mock tree by name.

    Args:
        tree_name (str): Name of the tree ('balanced', 'left_skewed', 'right_skewed',
                         'full', 'complex', 'sparse')

    Returns:
        Node: Root node of the requested tree

    Raises:
        ValueError: If tree_name is not recognized
    """
    if tree_name not in MOCK_TREES:
        raise ValueError(f"Unknown tree: {tree_name}. Available: {list(MOCK_TREES.keys())}")
    return MOCK_TREES[tree_name]()
