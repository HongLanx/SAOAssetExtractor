import os
import struct


def extract_tga_from_phyre(phyre_file):
    with open(phyre_file, 'rb') as f:
        if f.read(5) != b'RYHPT':
            print("Not a .tga.phyre file!")
            return
        f.seek(0)
        file_size = len(f.read())
        f.seek(80)
        tga_size = struct.unpack('I', f.read(4))[0]
        tga_offset = file_size - tga_size
        f.seek(tga_offset - 62)
        width = struct.unpack('I', f.read(4))[0]
        height = struct.unpack('I', f.read(4))[0]
        if f.read(16) != b'\x50\x54\x65\x78\x74\x75\x72\x65\x32\x44\x00\x52\x47\x42\x41\x38':
            print("Currently unsupported file format!")
        pixel_depth = struct.pack('B', int(tga_size / (width * height)) * 8)
        new_path = os.path.join(os.path.dirname(phyre_file),
                                f"{os.path.basename(phyre_file).split('.')[0]}.tga")
        f.seek(tga_offset)
        with open(new_path, "wb") as o:
            o.write(b'\x00\x00\x02\x00\x00\x00\x00\x00\x00\x00\x00\x00')
            o.write(struct.pack('H', width))
            o.write(struct.pack('H', height))
            o.write(pixel_depth)
            o.write(struct.pack('B', 8))
            for i in range(width):
                for j in range(height):
                    pixel = struct.unpack('BBBB', f.read(4))
                    blue = pixel[0]
                    green = pixel[1]
                    red = pixel[2]
                    alpha = pixel[3]
                    o.write(struct.pack('B', red))
                    o.write(struct.pack('B', green))
                    o.write(struct.pack('B', blue))
                    o.write(struct.pack('B', alpha))
            buffer = b''.join([
                b'\x00\x00\x00\x00\x00\x00\x00\x54\x52\x55\x45\x56\x49\x53\x49\x4F',
                b'\x4E\x2D\x58\x46\x49\x4C\x45\x2E\x00'])
            o.write(buffer)
    o.close()
    f.close()
    print(f"{os.path.basename(phyre_file)}: transfer complete")


def extract_bc7_from_phyre(phyre_file):
    with open(phyre_file, 'rb') as f:
        if f.read(5) != b'RYHPT':
            print("Not a .DDS.phyre file!")
            return
        file_size = os.path.getsize(phyre_file)
        f.seek(0x50)
        dds_size = struct.unpack('I', f.read(4))[0]
        dds_offset = file_size - dds_size
        f.seek(dds_offset - 0x3c)
        width = struct.unpack('I', f.read(4))[0]
        height = struct.unpack('I', f.read(4))[0]
        if f.read(0xf) != b'\x50\x54\x65\x78\x74\x75\x72\x65\x32\x44\x00\x42\x43\x37\x00':
            print("Not a BC7 DDS file!")
        new_path = os.path.join(os.path.dirname(phyre_file),
                                f"{os.path.basename(phyre_file).split('.')[0]}.dds")
        f.seek(dds_offset)
        data = f.read(dds_size)
        with open(new_path, "wb") as o:
            o.write(b'\x44\x44\x53\x20\x7C\x00\x00\x00\x07\x10\x0A\x00')
            o.write(struct.pack('I', height))
            o.write(struct.pack('I', width))
            o.write(
                b''.join([
                    b'\x00\x00\x10\x00\x01\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00',
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x20\x00\x00\x00\x04\x00\x00\x00',
                    b'\x44\x58\x31\x30\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x10\x00\x00\x00\x00\x00\x00',
                    b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x62\x00\x00\x00',
                    b'\x03\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00'])
            )
            o.write(data)
    o.close()
    f.close()
    print(f"{os.path.basename(phyre_file)}: transfer complete")
