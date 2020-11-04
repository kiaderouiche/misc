import lzma

def extract_file_xz(file_xz):
    with lzma.open(file_xz) as f:
        file_content = f.read()
        decompressed = lzma.decompress(file_content[4:])
    print(decompressed)

def main():
    extract_file_xz("./accountsservice-0.6.42.tar.xz")

if __name__ == '__main__':
    main()