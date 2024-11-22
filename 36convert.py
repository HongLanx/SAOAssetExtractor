import os
import tkinter as tk
from tkinter import filedialog, messagebox

def select_folder():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        process_folder(folder_selected)
    else:
        messagebox.showinfo("Info", "No folder selected")

def convert_id(id_str):
    """将4位id从36进制转换为xx_xx_xx_xx格式"""
    result = []
    for char in id_str:
        if char.isdigit():
            result.append(f'{int(char):02}')
        else:
            result.append(f'{ord(char) - ord("a") + 10:02}')
    return '_'.join(result)

def reverse_id(id_str):
    """将xx_xx_xx_xx格式的id转换回4位id"""
    parts = id_str.split('_')
    result = []
    for part in parts:
        num = int(part)
        if 0 <= num <= 9:
            result.append(str(num))
        else:
            result.append(chr(num - 10 + ord('a')))
    return ''.join(result)

def process_folder(folder, reverse=False):
    files = os.listdir(folder)
    for filename in files:
        if reverse:
            if len(filename) > 11 and filename[:11].count('_') == 3:
                file_id = filename[:11]
                new_id = reverse_id(file_id)
                new_filename = f"{new_id}{filename[11:]}"
                old_path = os.path.join(folder, filename)
                new_path = os.path.join(folder, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")
        else:
            if len(filename) >= 4 and filename[:4].isalnum():
                file_id = filename[:4]
                new_id = convert_id(file_id)
                new_filename = f"{new_id}{filename[4:]}"
                old_path = os.path.join(folder, filename)
                new_path = os.path.join(folder, new_filename)
                os.rename(old_path, new_path)
                print(f"Renamed: {filename} -> {new_filename}")

    messagebox.showinfo("Info", "Processing completed")

def process_normal():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        process_folder(folder_selected, reverse=False)
    else:
        messagebox.showinfo("Info", "No folder selected")

def process_reverse():
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        process_folder(folder_selected, reverse=True)
    else:
        messagebox.showinfo("Info", "No folder selected")

# 创建图形化窗口
root = tk.Tk()
root.title("File Renamer")

# 创建并放置按钮
btn_normal = tk.Button(root, text="Convert to xx_xx_xx_xx", command=process_normal)
btn_normal.pack(pady=10)

btn_reverse = tk.Button(root, text="Convert to xxxx", command=process_reverse)
btn_reverse.pack(pady=10)

# 运行窗口主循环
root.mainloop()
