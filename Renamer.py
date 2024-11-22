import json
import os
import shutil
import tkinter as tk
from tkinter import filedialog
from PyCriCodecs import *
import csv


def process_directory(directory):
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            process_file(file_path,directory)


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
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window
    files = filedialog.askopenfilenames()
    for file in files:
        process_csv(file)


def process_file(file_path, directory):
    new_file_path = file_path.split(".")[0]+f"_en."+file_path.split(".")[1]
    # file_name=os.path.basename(file_path)
    # new_file_name="_".join(file_name.split("_")[0:2])+"_"+"_".join(file_name.split("_")[5:7])+".wav"
    # new_file_path=os.path.join(directory,new_file_name)
    shutil.move(file_path, new_file_path)
    print(f"rename {file_path} to {new_file_path}")


def load_json(json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def load_csv(csv_file):
    csv_data = {}
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        for row in reader:
            key = row[0]
            csv_data[key] = row
    return csv_data


def sort_and_write_csv(json_file):
    csv_file = json_file.replace(".json", ".csv")
    output_folder=os.path.join(os.path.dirname(json_file),"zh")
    output_csv=os.path.join(output_folder,os.path.basename(csv_file))
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    if not os.path.exists(csv_file):
        print(f"{csv_file} not exists!")
        return
    # 读取 JSON 文件
    json_data = load_json(json_file)

    # 提取 JSON 中的 key 顺序
    key_order = []
    for item in json_data["Exports"][0]["Table"]["Value"]:
        key_order.append(item[0])

    # 读取 CSV 文件并存储数据
    csv_data = load_csv(csv_file)

    # 按照 JSON 中的顺序排序 CSV 数据
    sorted_csv_data = []
    for key in key_order:
        if key in csv_data:
            sorted_csv_data.append(csv_data[key])

    # 写回到 CSV 文件
    with open(output_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(sorted_csv_data)


def generate_ffmpeg_commands(directory, output_file='ffmpeg_commands.txt'):
    commands = []

    # 获取目录下所有的文件
    files = os.listdir(directory)

    # 过滤出 .adx 和 .m2v 文件
    adx_files = [f for f in files if f.endswith('.adx')]
    m2v_files = [f for f in files if f.endswith('.m2v')]

    # 对于每个 .adx 文件，找到对应的 .m2v 文件，并生成命令
    for adx in adx_files:
        base_name = os.path.splitext(adx)[0]
        m2v = base_name + '.m2v'
        if m2v in m2v_files:
            command = f'ffmpeg -i {m2v} -i {adx} -c:v copy -c:a aac -map 0:v:0 -map 1:a:0 {base_name}.mp4'
            commands.append(command)

    # 将命令写入文件
    with open(output_file, 'w') as f:
        f.write('\n'.join(commands))

    print(f"Commands written to {output_file}")


def trim_file_to_utf(filepath):
    """
    找到文件中第一个 b"@UTF" 的位置，并保留该位置之后的字节。
    """
    utf_marker = b"@UTF"
    output_file = filepath.split('.')[0] + f".acb"

    with open(filepath, 'rb') as f:
        data = f.read()

    # 查找第一个 b"@UTF" 的位置
    utf_position = data.find(utf_marker)

    if utf_position != -1:
        # 从 b"@UTF" 开始保留
        trimmed_data = data[utf_position:]

        # 将结果保存到新的文件
        with open(output_file, 'wb') as f_out:
            f_out.write(trimmed_data)

        print(f"Trimmed file saved as {output_file}")
    else:
        print(f"No b'@UTF' found in {filepath}")


def decode_adx(file_path):
    # Decoding:
    adx_data = open(file_path, "rb").read()
    print(f"正在处理{file_path}")
    wavfilebytes = ADX.decode(adx_data)  # Decode will return bytes object containing decoded ADX data as a wav file.
    wav_path = ".".join(file_path.split('.')[:-1]) + ".wav"
    with open(wav_path, "wb") as o:
        o.write(wavfilebytes)


def create_csv(input_file):
    # 用字典来存储不同表名对应的内容
    tables = {}

    # 打开输入文件
    with open(input_file, 'r', encoding='utf-8') as infile:
        reader = csv.reader(infile)
        next(reader)  # 跳过表头

        # 逐行处理
        for row in reader:
            key, source, target = row
            table_name, key_value = key.split('/')  # 分割表名和key

            # 如果该表名不存在于字典中，初始化一个空列表
            if table_name not in tables:
                tables[table_name] = []

            # 添加当前行的 key_value 和 source 到对应表名的列表
            tables[table_name].append([key_value, source, target])

    # 遍历所有表名并写入相应的文件
    for table_name, data in tables.items():
        output_file = f"{table_name}.csv"
        with open(output_file, 'w', encoding='utf-8', newline='') as outfile:
            writer = csv.writer(outfile)
            # 写入每一行
            writer.writerows(data)



def modify_csv(file_path):
    # 打开CSV文件并读取内容
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        lines = list(reader)

    # 修改第一列的格式
    for line in lines:
        if line:
            original_id = line[0]
            # 提取并格式化为36_0100_xxx_0格式
            if len(original_id) == 10 and original_id.isdigit():
                part1 = original_id[1:3]  # 36
                part2 = original_id[3:7]  # 0100
                part3 = original_id[7:10]  # 001
                line[0] = f"{part1}_{part2}_{part3}_0"

    # 将修改后的内容保存到源文件
    with open(file_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(lines)

def process_csv(input_file):
    output_file = input_file.split(".")[0] + ".txt"
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        reader = csv.reader(infile)
        lines = list(reader)
        # 修改第一列的格式
        for line in lines:
            original_id = line[0]
            msg=line[1]
            outfile.write(f"{original_id}\n{msg}\n\n")  # 按照你的格式写入


select_directory()
