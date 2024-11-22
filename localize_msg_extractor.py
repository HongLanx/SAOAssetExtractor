import os
import shutil
import gzip
import struct
from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label


class LocalizeExtractor:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Extract scripts from localize files",
                                     command=self.button_extract_clicked)
        self.extract_button.pack()

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            output_dir = os.path.dirname(single_file)
            self.extract_localize(single_file,
                                  os.path.join(output_dir, f"{os.path.basename(single_file).split('.')[0]}.txt"))

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def extract_localize(self, script_file, destination_dir):
        with open(script_file, 'rb') as f:
            f.seek(0x10)
            script_nums = struct.unpack('I', f.read(4))[0]
            script_offset = []
            script_id = []
            script_data = []
            for i in range(script_nums):
                script_offset.append(struct.unpack('I', f.read(4))[0] + 0x10)
                script_id.append(f.read(4))
            for i in range(script_nums):
                if i != script_nums - 1:
                    script_size = script_offset[i + 1] - script_offset[i]
                else:
                    script_size = os.path.getsize(script_file) - script_offset[i]
                if script_size>0:
                    f.seek(script_offset[i])
                    script_data.append(f.read(script_size).strip(b'\x00'))
                else:
                    print(script_offset[i])
                    script_data.append(b'')
            # 用UTF-8编码转换成字符串并写入文件
            with open(destination_dir, "wb") as output:
                for i in range(script_nums):
                    hex_str=script_id[i].hex()
                    str=(''.join(reversed([hex_str[j:j+2] for j in range(0, len(hex_str), 2)]))).upper()
                    output.write(str.encode()+b'\n')
                    output.write(script_data[i] + b'\n\n')


root = Tk()
app = LocalizeExtractor(root)
root.title("Script Extractor")
root.mainloop()
