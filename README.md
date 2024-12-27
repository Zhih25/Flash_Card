# Vocabulary Flashcards 
## Overview
The Vocabulary Flashcards program is an interactive flashcard application built using Python's tkinter library. It allows users to study vocabulary from markdown files, track mistakes, and review them to improve retention. The system supports vocabulary sets in markdown format and lets users keep track of their progress with a review system that updates the mistake counts.

## Features
Vocabulary Flashcards: Display vocabulary words and their translations in a flashcard format.
Review System: Tracks vocabulary words the user struggles with and allows for focused review of those words.
File Handling: Load vocabulary sets from markdown files (.md) and save mistakes to a new file.
Mistake Buffer: Automatically updates the count of mistakes made for each word and saves it to a markdown file for future review.
Interactive Interface: Provides a graphical user interface (GUI) for easy interaction with the flashcards, including buttons for navigation.

## Requirements
- Python3
- Tkinter (usually included in Python standard library)

## Installation
Ensure Python 3.x is installed on your system.
Clone the repository or download the file directly.

```
$ git clone https://github.com/Zhih25/Flash_Card.git
```

Install any required dependencies (tkinter is typically included with Python, but you can install it manually if needed).
Run the Python script to launch the application:

``` 
#!/bin/bash
python3 flash_card.py
```
## Key Bindings
- **Up Arrow**: Mark word as known (Review mode only).
- **Down Arrow**: Mark word as unknown (Moves to mistake set).
- **Enter**: Show translation or move to the next card.
  
## Usage Instructions

### 1. Load Vocabulary Set
- Choose a vocabulary set from available markdown files in the current directory.

### 2. Study Vocabulary
- Flashcards are shown with vocabulary words. Press **Up** if you know the word or **Down** if you don't.
- Press **Enter** to show the translation and again to skip to the next card.

### 3. Review Mode
- Words marked as mistakes are reviewed based on how often they've been forgotten.
- Mistakes are logged and saved to a separate file once a threshold (default 10) is reached.

### 4. Error Handling
- If the markdown file is malformed or empty, an error message will be shown.

### 5. Managing Mistakes
- Mistakes are logged and stored in a separate file named `<original_file_name>_mistakes.md`.

### 6. Main Menu
- Click the "Main Menu" button to return to the main menu at any time.

## File Format
Each vocabulary set is a markdown file with the following structure:


    ```
    | Word | Translation | Times |
    | ---- | ----------- | ----- |
    | Word1 | Translation1 | 0     |
    | Word2 | Translation2 | 1     |
    ```
- The first column is the vocabulary word.

- The second column is the translation.

- The third column is the number of times the word has been encountered as ~a mistake (this is used in the review system).

## Customization
- Adjust mistake weights with `probability_weight` (default: [0.1, 0.2, 0.3, 0.4]).
- Set mistake buffer length with `buffer_length` (default: 10).
Example Markdown File
Here’s an example of a correctly formatted markdown file for vocabulary:
For those format only with Word and Translation are also supported. The Times column will be automatically count as 0, and will automatically update in the review mode.


    ```
    | Word       | Translation    | Times |
    |------------|----------------|-------|
    | Bonjour    | Hello          | 0     |
    | Merci      | Thank you      | 0     |
    | Chat       | Cat            | 0     |
    ```
This file can be used to create flashcards with words and translations.

