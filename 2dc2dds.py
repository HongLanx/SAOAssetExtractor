import os
import shutil
import gzip
import struct
from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label


class TwoDCTool:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Extract 2DC", command=self.button_extract_clicked)
        self.extract_button.pack()

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            # output_dir = os.path.join(os.path.dirname(single_file), os.path.basename(single_file).split('.')[0])
            output_dir=os.path.dirname(single_file)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            self.extract_2dc(single_file, output_dir)

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def extract_2dc(self, file, dest):
        with open(file, 'rb') as f:
            dds_files = []
            f.seek(0x58)
            file_size = struct.unpack('I', f.read(4))[0] + 0x40
            f.seek(0xC0)
            while f.tell() < file_size:
                head = f.read(8)
                dds_size = self.get_size(head, f)
                f.read(0x74)
                dds_file = f.read(dds_size)
                dds_files.append(dds_file)
            for i in range(len(dds_files)):
                new_file_name=os.path.join(dest,f"{os.path.basename(file).split('.')[0]}_{i:04d}.dds")
                with open(new_file_name, 'wb') as new_file:
                    new_file.write(dds_files[i])
                print(f"{os.path.basename(file).split('.')[0]}_{i:04d}.dds")


    def get_size(self, head, f):
        start_offset = f.tell() - 0x8
        if head == b'CH2DPLAN':
            plan_size = struct.unpack('I', f.read(4))[0]
            dds_size = plan_size - 0x70
        elif head == b'CH2DPOSE':
            f.read(0x38)
            new_head = f.read(8)
            dds_size = self.get_size(new_head, f)
        elif head == b'CH2DEXPR':
            f.read(0x28)
            new_head = f.read(8)
            dds_size = self.get_size(new_head, f)
        elif head == b'CH2DPART':
            f.read(0x28)
            new_head = f.read(8)
            dds_size = self.get_size(new_head, f)
        else:
            dds_size = 0
        return dds_size

root = Tk()
app = TwoDCTool(root)
root.title("2DC2DDS Tool")
root.mainloop()
