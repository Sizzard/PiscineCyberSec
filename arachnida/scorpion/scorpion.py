import sys
from termcolor import colored

def ParseBMPFile(fileName):
    with open(fileName, 'rb') as file:
        print("    -----BMP File-----")
        BITMAPFILEHEADER = file.read(14)
        print("    --BMP File Header--")
        print("Signature       : ", (BITMAPFILEHEADER[0:2]).decode("utf-8"))
        print("Size            : ", int.from_bytes(BITMAPFILEHEADER[2:8], "little"), "bytes")
        print("PixelArray      : ", int.from_bytes(BITMAPFILEHEADER[10:14], "little"))
        DIB_HEADER = file.read(40)
        print("       --DIB Header--")
        print("DIB header size : ", int.from_bytes(DIB_HEADER[0:4], "little"))
        print("Width           : ", int.from_bytes(DIB_HEADER[4:8], "little"))
        print("Height          : ", int.from_bytes(DIB_HEADER[8:12], "little"))
        print("Planes          : ", int.from_bytes(DIB_HEADER[12:14], "little"))
        print("Bpp             : ", int.from_bytes(DIB_HEADER[14:16], "little"))
        print("Compression     : ", int.from_bytes(DIB_HEADER[16:20], "little"))
        print("Image Size      : ", int.from_bytes(DIB_HEADER[20:24], "little"))

def ParsePNGFile(fileName):
    with open(fileName, 'rb') as file:
        print("    -----PNG File-----")
        FILEDATA = file.read()
        print("--PNG File Header--")
        print("Signature          : ", FILEDATA[1:4].decode("utf-8"))
        print("Width              : ", int.from_bytes(FILEDATA[16:20], "big"))
        print("Height             : ", int.from_bytes(FILEDATA[20:24], "big"))
        print("Bit depth          : ", int.from_bytes(FILEDATA[24:25], "big"))
        print("Color type         : ", int.from_bytes(FILEDATA[25:26], "big"))
        print("Compression method : ", int.from_bytes(FILEDATA[26:27], "big"))
        print("Filter method      : ", int.from_bytes(FILEDATA[27:28], "big"))
        print("Interlace method   : ", int.from_bytes(FILEDATA[28:29], "big"))
        TIME_OFFSET = FILEDATA.find(b'tIME') + 4
        print("Last Modification Date : ", str(int.from_bytes(FILEDATA[TIME_OFFSET + 3 :TIME_OFFSET + 4], "big")) + "/" + str(int.from_bytes(FILEDATA[TIME_OFFSET + 2 :TIME_OFFSET + 3], "big")) + "/" + str(int.from_bytes(FILEDATA[TIME_OFFSET:TIME_OFFSET + 2], "big")))
        print("Last Modification Time : ", int.from_bytes(FILEDATA[TIME_OFFSET + 4 :TIME_OFFSET + 5], "big"),"h", int.from_bytes(FILEDATA[TIME_OFFSET + 5 :TIME_OFFSET + 6], "big"),"m", int.from_bytes(FILEDATA[TIME_OFFSET + 6 :TIME_OFFSET + 7], "big"),"s")
        TEXT_OFFSET = FILEDATA.find(b'tEXT')

def get_image_size_jpeg(fileName):
    with open(fileName, 'rb') as file:
        data = file.read()

    i = 0
    while i < len(data):
        if data[i] == 0xFF and data[i + 1] in [0xC0, 0xC2]:
            height = int.from_bytes(data[i + 5:i + 7], byteorder='big')
            width = int.from_bytes(data[i + 7:i + 9], byteorder='big')
            return width, height
        i += 1
    raise ValueError("Dimensions not found")

def get_exif_data(fileName):
    with open(fileName, 'rb') as file:
        data = file.read()

    i = 0
    while i < len(data) - 2:
        if data[i] == 0xFF and data[i + 1] == 0xE1:
            length = int.from_bytes(data[i + 2:i + 4], "big")
            if data[i + 4:i + 10] == b'Exif\x00\x00': 
                return data[i + 10:i + 10 + length - 2]
        i += 1
    return None

def parse_exif_tags(exif_data):
    endianness = exif_data[:2]
    byte_order = "little" if endianness == b'II' else "big"

    offset_to_ifd = int.from_bytes(exif_data[4:8], byte_order)
    num_entries = int.from_bytes(exif_data[offset_to_ifd:offset_to_ifd + 2], byte_order)

    tags = {}
    base_offset = offset_to_ifd + 2
    for i in range(num_entries):
        entry_offset = base_offset + i * 12
        tag_id = int.from_bytes(exif_data[entry_offset:entry_offset + 2], byte_order)
        data_type = int.from_bytes(exif_data[entry_offset + 2:entry_offset + 4], byte_order)
        num_values = int.from_bytes(exif_data[entry_offset + 4:entry_offset + 8], byte_order)
        value_offset = exif_data[entry_offset + 8:entry_offset + 12]

        if tag_id == 0x010F:
            tags["Fabricant"] = exif_data[int.from_bytes(value_offset, byte_order):].split(b'\x00')[0].decode("utf-8", errors="ignore")
        elif tag_id == 0x0110:
            tags["Modèle"] = exif_data[int.from_bytes(value_offset, byte_order):].split(b'\x00')[0].decode("utf-8", errors="ignore")
        elif tag_id == 0x9003:
            tags["Date de prise"] = exif_data[int.from_bytes(value_offset, byte_order):].split(b'\x00')[0].decode("utf-8", errors="ignore")
        elif tag_id == 0x920A:
            tags["Focale"] = int.from_bytes(value_offset, byte_order) / int.from_bytes(exif_data[int.from_bytes(value_offset, byte_order) + 4:], byte_order)

    return tags

