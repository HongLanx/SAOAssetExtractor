import os

def read_file(file_path):
    """读取文件内容并返回按行分割的列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read().strip().split('\n\n')
    return content

def merge_contents(*file_contents):
    """按行合并多个文件内容"""
    merged_content = []
    for lines in zip(*file_contents):
        merged_content.append('\n'.join(lines))
        merged_content.append('')  # 添加空行
    return '\n'.join(merged_content).strip()

# 获取当前目录
current_dir = os.getcwd()

# 获取所有文件名并按编号分组
files = os.listdir(current_dir)
grouped_files = {}

for filename in files:
    if filename.startswith("localize_msg_") and filename.endswith(".txt"):
        # 提取文件类型和编号
        parts = filename.split('_')
        file_type = parts[2]
        file_number = parts[3]
        key = file_number

        if key not in grouped_files:
            grouped_files[key] = {}
        grouped_files[key][file_type] = filename

# 对每一组文件进行合并
for group, files in grouped_files.items():
    cht_file = files.get('cht')
    jpn_file = files.get('jpn')
    usa_file = files.get('usa')

    if cht_file and jpn_file and usa_file:
        # 读取文件内容
        cht_content = read_file(cht_file)
        jpn_content = read_file(jpn_file)
        usa_content = read_file(usa_file)

        # 合并内容
        merged_content = merge_contents(cht_content, jpn_content, usa_content)

        # 写入新的合并文件
        output_filename = f"merged_localize_msg_{group}"
        with open(output_filename, 'w', encoding='utf-8') as output_file:
            output_file.write(merged_content)

        print(f"Created: {output_filename}")
