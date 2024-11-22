import os

def read_file(file_path):
    """读取文件内容并返回按行分割的列表"""
    with open(file_path, 'r', encoding='utf-8') as file:
        try:
            content = file.read().strip().split('\n')
        except UnicodeDecodeError:
            print("该文件无法正确通过UTF-8编码打开")
            return
    return content

def merge_contents(deduplicate, *file_contents):
    """按行合并多个文件内容"""
    merged_content = []
    for lines in zip(*file_contents):
        if deduplicate and all(line == lines[0] for line in lines):
            merged_content.append(lines[0])
        else:
            merged_content.append('\n'.join(lines))
        merged_content.append('')  # 添加空行
    return '\n'.join(merged_content).strip()

# 获取当前目录
current_dir = os.getcwd()

# 获取所有文件名并按编号分组
files = os.listdir(current_dir)
grouped_files = {}

for filename in files:
    if filename.endswith(".txt"):
        # 提取文件类型和编号
        parts = filename.split('_')
        file_type = parts[-1:][0].split('.')[0]
        file_id = filename.strip(parts[-1:][0])
        key = file_id

        if key not in grouped_files:
            grouped_files[key] = {}
        grouped_files[key][file_type] = filename

# 提示用户是否启用去重功能
deduplicate = input("Do you want to enable deduplication of identical lines? (yes/no): ").strip().lower() == 'yes'

# 对每一组文件进行合并
for id, files in grouped_files.items():
    cht_file = files.get('cht')
    jpn_file = files.get('jpn')

    if cht_file and jpn_file:
        # 读取文件内容
        cht_content = read_file(cht_file)
        jpn_content = read_file(jpn_file)

        if cht_content and jpn_content:
            # 合并内容
            merged_content = merge_contents(deduplicate, cht_content, jpn_content)
            # 写入新的合并文件
            output_filename = f"{id}_cht_jpn.txt"
            with open(output_filename, 'w', encoding='utf-8') as output_file:
                output_file.write(merged_content)

            print(f"Created: {output_filename}")
            os.remove(cht_file)
            os.remove(jpn_file)
        else:
            print("未能够成功读入文本")
