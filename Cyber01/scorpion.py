

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

def ParseJPGFile(fileName):
    with open(fileName, 'rb') as file:
        print("    -----JPG File-----")
        FILEDATA = file.read()
        print("--JPG File Header--")
        OFFSET = FILEDATA.find(b'JFIF') + 5
        print("Version : 1.0" + str(int.from_bytes(FILEDATA[OFFSET:OFFSET+1], "big")))
        print("Density units : " + str(int.from_bytes(FILEDATA[OFFSET+2:OFFSET+3], "big")))

ParseJPGFile('jpg.jpg')