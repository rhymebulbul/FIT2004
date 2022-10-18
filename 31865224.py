"""
Monash University
FIT2004 - Algorithms and Data Structures
Assignment 3

Rhyme Bulbul
31865224

References:
    1.
"""
import math


class Node:
    def __init__(self, height=0):
        self.children = [None] * 29
        self.height = height


class Trie:
    def __init__(self, original_string):
        self.root = Node()
        self.total = original_string

    def insert(self, suffix):
        word = self.root

        for each_character in range(len(suffix)):
            index = ord(suffix[each_character]) - ord('a')

            if word.children[index] is None:
                word.children[index] = Node(each_character)

            # TODO: compress trie add indices
            word = word.children[index]








def build_suffix(submission1, submission2):
    total = submission1 + '{' + submission2 + '}'
    total = total.replace(' ', '|')
    x = Trie(total)
    for i in range(len(total)):
        x.insert(total[i:])
        # x.insert(i, len(total))
    return x


def compute(suffix_tree):
    current_node = suffix_tree.root
    counter = 0
    end = ord('}') - ord('a')
    for child in range(len(current_node.children)):
        if current_node.children[child] is not None:

            current_node = child
            if child == end:
                pass


    return "somesti"


def compare_subs(submission1, submission2):
    longest_common_substring = max(submission1, submission2)

    if len(submission1) == 1:
        for char in submission2:
            if char == submission1:
                longest_common_substring = submission1
    elif len(submission2) == 1:
        for char in submission1:
            if char == submission2:
                longest_common_substring = submission2
    elif len(submission2) == len(submission1):
        flag = False
        for i in range(len(submission1)):
            if submission1[i] != submission2[i]:
                flag = False
        if flag:
            longest_common_substring = submission1
    else:
        suffix_tree = build_suffix(submission1, submission2)
        longest_common_substring = compute(suffix_tree)

    one = math.floor(100 * len(longest_common_substring) / len(submission1))
    two = math.floor(100 * len(longest_common_substring) / len(submission2))

    return [longest_common_substring, one, two]


if __name__ == '__main__':
    """
    Example 1
    """
    submission1 = 'the quick brown fox jumped over the lazy dog'
    submission2 = 'my lazy dog has eaten my homework'
    print(compare_subs(submission1, submission2))
    expected = [' lazy dog', 20, 27]

    print(compare_subs('d', 'fakdlmg'))
    print(compare_subs('fakdlmg', 'k'))
    print(compare_subs('fakdlmg', 'fakdlmg'))

    """
    Example 2
    """
    # # submission1 = "radix sort and counting sort are both non comparison sorting algorithms"
    # # submission2 = "counting sort and radix sort are both non comparison sorting algorithms"
    # # print(compare_subs(submission1, submission2))
    # # print([" sort are both non comparison sorting algorithms", 68, 68])