def ParseJPGFile(fileName):
    with open(fileName, 'rb') as file:
        print("    ----- JPG File -----")
        FILEDATA = file.read()
        
        JFIF_OFFSET = FILEDATA.find(b'JFIF')
        
        if JFIF_OFFSET != -1:
            print("-- JPG File Header --")
            OFFSET = JFIF_OFFSET + 5
            version_major = int.from_bytes(FILEDATA[OFFSET:OFFSET + 1], "big")
            version_minor = int.from_bytes(FILEDATA[OFFSET + 1:OFFSET + 2], "big")
            print(f"Version : {version_major}.{version_minor}")
            
            density_units = int.from_bytes(FILEDATA[OFFSET + 2:OFFSET + 3], "big")
            density_units_map = {0: "No units", 1: "Pixels per inch (DPI)", 2: "Pixels per cm (DPCM)"}
            print(f"Density units : {density_units_map.get(density_units, 'Unknown')}")
        else:
            print("No JFIF header found.")
        
        try:
            width, height = get_image_size_jpeg(fileName)
            print(f"Width : {width}, Height : {height}")
        except ValueError as e:
            print(e)
        
        exif_data = get_exif_data(fileName)
        if not exif_data:
            print("No EXIF data found.")
        else:
            print("EXIF data found!")
            print(parse_exif_tags(exif_data))



def ParseGIFFile(fileName):
    with open(fileName, "rb") as file:
        print("----- GIF Metadata -----")

        header = file.read(6).decode("utf-8")
        print("Signature        :", header)

        if header not in ["GIF87a", "GIF89a"]:
            print("Ce fichier n'est pas un GIF valide.")
            return

        screen_desc = file.read(7)
        width = int.from_bytes(screen_desc[0:2], "little")
        height = int.from_bytes(screen_desc[2:4], "little")
        packed_field = screen_desc[4]

        has_global_color_table = (packed_field & 0b10000000) != 0
        color_resolution = ((packed_field & 0b01110000) >> 4) + 1
        sorted_colors = (packed_field & 0b00001000) != 0
        global_color_table_size = 2 ** ((packed_field & 0b00000111) + 1) if has_global_color_table else 0

        print("Width            :", width)
        print("Height           :", height)
        print("Global Color Table:", "Yes" if has_global_color_table else "No")
        print("Color Resolution :", color_resolution)
        print("Sorted Colors    :", "Yes" if sorted_colors else "No")
        print("Color Table Size :", global_color_table_size, "entries")

        while True:
            byte = file.read(1)
            if not byte:
                break

            marker = byte[0]

            if marker == 0x21:
                label = file.read(1)[0]
                if label == 0xFE:
                    print("\n---- Comment Extension ----")
                    comment_data = []
                    while True:
                        block_size = file.read(1)[0]
                        if block_size == 0:
                            break
                        comment_data.append(file.read(block_size).decode("utf-8"))
                    print("Comment:", " ".join(comment_data))

            elif marker == 0x21 and label == 0xFF:
                print("\n---- Application Extension ----")
                app_data = file.read(11)
                print("Identifier:", app_data.decode("utf-8"))

            elif marker == 0x3B:
                print("\n----- End of GIF File -----")
                break


if __name__ == "__main__":

    valid_extensions = ['.jpg', '.jpeg', '.png', '.bmp', '.gif']

    for arg in sys.argv[1:]:
        if any(substring in arg for substring in valid_extensions) is False:
            
            print(colored("Not a valid File Format : " + arg, 'red'))
        else:
            if arg.endswith('.jpg') or arg.endswith('.jpeg'):
                try:
                    ParseJPGFile(arg)
                except:
                    print("Error when reading file : ", arg)
            elif arg.endswith('.png'):
                try:
                    ParsePNGFile(arg)
                except:
                    print("Error when reading file : ", arg)
            elif arg.endswith('.bmp'):
                try:
                    ParseBMPFile(arg)
                except:
                    print("Error when reading file : ", arg)
            elif arg.endswith('.gif'):
                try:
                    ParseGIFFile(arg)
                except:
                    print("Error when reading file : ", arg)
        print()
