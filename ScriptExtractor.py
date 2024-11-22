import os
import shutil
import gzip
import struct
from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label


class ScriptExtractor:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Extract Script", command=self.button_extract_clicked)
        self.extract_button.pack()

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            output_dir = os.path.dirname(single_file)
            self.extract_script(single_file, os.path.join(output_dir))

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def extract_script(self, script_file, destination_dir):
        with open(script_file, 'rb') as f:
            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            f.read(8)
            script_offset = struct.unpack('I', f.read(4))[0]
            script_size = struct.unpack('I', f.read(4))[0]
            f.seek(script_offset)
            script_hex=f.read(script_size)
            split_data = script_hex.split(b'\x00')
            script_path = os.path.join(destination_dir, f"{os.path.basename(script_file)}.txt")
            with open(script_path, "wb") as o:
                for chunk in split_data:
                    if chunk:  # 跳过空字符串
                        o.write(chunk+b'\n')


root = Tk()
app = ScriptExtractor(root)
root.title("Script Extractor")
root.mainloop()


