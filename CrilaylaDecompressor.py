import struct
import tkinter as tk
from tkinter import filedialog, messagebox


def xor(input_bytes, key):
    return bytearray([b ^ key[i % len(key)] for i, b in enumerate(input_bytes)])


def decompress_crilayla(input_data):
    decompressed_header_size = 0x100

    # CRILAYLA check
    magic = input_data[0][:8]
    if magic != b"CRILAYLA":
        raise ValueError("CRILAYLA Header not found")

    decompressed_size, decompressed_header_offset = struct.unpack("<II", input_data[0][8:16])

    result = bytearray(decompressed_size + decompressed_header_size)

    # Copy uncompressed 0x100 header to start of file
    result[:decompressed_header_size] = input_data[0][
                                        decompressed_header_offset + 0x10:decompressed_header_offset + decompressed_header_size]

    input_end = len(input_data[0]) - decompressed_header_size - 1
    input_offset = [input_end]  # Using a list to simulate pass-by-reference
    output_end = decompressed_header_size + decompressed_size - 1
    bit_pool = [0]  # Using a list to simulate pass-by-reference
    bits_left = [0]  # Using a list to simulate pass-by-reference
    bytes_output = 0
    vle_lens = [2, 3, 5, 8]

    while bytes_output < decompressed_size:

        if decompressed_size - bytes_output < 22:
            # TODO: Fix last few bytes on some files (could just be junk data)
            break

        check = get_next_bits(input_data, input_offset, bit_pool, bits_left, 1)

        if check > 0:
            backreference_offset = output_end - bytes_output + get_next_bits(input_data, input_offset, bit_pool,
                                                                             bits_left, 13) + 3
            back_reference_length = 3
            vle_level = 0

            for vle_level in range(len(vle_lens)):
                this_level = get_next_bits(input_data, input_offset, bit_pool, bits_left, vle_lens[vle_level])
                back_reference_length += this_level
                if this_level != (1 << vle_lens[vle_level]) - 1:
                    break

            if vle_level == len(vle_lens):
                this_level = 0
                while this_level == 255:
                    this_level = get_next_bits(input_data, input_offset, bit_pool, bits_left, 8)
                    back_reference_length += this_level

            for i in range(back_reference_length):
                result[output_end - bytes_output] = result[backreference_offset]
                backreference_offset -= 1
                bytes_output += 1
        else:
            # Verbatim byte
            result[output_end - bytes_output] = get_next_bits(input_data, input_offset, bit_pool, bits_left, 8)
            bytes_output += 1

    return bytes(result)


def get_next_bits(input_data, offset, bit_pool, bits_left, bit_count):
    out_bits = 0
    num_bits_produced = 0

    while num_bits_produced < bit_count:

        if bits_left[0] == 0:
            bit_pool[0] = input_data[0][offset[0]]
            bits_left[0] = 8
            offset[0] -= 1

        if bits_left[0] > (bit_count - num_bits_produced):
            bits_this_round = bit_count - num_bits_produced
        else:
            bits_this_round = bits_left[0]

        out_bits <<= bits_this_round
        out_bits |= (bit_pool[0] >> (bits_left[0] - bits_this_round)) & ((1 << bits_this_round) - 1)

        bits_left[0] -= bits_this_round
        num_bits_produced += bits_this_round
    return out_bits


def decompress_file(input_path):
    try:
        in_file_data = [bytearray()]
        with open(input_path, 'rb') as f:
            in_file_data[0] = bytearray(f.read())

        # XOR header 16 bytes with key 0xff
        enc_header = in_file_data[0][:16]
        dec_header = xor(enc_header, b'\xff')

        # Replace with fixed header
        in_file_data[0][:16] = dec_header

        decompressed_data = decompress_crilayla(in_file_data)

        # Overwrite the original file with decompressed data
        with open(input_path, 'wb') as f:
            f.write(decompressed_data)

        messagebox.showinfo("Success", f"File decompressed and saved to {input_path}")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def select_file():
    input_path = filedialog.askopenfilename()
    if input_path:
        decompress_file(input_path)


# Setting up the GUI
root = tk.Tk()
root.title("CRILAYLA Decompressor")

frame = tk.Frame(root)
frame.pack(pady=20, padx=20)

select_button = tk.Button(frame, text="Select File to Decompress", command=select_file)
select_button.pack()

root.mainloop()
