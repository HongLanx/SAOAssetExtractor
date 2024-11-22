import os
import re
from collections import defaultdict

def extract_utf8_string(file_content):
    """Extract the UTF-8 string from the file content, ignoring the trailing 00 bytes."""
    # Remove trailing 00 bytes
    content = file_content.rstrip(b'\x00')
    # Decode the remaining bytes as UTF-8
    return content.decode('utf-8')

# 获取当前目录
current_dir = os.getcwd()

# 正则表达式匹配文件名格式
pattern = re.compile(r"localize_msg_cht_\(\d{4}\)_\(\d{4}\)")

# 字典存储文件内容，键为文件名前缀，值为内容列表
file_groups = defaultdict(list)

# 遍历当前目录中的所有文件
for filename in os.listdir(current_dir):
    if os.path.isfile(filename) and pattern.match(filename):
        # 提取文件名前缀（localize_msg_cht_(0000)）
        prefix = re.match(r"(localize_msg_cht_\(\d{4}\))_\(\d{4}\)", filename).group(1)
        with open(filename, 'rb') as file:
            content = file.read()
            extracted_string = extract_utf8_string(content)
            file_groups[prefix].append(extracted_string)
        os.remove(filename)

# 将内容写入新的合并文件
for prefix, contents in file_groups.items():
    new_filename = f"{prefix}.txt"
    with open(new_filename, 'w', encoding='utf-8') as new_file:
        for content in contents:
            new_file.write(content + '\n\n')
    print(f"Created: {new_filename}")