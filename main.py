# Install opencv-python library using pip
# pip install opencv-python

import cv2
from PIL import Image
import pytesseract
import pickle
from trie_tree import Trie

img_path = 'single_letter.jpg'

def postprocessing(image_path):

    # Load the image
    img = cv2.imread(image_path)

    # Convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to make the image binary
    _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

    # Display the modified image
    #cv2.imshow('Modified Image', binary)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()

    # Convert the binary image back to PIL format
    binary_pil = Image.fromarray(binary)
    return binary

def split_into_parts(img_path):
    
    img = cv2.imread(img_path)
    
    x = 190
    y = 1150
    width = 150;
    height = 150;
    
    for i in range(4):
        for j in range(4):
            cropped_img = img[y:y+height, x:x+width]
            # Convert the image to grayscale
            gray = cv2.cvtColor(cropped_img, cv2.COLOR_BGR2GRAY)
            # Apply thresholding to make the image binary
            _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            cv2.imwrite('cropped_image'+str(i)+str(j)+'.jpg', binary)
            x += 210
        y += 210
        x = 190

    # Display the cropped image (optional)
    #cv2.imshow('Cropped Image', cropped_img)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
split_into_parts("full.jpg")

letters = [["a", "a", "a", "a"], ["a", "a", "a", "a"], ["a", "a", "a", "a"], ["a", "a", "a", "a"]]

for i in range(4):
    for j in range(4):
        #print("i is: " + str(i) + " j is: " + str(j))
        #print("Image: cropped_image"+str(i)+str(j)+".jpg")
        letter = pytesseract.image_to_string(Image.open("cropped_image"+str(i)+str(j)+".jpg"), config=(" --psm 10"))
        #print(letter)
        letters[i][j] = letter
        
#print(letters)
 
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

# Function to find all possible words in the grid
def find_all_words(grid):
    found_words = set()  # Set to store found words
    visited = [[False] * len(grid[0]) for _ in range(len(grid))]  # 2D array to track visited cells
    
    # Traverse each cell in the grid
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            find_words(grid, visited, row, col, "", found_words)
    
    return found_words

# Example usage
grid = [
    ['d', 'o', 'g', 't'],
    ['d', 'b', 'f', 's'],
    ['e', 'n', 'a', 'r'],
    ['x', 'y', 'z', 'k']
]

# Load the word list or dictionary
f = open("word_list.txt", "r")
word_list = f.read().splitlines()
f.close()
#print("read the word list")
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

# Function to format words based on their length
def format_words_by_length(words):
    formatted_words = {}
    for word in words:
        word_length = len(word)
        if word_length not in formatted_words:
            formatted_words[word_length] = []
        formatted_words[word_length].append(word)
    return formatted_words

# Find all words in the grid
all_words = find_all_words(grid)

# Format the words by length
formatted_words = format_words_by_length(all_words)

# Print the formatted words
for length, words in formatted_words.items():
    print(f"Words of length {length}: {', '.join(words)}")

