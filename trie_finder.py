
# Load the word list or dictionary
f = open("word_list.txt", "r")
word_list = f.read().splitlines()
f.close()
print("read the word list")

# Define the grid traversal directions
directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

    def contains_key(self, char):
        return char in self.children

def build_trie(word_list):
    root = TrieNode()
    for word in word_list:
        node = root
        for char in word:
            if not node.contains_key(char):
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    return root


def find_words(grid, row, col, trie_node, current_word, found_words, visited):
    visited[row][col] = True
    if trie_node.is_end_of_word:
        found_words.add(current_word)
        print("Found word:", current_word)

    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and not visited[new_row][new_col]:
            char = grid[new_row][new_col]
            if char in trie_node.children:
                new_word = current_word + char  # Create a new copy of current_word for this recursive call
                find_words(grid, new_row, new_col, trie_node.children[char], new_word, found_words, visited)

    visited[row][col] = False




def find_all_words(grid, root):
    found_words = set()
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            find_words(grid, row, col, root, "", found_words, visited)
    return found_words

# Example usage
grid = [
    ['d', 'o', 'g'],
    ['d', 'b', 'f'],
    ['e', 'n', 'a']
]

root = build_trie(word_list)
all_words = find_all_words(grid, root)
print(all_words)
