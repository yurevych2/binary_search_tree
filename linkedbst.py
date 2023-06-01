"""
File: linkedbst.py
Author: Ken Lambert
"""

from random import randint
import timeit
from collections import deque
from sys import setrecursionlimit

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from linkedqueue import LinkedQueue
from math import log


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            string = ""
            if node != None:
                string += recurse(node.right, level + 1)
                string += "| " * level
                string += str(node.data) + "\n"
                string += recurse(node.left, level + 1)
            return string

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def lift_max_in_left_subtree_to_top(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right == None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node == None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed == None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left == None \
                and not current_node.right == None:
            lift_max_in_left_subtree_to_top(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left == None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top: root of subtree.
            :return:
            '''
            if not 'left' in dir(top): # leaf  not (top.left or top.right)
                return 0
            else:
                return 1 + max(height1(top.left), height1(top.right))

        top = self._root
        return height1(top) - 1

    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        nothing = 0
        for _ in self:
            nothing += 1

        if self.height() < 2 * log(nothing + 1, 2) - 1:
            return True

        return False

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        result = []

        for node in self:
            if low <= node <= high:
                result.append(node)

        return sorted(result)

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def build_subtree(lst: list, root=None):
            if root is None:
                self._root = BSTNode(lst[len(lst) // 2])
                root = self._root

            if len(lst) > 3:
                left_lst = lst[:len(lst) // 2]
                right_lst = lst[len(lst) // 2 + 1:]

                root.left = BSTNode(left_lst[len(left_lst) // 2])
                root.right = BSTNode(right_lst[len(right_lst) // 2])

                build_subtree(left_lst, root.left)
                build_subtree(right_lst, root.right)
            else:
                if not len(lst) == 1:
                    root.left = BSTNode(lst[0])

                if len(lst) == 3:
                    root.right = BSTNode(lst[-1])

        nodes = sorted([node for node in self.inorder()])
        self._root = None

        build_subtree(nodes)

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        smallest = item
        for node in self:
            if node > item:
                if not smallest == item:
                    smallest = min(smallest, node)
                else:
                    smallest = node

        if smallest == item:
            return None

        return smallest

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        biggest = None
        for node in self:
            if not biggest and node != item and node < item:
                biggest = node

            if not biggest is None and node < item:
                biggest = max(biggest, node)

        return biggest

    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """
        def bfs(tree, item):
            if tree._root is None:
                return []

            result = []
            queue = deque()
            queue.append(tree._root)

            while queue:
                node = queue.popleft()
                if node.data == item:
                    return node, node.data
                result.append(node.data)

                if node.left:
                    queue.append(node.left)
                if node.right:
                    queue.append(node.right)

        words = []
        self._root = None
        self.height = 0
        with open(path, 'r') as file:
            for line in file.readlines():
                for word in line.split():
                    self.add(word)
                    words.append(word)

                if len(words) > 10000:
                    print('10000 words')
                    break
        
        sorted_words = sorted(words)

        rand_word = words[randint(0, 9999)]

        start_time = timeit.default_timer()
        sorted_words.index(rand_word)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        print(f'list.index() in an unsorted list: {elapsed_time}\n')

        start_time = timeit.default_timer()
        bfs(self, rand_word)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        print(f'BFS in LinkedBST (words added in a row): {elapsed_time}\n')

        self._root = None
        self.height = 0
        for word in sorted_words:
            self.add(word)
        start_time = timeit.default_timer()
        bfs(self, rand_word)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        print(f'BFS in LinkedBST (words added from a sorted list): {elapsed_time}\n')

        self.rebalance()
        start_time = timeit.default_timer()
        bfs(self, rand_word)
        end_time = timeit.default_timer()
        elapsed_time = end_time - start_time
        print(f'BFS in LinkedBST (rebalanced tree): {elapsed_time}\n')


if __name__ == '__main__':
    setrecursionlimit(10000)
    tree = LinkedBST()

    tree.demo_bst('words.txt')
