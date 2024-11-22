import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox


def move_to_pattern_end(f, pattern):
    pattern_length = len(pattern)
    buffer = bytearray()

    while True:
        byte = f.read(1)
        if not byte:
            break
        buffer.append(byte[0])

        # 如果缓冲区的长度超过了模式长度，删除最早的字节
        if len(buffer) > pattern_length:
            buffer.pop(0)

        # 检查缓冲区的内容是否匹配模式
        if buffer == pattern:
            break

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        process_folder(folder_selected)
    else:
        messagebox.showinfo("Info", "No folder selected")


def process_folder(folder):
    # 提取文件夹中的所有文件名
    files = os.listdir(folder)

    # 创建一个字典来存储每个编号对应的主文件名
    main_files = {}

    for filename in files:
        if filename[-4:] != ".hca":
            file_id = filename
            main_files[file_id]={}
    # 遍历文件，找到主文件并记录编号对应的主文件名
    for filename in files:
        if filename[-4:] == ".hca":
            file_count = int(filename.split('.')[1].split('_')[0])  # 提取编号部分
            file_id = filename.split('_')[0]
            main_files[file_id][file_count] = filename

    for filename in files:
        if filename[-4:] != ".hca":
            file_id = filename
            hca_files = main_files.get(file_id)
            with open(os.path.join(folder,filename), 'rb') as f:
                f.seek(1632)
                move_to_pattern_end(f,b'\x43\x75\x65\x49\x6E\x64\x65\x78\x00')
                new_names = f.read(len(hca_files) * 14).split(b'\x00')
                for i in range(len(hca_files)):
                    new_name = new_names[i].decode()
                    print(new_name)
                    hca_files[i] = new_name
                f.close()

    for filename in files:
        if filename[-4:] == ".hca":
            file_count = int(filename.split('.')[1].split('_')[0])  # 提取编号部分
            file_id = filename.split('_')[0]
            old_path = os.path.join(folder, filename)
            new_name = f"{file_id}_.{main_files[file_id][file_count]}.hca"
            new_path = os.path.join(folder, new_name)
            os.rename(old_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")

    messagebox.showinfo("Info", "Processing completed")


# 创建图形化窗口
root = tk.Tk()
root.title("Localize File Renamer")

# 创建并放置按钮
btn = tk.Button(root, text="Select Folder", command=select_folder)
btn.pack(pady=20)

# 运行窗口主循环
root.mainloop()
