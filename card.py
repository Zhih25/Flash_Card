import tkinter as tk
import os
import random

# 初始化全域變數
word_list = []
current_card = {}
current_file = ""
showing_translation = False  
mistake_buffer = {}  
file_name = ""

# 解析 Markdown 文件
def parse_md_file(filename):
    words = []
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if line.strip() == "" or line.startswith("|---"):
                    continue
                if "|" in line:  # 只處理表格格式的行
                    columns = line.strip().split("|")
                    if len(columns) >= 3:
                        word = columns[1].strip()  # 第一欄為單字
                        translation = columns[2].strip()  # 第二欄為翻譯
                        words.append({"word": word, "translation": translation})
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
    return words

# 顯示單字本選擇畫面
def show_main_menu():
    clear_window()
    root.bind("<Escape>", lambda event: None)
    tk.Label(root, text="Choose Vocabulary", font=("Arial", 18), bg="lightgray", fg="black").pack(pady=20)

    files = [f for f in os.listdir() if f.endswith(".md")]
    for file in files:
        tk.Button(root, text=file, font=("Arial", 14), bg="lightgray", fg="black",
                  command=lambda f=file: load_wordbook(f)).pack(pady=5)

# 載入選定的單字本
def load_wordbook(filename):
    global word_list, current_file, file_name 
    file_name=filename[:-3]
    word_list = parse_md_file(filename)
    current_file = filename
    if word_list:
        show_flashcard()
    else:
        tk.Label(root, text="Empty Vocabulary or Error Format!", font=("Arial", 14), bg="black", fg="red").pack(pady=10)

# 顯示單字卡畫面
def show_flashcard():
    clear_window()
    global current_card, showing_translation
    showing_translation = False

    if not word_list:
        show_main_menu()
        return

    current_card = random.choice(word_list)
    global word_label, translation_label

    word_label = tk.Label(root, text=current_card["word"], font=("Arial", 24), bg="black", fg="white",
                          wraplength=700, justify="center")
    word_label.pack(pady=20)

    translation_label = tk.Label(root, text="", font=("Arial", 18), bg="black", fg="white")
    translation_label.pack(pady=10)

    root.bind("<space>", add_to_mistake_buffer)
    root.bind("<Escape>", lambda event: show_main_menu())
    root.bind("<Return>", toggle_translation_or_next)

# 切換顯示翻譯或下一張
def toggle_translation_or_next(event=None):
    global showing_translation, translation_label, current_card
    if showing_translation:
        show_flashcard()
    else:
        translation_label.config(text=current_card["translation"])
        showing_translation = True

# 新增至緩衝區
def add_to_mistake_buffer(event=None):
    global mistake_buffer
    word = current_card["word"]
    translation = current_card["translation"]

    if word not in mistake_buffer:
        mistake_buffer[word] = translation

    if len(mistake_buffer) >= 5:
        update_mistake_file()
    
    show_flashcard()

# 更新錯題集文件
def update_mistake_file():
    global mistake_buffer, file_name
    mistake_file = file_name+"_mistakes.md"

    existing_words = set()
    if not os.path.exists(mistake_file):
        with open(mistake_file, "w", encoding="utf-8") as file:
            file.write("| Word | Translation |\n")
            file.write("| --- | --- |\n")
    if os.path.exists(mistake_file):
        with open(mistake_file, "r", encoding="utf-8") as file:
            for line in file:
                if "|" in line:
                    columns = line.strip().split("|")
                    if len(columns) >= 3:
                        existing_words.add(columns[1].strip())

    with open(mistake_file, "a", encoding="utf-8") as file:
        for word, translation in mistake_buffer.items():
            if word not in existing_words:
                file.write(f"| {word} | {translation} |\n")

    mistake_buffer.clear()

# 清除目前畫面
def clear_window():
    for widget in root.winfo_children():
        widget.destroy()

# 建立主視窗
root = tk.Tk()
root.title("Card")
root.geometry("800x400")
root.config(bg="black")

# 顯示主選單
show_main_menu()

# 啟動主迴圈
root.mainloop()
