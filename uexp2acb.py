import os
import shutil
import gzip
import struct
from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label


class AcbExtractor:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Extract acbs from .uexp files", command=self.button_extract_clicked)
        self.extract_button.pack()

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            if single_file.split('.')[-1]!="uexp":
                continue
            output_dir = os.path.dirname(single_file)
            self.extract_acb(single_file,
                             os.path.join(output_dir, f"{os.path.basename(single_file).split('.')[0]}.acb"))

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def extract_acb(self, script_file, destination_dir):
        with open(script_file, 'rb') as f:
            file_size=os.path.getsize(script_file)
            f.seek(0x19)
            name_len=struct.unpack('I', f.read(4))[0]
            f.read(name_len+0x20)
            acb_hex=f.read(file_size-f.tell())
            with open(destination_dir, "wb") as output:
                output.write(acb_hex)


root = Tk()
app = AcbExtractor(root)
root.title("Script Extractor")
root.mainloop()
