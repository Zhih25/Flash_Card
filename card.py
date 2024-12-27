import tkinter as tk
import os
import random
import re

class VocabularySystem:
    def __init__(self, root):
        self.root = root                         #window object
        self.root.title("Vocabulary Flashcards") #window title
        self.root.geometry("800x400")            #window size
        self.root.config(bg="black")             #window background color

        # state variables
        self.word_list = []
        self.current_card = {}
        self.current_file = ""
        self.showing_translation = False
        self.mistake_buffer = {}
        self.mistake_buffer_ch = {}
        self.file_name = ""
        self.is_in_review = False
        self.buffer_length = 1

        # initial setup
        self.show_main_menu()

    # parse markdown file
    def parse_md_file(self, filename):
        words = []
        self.is_in_review = bool(re.search(r'_mistakes\.md$', filename))
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()[2:]
                for line in lines:
                    if line.strip() == "" or line.startswith("| -") or line.startswith("#"):
                        continue
                    if "|" in line:
                        columns = line.strip().split("|")
                        if len(columns) >= 3:
                            word = columns[1].strip()
                            translation = columns[2].strip()
                            times=0
                            if len(columns)==4:
                                times=columns[3].strip()
                            words.append({"word": word, "translation": translation, "times":times})
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
        return words

    # 清除目前畫面
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # 顯示單字本選擇畫面
    def show_main_menu(self):
        self.clear_window()
        self.root.bind("<Escape>", lambda event: None)
        tk.Label(self.root, text="Choose Vocabulary", font=("Arial", 18), bg="lightgray", fg="black").pack(pady=20)

        files = [f for f in os.listdir() if f.endswith(".md")]
        for file in files:
            tk.Button(
                self.root,
                text=file,
                font=("Arial", 14),
                bg="lightgray",
                fg="black",
                command=lambda f=file: self.load_wordbook(f)
            ).pack(pady=5)

    # load corresponding wordbook
    def load_wordbook(self, filename):
        self.file_name = filename[:-3]
        self.word_list = self.parse_md_file(filename)
        self.current_file = filename
        if self.word_list:
            self.show_flashcard()

        else:
            tk.Label(
                self.root,
                text="Empty Vocabulary or Error Format!",
                font=("Arial", 14),
                bg="black",
                fg="red"
            ).pack(pady=10)

    #show flashcard
    def show_flashcard(self):
        self.clear_window()
        self.showing_translation = False

        if not self.word_list:
            self.show_main_menu()
            return

        self.current_card = random.choice(self.word_list)
        self.word_label = tk.Label(
            self.root,
            text=self.current_card["word"],
            font=("Arial", 24),
            bg="black",
            fg="white",
            wraplength=700,
            justify="center"
        )
        self.word_label.pack(pady=20)

        self.translation_label = tk.Label(
            self.root,
            text="",
            font=("Arial", 18),
            bg="black",
            fg="white"
        )
        self.translation_label.pack(pady=10)
        if self.is_in_review:
            self.root.bind("<Up>",lambda event: self.update_buffer(False, event))
            self.root.bind("<Down>",lambda event: self.update_buffer(True, event))
            self.root.bind("<Escape>", lambda event: self.show_main_menu())
            self.root.bind("<Return>", self.toggle_translation_or_next)
        else:
            self.root.bind("<Down>",lambda event: self.update_buffer(True, event))
            self.root.bind("<Escape>", lambda event: self.show_main_menu())
            self.root.bind("<Return>", self.toggle_translation_or_next)

    # 切換顯示翻譯或下一張
    def toggle_translation_or_next(self, event=None):
        if self.showing_translation:
            self.show_flashcard()
        else:
            self.translation_label.config(text=self.current_card["translation"])
            self.showing_translation = True

    # add to mistake times
    def update_buffer(self,ans, event=None):
        word = self.current_card["word"]
        self.mistake_buffer_ch[word] = self.current_card["translation"]
        if word not in self.mistake_buffer:
            self.mistake_buffer[word] = 1* (1 if ans else -1)
        else:
            self.mistake_buffer[word] += 1 * (1 if ans else -1)

        if len(self.mistake_buffer) >= self.buffer_length:
            self.update_mistake_file()

        self.show_flashcard()


    # 更新錯題集文件
    def update_mistake_file(self):
        
        mistake_file = self.current_file if self.is_in_review else self.file_name + "_mistakes.md"
        
        if not os.path.exists(mistake_file):
            with open(mistake_file, "w", encoding="utf-8") as file:
                file.write("| Word | Translation | Mistakes|\n")
                file.write("| --- | --- | --- |\n")
        
        # #get mistake list and times
        exist_word = {}
        with open(mistake_file, "r", encoding="utf-8") as file:
            lines = file.readlines()[2:]
            for line in lines:
                if line.strip() == "" or line.startswith("|-") or line.startswith("#"):
                    continue
                if "|" in line:
                    columns = line.strip().split("|")
                    if len(columns) >= 3:
                        word = columns[1].strip()
                        translate=columns[2].strip()
                        times=columns[3].strip()
                        exist_word[word] = {"translate":translate,"times":times}

        #update mistake list
        for word, times in self.mistake_buffer.items():
            if word in exist_word:
                exist_word[word]["times"] = int(exist_word[word]["times"]) + times
            else:
                exist_word[word] = {"translate":self.mistake_buffer_ch[word],"times":times}
        #write to file
        with open(mistake_file, "w", encoding="utf-8") as file:
            file.write("| Word | Translation | Mistakes|\n")
            file.write("| --- | --- | --- |\n")
            for word, data in exist_word.items():
                if int(data["times"])>-2:
                    file.write(f"| {word} | {data['translate']} | {data['times']} |\n")
        # clear buffer
        self.mistake_buffer.clear()


def main():
    root = tk.Tk()
    VocabularySystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
