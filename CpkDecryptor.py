from tkinter import Tk, filedialog, messagebox, Button
from tkinter.ttk import Label


class CpkDecryptor:
    def __init__(self, root):
        self.root = root
        self.label = Label(root, text="Ready!")
        self.label.pack()

        self.extract_button = Button(root, text="Decrypt cpks", command=self.button_extract_clicked)
        self.extract_button.pack()

    def button_extract_clicked(self):
        files = filedialog.askopenfilenames(title="Select one or more files")
        if not files:
            return

        self.label.config(text="Wait...")
        self.label.update()

        for single_file in files:
            self.process_file(single_file)

        self.label.config(text="Ready!")
        messagebox.showinfo("Status", "Done!")

    def process_file(self, input_file):
        hex_string = bytes.fromhex('BCADB6B3BEA6B3BE')  # 要寻找的十六进制字符串
        output_file = f"{input_file}_output"

        with open(input_file, 'rb') as f:
            data = f.read()

        result = bytearray()
        i = 0
        while i < len(data):
            # 寻找匹配的十六进制字符串
            if data[i:i + 8] == hex_string:
                # 提取匹配字符串及其后的8个字节，共16个字节
                chunk = data[i:i + 22]
                # 对这些字节进行异或运算
                result.extend(xor_bytes(chunk))
                # 跳过这16个字节
                i += 22
            else:
                result.append(data[i])
                i += 1

        with open(output_file, 'wb') as f:
            f.write(result)

        print(f"Modified file saved as {output_file}")


def xor_bytes(data):
    return bytes([b ^ 0xFF for b in data])


root = Tk()
app = CpkDecryptor(root)
root.title("Script Extractor")
root.mainloop()
