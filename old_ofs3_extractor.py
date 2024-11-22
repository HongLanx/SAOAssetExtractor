import os
import shutil
import gzip
import struct
from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label
from RGBAtrans import extract_tga_from_phyre


class OFS3Tool:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Extract OFS3", command=self.button_extract_clicked)
        self.extract_button.pack()

    def decompress_gzip(self, compressed_file):
        decompressed_file = compressed_file + ".decompressed"

        with open(compressed_file, 'rb') as f:
            magic = f.read(4)
            if magic == b'OFS3':
                decompressed_file += ".ofs3"

        with gzip.open(compressed_file, 'rb') as f_in:
            with open(decompressed_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        os.remove(compressed_file)

        if os.path.splitext(decompressed_file)[1] == ".ofs3":
            self.unpack_ofs3(decompressed_file, os.path.dirname(decompressed_file))

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            output_dir = os.path.dirname(single_file)
            self.unpack_ofs3(single_file, output_dir)

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def unpack_ofs3(self, ofs3_file, destination_dir):
        if ofs3_file.split('.')[-1]=="phyre" and ofs3_file.split('.')[-2] == "tga":
            extract_tga_from_phyre(ofs3_file)
        with open(ofs3_file, 'rb') as f:
            head=f.read(4)
            if head != b'OFS3':
                print("Not a OFS3 File")
                return

            if not os.path.exists(destination_dir):
                os.makedirs(destination_dir)

            f.read(4)  # Header
            type_ = struct.unpack('H', f.read(2))[0]
            padding = struct.unpack('B', f.read(1))[0]
            subtype = struct.unpack('B', f.read(1))[0]
            size = struct.unpack('I', f.read(4))[0]
            n_files = struct.unpack('I', f.read(4))[0]

            extracted_file_offset = []
            extracted_file_size = []
            file_name_offset = []

            for _ in range(n_files):
                extracted_file_offset.append(struct.unpack('I', f.read(4))[0] + 0x10)
                extracted_file_size.append(struct.unpack('I', f.read(4))[0])
                if type_ == 0x02:
                    file_name_offset.append(struct.unpack('I', f.read(4))[0] + 0x10)
                elif type_ == 0x01:
                    file_name_offset.append(size + 0x10)

            with open(os.path.join(destination_dir, "temp"), 'wb') as info_file:
                info_file.write(struct.pack('H', type_))
                info_file.write(struct.pack('B', padding))
                info_file.write(struct.pack('B', subtype))

                if subtype == 1:
                    info_file.write(struct.pack('I', n_files))
                    for size in extracted_file_size:
                        info_file.write(struct.pack('I', size))

            for i in range(n_files):
                if extracted_file_offset[i] <= 32:
                    continue
                if subtype == 1:
                    if i == n_files - 1:
                        extracted_file_size[i] = os.path.getsize(ofs3_file) - extracted_file_offset[i]
                    else:
                        extracted_file_size[i] = extracted_file_offset[i + 1] - extracted_file_offset[i]

                if type_ == 0x02 or type_ == 0x01:
                    f.seek(file_name_offset[i])
                    chara = 1
                    new_file_name = ""
                    while chara != 0:
                        chara = struct.unpack('B', f.read(1))[0]
                        if chara != 0:
                            new_file_name += chr(chara)
                    new_file_name = os.path.join(destination_dir,
                                                 f"{os.path.basename(ofs3_file).split('.')[0]}"
                                                 f"_({i:04d})_{os.path.basename(new_file_name)}")
                else:
                    new_file_name = os.path.join(destination_dir,
                                                 f"{os.path.basename(ofs3_file).split('.')[0]}_({i:05d})")

                f.seek(extracted_file_offset[i])
                new_file_body = f.read(extracted_file_size[i])

                if len(new_file_body) > 8:
                    if not new_file_name.endswith(".ofs3") and new_file_body[:4] == b'OFS3':
                        new_file_name += ".ofs3"
                    elif type_ == 0 and new_file_body[:3] == b'\x1f\x8b\x08':
                        new_file_name += ".gz"
                    elif type_ == 0 and new_file_body[:6] == b'OMG.00':
                        new_file_name += ".gmo"
                    elif type_ == 0 and new_file_body[:6] == b'MIG.00':
                        new_file_name += ".gim"
                    elif type_ == 0 and new_file_body[:4] == b'TIM2':
                        new_file_name += ".tm2"
                    elif type_ == 0 and new_file_body[:4] == b'PIM2':
                        new_file_name += ".pm2"

                with open(new_file_name, 'wb') as new_file:
                    new_file.write(new_file_body)

                if len(new_file_body) > 4:
                    if new_file_body[:3] == b'\x1f\x8b\x08':
                        self.decompress_gzip(new_file_name)
                    elif new_file_body[:4] == b'OFS3':
                        self.unpack_ofs3(new_file_name, os.path.dirname(new_file_name))
                        os.remove(new_file_name)
                name_fix = os.path.basename(new_file_name).split('.')
                if len(name_fix) == 3 and name_fix[1] == "tga" and (name_fix[2] == "phyre" or name_fix[2]=="phyre "):
                    extract_tga_from_phyre(new_file_name)
                    os.remove(new_file_name)


root = Tk()
app = OFS3Tool(root)
root.title("OFS3 Tool")
root.mainloop()
