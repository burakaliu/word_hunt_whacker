import pickle

class TrieNode:
    def __init__(self):
        self.children = {}  # Dictionary to store child nodes
        self.is_end_of_word = False  # Flag to indicate end of word

class Trie:
    def __init__(self):
        self.root = TrieNode()  # Create the root node

    def insert(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                current_node.children[char] = TrieNode()
            current_node = current_node.children[char]
        current_node.is_end_of_word = True  # Mark the end of the word

    def search(self, word):
        current_node = self.root
        for char in word:
            if char not in current_node.children:
                return False  # Word not found
            current_node = current_node.children[char]
        return current_node.is_end_of_word  # Return True if word found and marked as end

    def prefix_search(self, prefix):
        current_node = self.root
        for char in prefix:
            if char not in current_node.children:
                return []  # No words with the given prefix
            current_node = current_node.children[char]
        # Explore all paths starting from the current node (words with the given prefix)
        all_words = []
        self._dfs(current_node, prefix, all_words)  # Use DFS to traverse all paths
        return all_words

    def _dfs(self, node, current_word, all_words):
        if node.is_end_of_word:
            all_words.append(current_word)  # Add the complete word

        for char, child in node.children.items():
            self._dfs(child, current_word + char, all_words)  # Explore child nodes
            
    def save_trie(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.root, file)

    @staticmethod
    def load_trie(filename):
        trie = Trie()
        with open(filename, 'rb') as file:
            trie.root = pickle.load(file)
        return trie

