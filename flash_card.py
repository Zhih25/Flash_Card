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
        self.probability_weight = [0.1,0.2,0.3,0.4]
        self.current_card = {}
        self.current_file = ""
        self.showing_translation = False
        self.mistake_buffer = {}
        self.mistake_buffer_ch = {}
        self.file_name = ""
        self.is_in_review = False
        self.update_threshold = 5
        self.update_cnt =0

        # initial setup
        self.show_main_menu()

    # parse markdown file
    def parse_md_file(self, filename):
        words = []
        self.is_in_review = bool(re.search(r'_mistakes\.md$', filename))
        try:
            with open(filename, "r", encoding="utf-8") as file:
                lines = file.readlines()[2:]
                word_list=[{} for i in range(4)]
                for line in lines:
                    if line.strip() == "" or line.startswith("| -") or line.startswith("#"):
                        continue
                    if "|" in line:
                        columns = line.strip().split("|")
                        if len(columns) >= 3:
                            word = columns[1].strip()
                            translation = columns[2].strip()
                            times = int(re.sub(r'\s+', '', columns[3])) if len(columns) >=5 else 0

                            if not self.is_in_review:
                                # word_list[0].append({"word": word, "translation": translation, "times":times})
                                word_list[0][word]= {"word": word, "translation": translation, "times":times}
                            else:
                                index = self.get_index(times)
                                # word_list[index].append({"word": word, "translation": translation, "times":times})
                                word_list[index][word]= {"word": word, "translation": translation, "times":times}
        except Exception as e:
            print(f"Error reading file {filename}: {e}")
        return word_list

    # clear window
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    #  get index
    def get_index(self, times):
        index_mapping = {
            range(-2, 0): 0,   # times in [-2, -1]
            range(0, 2): 1,    # times in [0]
            range(2, 4): 2,    # times in [1]
            range(4, 101): 3   # times in [2, 100]
        }
        return next((idx for r, idx in index_mapping.items() if times in r), -1)

    # show main menu
    def show_main_menu(self):
        self.clear_window()
        self.root.bind("<Escape>", lambda event: None)
        tk.Label(self.root, text="Choose Vocabulary Set", font=("Helvetica", 18), bg="white", fg="black").pack(pady=20)

        files = [f for f in os.listdir() if f.endswith(".md")]
        for file in files:
            tk.Button(
                self.root,
                text=file,
                font=("Helvetica", 14),
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
                font=("Helvetica", 14),
                bg="black",
                fg="red"
            ).pack(pady=10)

    def get_a_volcabulary(self):
        if not self.word_list:
            return None
        if self.is_in_review:
            # check if the list is empty
            index = random.choices(range(len(self.word_list)), weights=self.probability_weight, k=1)[0]
            while len(self.word_list[index]) == 0:
                index = random.choices(range(len(self.word_list)), weights=self.probability_weight, k=1)[0]

            # self.current_card = random.choice(self.word_list[index])
            self.current_card = random.choice(list(self.word_list[index].values()))
        else:
            # self.current_card = random.choice(self.word_list[0])
            self.current_card = random.choice(list(self.word_list[0].values()))
        return self.current_card
    
    #show flashcard
    def show_flashcard(self):
        self.clear_window()
        self.showing_translation = False
        self.current_card = self.get_a_volcabulary()

        canvas = tk.Canvas(self.root, width=700, height=160, bg="lightyellow", bd=0, highlightthickness=0)
        canvas.pack(pady=50)
        canvas.create_rectangle(10, 10, 690, 150, fill="lightyellow", outline="black", width=2)

        self.word_label = tk.Label(
            self.root,
            text=self.current_card["word"],
            font=("Helvetica", 24),
            bg="lightyellow",
            fg="black",
            wraplength=680,
            justify="center"
        )
        canvas.create_window(350, 80, window=self.word_label)

        self.translation_label = tk.Label(
            self.root,
            text="",
            font=("Helvetica", 18),
            bg="black",
            fg="white"
        )
        self.translation_label.pack(pady=10)
        
        instruction_label = tk.Label(
            self.root,
            text="Press Up key if you know, Down key for you don't know, Enter key to Skip.",
            font=("Helvetica", 12),
            fg="white",
            bg="black"
        )
        instruction_label.pack(side="bottom", pady=20)

        esc_label = tk.Button(
            self.root,
            text="Main Menu",
            font=("Helvetica", 10),
            fg="black",
            bg="black",
            command=self.show_main_menu
        )
        #place the ESC label at the top left
        esc_label.place(x=10, y=10)
        
        if self.is_in_review:
            self.root.bind("<Up>",lambda event: self.update_buffer(False, event))
            self.root.bind("<Down>",lambda event: self.update_buffer(True, event))
            self.root.bind("<Escape>", lambda event: self.show_main_menu())
            self.root.bind("<Return>", self.toggle_translation_or_next)
        else:
            self.root.bind("<Up>", self.toggle_translation_or_next)
            self.root.bind("<Down>",lambda event: self.update_buffer(True, event))
            self.root.bind("<Escape>", lambda event: self.show_main_menu())
            self.root.bind("<Return>", self.toggle_translation_or_next)

    # show translation or next word
    def toggle_translation_or_next(self, event=None):
        if self.showing_translation:
            self.show_flashcard()
        else:
            self.translation_label.config(text=self.current_card["translation"])
            self.showing_translation = True

    def update_list(self, ans):
        word = self.current_card["word"]
        for i in range(4):
            if word in self.word_list[i]:
                del self.word_list[i][word]

        self.current_card["times"] += 1 if ans else -1
        index = self.get_index(self.current_card["times"])
        if index != -1:
            self.word_list[index][word] = self.current_card

    # add to mistake times
    def update_buffer(self,ans, event=None):
        if self.is_in_review:
            self.update_list(ans)
        self.update_cnt += 1
        print(self.update_cnt)
        word = self.current_card["word"]
        self.mistake_buffer_ch[word] = self.current_card["translation"]
        if word not in self.mistake_buffer:
            self.mistake_buffer[word] = 1* (1 if ans else -1)
        else:
            self.mistake_buffer[word] += 1 * (1 if ans else -1)

        if self.update_cnt >= self.update_threshold:
            self.update_mistake_file()

        self.toggle_translation_or_next()


    # update review file
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
        self.update_cnt = 0

def main():
    root = tk.Tk()
    VocabularySystem(root)
    root.mainloop()


if __name__ == "__main__":
    main()
