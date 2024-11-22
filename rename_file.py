import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox


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

    # 正则表达式匹配文件名
    main_pattern = re.compile(r'^(.*?_\(\d{4}\))\.txt$')
    localize_pattern = re.compile(r'^localize_msg_(cht|jpn|usa)_\(\d{4}\)\.txt$')

    # 遍历文件，找到主文件并记录编号对应的主文件名
    for filename in files:
        main_match = main_pattern.match(filename)
        if filename[:8] != "localize" and main_match:
            file_id = main_match.group(1)[-6:]  # 提取编号部分
            main_files[file_id] = main_match.group(1)
            print(main_match.group(1)[:-7])

    # 遍历文件，重命名本地化文件
    for filename in files:
        localize_match = localize_pattern.match(filename)
        if localize_match:
            lang = localize_match.group(1)
            file_id = filename[-10:-4]  # 提取编号部分
            if file_id in main_files:
                new_filename = f"{main_files[file_id]}_{lang}_{file_id}.txt"
                old_path = os.path.join(folder, filename)
                new_path = os.path.join(folder, lang,new_filename)
                if not os.path.exists(os.path.join(folder, lang)):
                    os.makedirs(os.path.join(folder, lang))
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")

    messagebox.showinfo("Info", "Processing completed")


# 创建图形化窗口
root = tk.Tk()
root.title("Localize File Renamer")

# 创建并放置按钮
btn = tk.Button(root, text="Select Folder", command=select_folder)
btn.pack(pady=20)

# 运行窗口主循环
root.mainloop()
