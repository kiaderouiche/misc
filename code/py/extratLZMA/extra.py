import lzma

class Compressorerror(Exception):
    pass

def extract_file_xz(file_xz):
    with lzma.open(file_xz) as f:
        file_content = f.read()
        print(type(file_content))
        try:
            decompressed = lzma.decompress(file_content)
            fp.write(decompressed)
        except lzma.LZMAError as e:
            raise Compressorerror(e)
    print(fp)

def main():
    extract_file_xz("./accountsservice-0.6.42.tar.xz")

if __name__ == '__main__':
    main()