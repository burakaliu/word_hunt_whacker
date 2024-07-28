
from collections import defaultdict
import time
import cv2
from PIL import Image
import pytesseract
import pickle
from trie_tree import Trie
import screenshotter
import img_processing
import matplotlib.pyplot as plt
import numpy as np


startTime = time.time()
letters = img_processing.img_complete_processing()
endTime = time.time()
print("Time taken: " + str(endTime - startTime) + " seconds")

startTime = time.time()
print(letters)
 
# Define the grid traversal directions for a 4x4 grid
directions = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]

# Function to recursively find words starting from a given position
def find_words(grid, visited, row, col, current_word, found_words):
    # Mark the current cell as visited
    visited[row][col] = True
    
    # Append the letter of the current cell to the current word
    current_word += grid[row][col]
    
    # Check if the current word is a valid prefix
    '''
    if not trie.prefix_search(current_word.lower()):
        # If the current prefix is not a valid prefix of any word, stop searching further
        return
    '''
    # Check if the current word is a valid word
    if trie.search(current_word.lower()):
        # Add the current word to the list of found words
        found_words.add(current_word)
    
    # Recursively explore neighboring cells
    for dr, dc in directions:
        new_row, new_col = row + dr, col + dc
        if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]) and not visited[new_row][new_col]:
            find_words(grid, visited, new_row, new_col, current_word, found_words)
    
    # Backtrack: mark the current cell as unvisited
    visited[row][col] = False

# Placeholder function for finding all words with their paths
def find_all_words_with_paths(grid):
    words_with_paths = []

    def is_valid(x, y, visited):
        return 0 <= x < len(grid) and 0 <= y < len(grid[0]) and (x, y) not in visited

    def dfs(x, y, visited, path, current_word):
        visited.add((x, y))
        path.append((x, y))
        current_word += grid[x][y]

        if trie.search(current_word):  # Assuming you have a Trie to check valid words
            words_with_paths.append((current_word, list(path)))

        for dx, dy in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            nx, ny = x + dx, y + dy
            if is_valid(nx, ny, visited):
                dfs(nx, ny, visited, path, current_word)

        visited.remove((x, y))
        path.pop()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            dfs(i, j, set(), [], "")

    return words_with_paths

# Example usage
grid = [
    ['d', 'o', 'g', 't'],
    ['d', 'b', 'f', 's'],
    ['e', 'n', 'a', 'r'],
    ['x', 'y', 'z', 'k']
]


# Function to visualize the path on the grid using matplotlib
def visualize_path_with_matplotlib(grid, path, word):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()
    ax.set_xticks(np.arange(len(grid[0])+1)-0.5, minor=True)
    ax.set_yticks(np.arange(len(grid)+1)-0.5, minor=True)
    ax.grid(which='minor', color='gray', linestyle='-', linewidth=2)
    ax.tick_params(which='minor', size=0)
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            ax.text(j, i, grid[i][j], ha='center', va='center', fontsize=20,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))

    x_coords = [y for x, y in path]
    y_coords = [x for x, y in path]
    
    # Plot the path
    ax.plot(x_coords, y_coords, 'ro-', linewidth=2, markersize=12)
    
    # Highlight the starting point
    ax.plot(x_coords[0], y_coords[0], 'go', markersize=14, markeredgewidth=2, markeredgecolor='black')  # Green circle for start
    ax.text(x_coords[0], y_coords[0], grid[y_coords[0]][x_coords[0]], ha='center', va='center', fontsize=20,
                    bbox=dict(facecolor='green', edgecolor='black', boxstyle='round,pad=0.5'))


    ax.set_xlim(-0.5, len(grid[0]) - 0.5)
    ax.set_ylim(-0.5, len(grid) - 0.5)
    ax.set_aspect('equal')
    ax.invert_yaxis() 
    
    # Add a separate axis for the caption above the grid
    caption_ax = fig.add_axes([0.5, 0.95, 0.1, 0.05])  # [left, bottom, width, height]
    caption_ax.text(0.5, 0.5, word, ha='center', va='center', fontsize=18,
                    bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.5'))
    caption_ax.axis('off')  # Hide the axis

    plt.draw()  # Draw the plot
    print("Press Enter to continue...")
    plt.waitforbuttonpress()  # Wait for user to press a key
    plt.close(fig)  # Close the figure after key press

'''
# Create a trie object
trie = Trie()
# Insert all words from the word list into the trie
for word in word_list:
    trie.insert(word.lower())
print("Words from the list added to the trie")
trie.save_trie("trie_tree.pkl")
print("trie tree saved in file")
'''
# Load trie from file
trie = Trie.load_trie("trie_tree.pkl")
#print(trie.search("app"))  # True
#print(trie.search("apl"))  # False
#print(trie.prefix_search("app"))  # ["app", "ape"]

# Function to mark and visualize the path on the grid
def visualize_path(grid, path):
    # Create a copy of the grid to mark the path
    visual_grid = [row[:] for row in grid]
    
    # Mark the path with a special character, e.g., '*'
    for (x, y) in path:
        visual_grid[x][y] = f'*{visual_grid[x][y].upper()}'
    
    # Print the visual grid
    for row in visual_grid:
        print(' '.join(row))
    print()

# Function to format words and paths based on their length
def format_words_by_length(words_with_paths):
    formatted_words = defaultdict(list)
    for word, path in words_with_paths:
        if len(word) >= 3:  # Only include words with 3 or more letters
            formatted_words[len(word)].append((word, path))
    return formatted_words

# Find all words in the grid with their paths
all_words_with_paths = find_all_words_with_paths(letters)

# Format the words by length
formatted_words = format_words_by_length(all_words_with_paths)

endTime = time.time()
print("Time taken: " + str(endTime - startTime) + " seconds")

# Sort the keys (word lengths) and print the formatted words with their paths
for length in sorted(formatted_words.keys(), reverse=True):
    words_and_paths = formatted_words[length]
    print(f"Words of length {length}:")
    for word, path in words_and_paths:
        print(f"  {word}:")
        visualize_path_with_matplotlib(letters, path, word)
    
