import os
import shutil
import gzip
import struct
from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label


class GopExtractor:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Extract scripts from .gop files", command=self.button_extract_clicked)
        self.extract_button.pack()

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            output_dir = os.path.dirname(single_file)
            self.extract_gop(single_file,
                             os.path.join(output_dir, f"{os.path.basename(single_file).split('.')[0]}.txt"))

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def extract_gop(self, script_file, destination_dir):
        with open(script_file, 'rb') as f:

            f.seek(0x28)
            offset_GREC = struct.unpack('I', f.read(4))[0] + 0x30
            f.seek(offset_GREC + 8)
            offset_STRT = struct.unpack('I', f.read(4))[0] + offset_GREC + 0x10
            f.seek(offset_STRT + 8)
            script_end = struct.unpack('I', f.read(4))[0] + offset_STRT + 0x10
            f.read(0x0C)
            script_start = struct.unpack('I', f.read(4))[0] + offset_STRT + 0x10
            script_size = script_end - script_start
            f.seek(script_start)
            script_bytes = f.read(script_size)
            split_data = script_bytes.split(b'\x00')
            # 用UTF-8编码转换成字符串并写入文件
            with open(destination_dir, "wb") as output:
                for chunk in split_data:
                    if chunk:  # 跳过空字符串
                        output.write(chunk + b'\n')


root = Tk()
app = GopExtractor(root)
root.title("Script Extractor")
root.mainloop()
