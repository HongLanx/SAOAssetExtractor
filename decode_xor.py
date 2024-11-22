import os
import struct
import tkinter as tk
from tkinter import filedialog
from RGBAtrans import extract_bc7_from_phyre
def xor_bytes(data, key=0xFF):
    return bytes([b ^ key for b in data])

def process_file(file_path):
    with open(file_path, 'rb+') as f:
        data = f.read(32)
        if data:
            f.seek(0)
            f.write(xor_bytes(data))
            print(f"Find CRILAYLA: {file_path}")
        else:
            print(f"Not CRILAYLA: {file_path}")

def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            process_file(file_path)

def select_directory():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    folder_selected = filedialog.askdirectory()
    if folder_selected:
        process_directory(folder_selected)
        print(f"Processing completed for folder: {folder_selected}")
    else:
        print("No folder selected.")

def select_files():
    files = filedialog.askopenfilenames(title="Select one or more files")
    for file in files:
        extract_bc7_from_phyre(file)

def decode_file(file):
    with open(file, 'rb+') as f:
        f.seek(os.path.getsize(file)-0x20)
        data_byte=[]
        need_decode=0
        for i in range(32):
            data_byte += struct.unpack('B', f.read(1))
        for i in data_byte:
            if i>= 0x7f:
                need_decode+=1
        if need_decode>0x10:
            f.seek(os.path.getsize(file) - 0x20)
            data = f.read(32)
            f.seek(os.path.getsize(file) - 0x20)
            f.write(xor_bytes(data))
            print(f"file_processed: {file}")

# Copy as Python - from 010 Editor - byte count: 32 (0x20)
buffer = b''.join([
    b'\x8A\xF2\xFC\xFF\x7B\xC4\xED\xFF\x83\xF2\xFC\xFF\x63\xC4\xED\xFF',
    b'\x82\xF2\xFC\xFF\x4F\xC4\xED\xFF\x81\xF2\xFC\xFF\x3B\xC4\xED\xFF'])



print(xor_bytes(buffer).hex())