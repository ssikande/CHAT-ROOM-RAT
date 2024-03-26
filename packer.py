import sys
import gzip
import base64

def pack(payload_file, packed_file):
    # Step 1: Compress the contents of the payload file
    with open(payload_file, 'rb') as f:
        payload_content = f.read()
        payload_zipped = gzip.compress(payload_content)

    # Step 2: Convert the compressed payload to a printable string
    payload_encoded = base64.b64encode(payload_zipped).decode('utf-8')

    # Step 3: Write the packed file with unpacking code
    with open(packed_file, 'w') as f:
        f.write(f'''
import base64
import gzip
import sys

packed_payload = "{payload_encoded}"

def unpack():
    payload_zipped = base64.b64decode(packed_payload)
    payload_content = gzip.decompress(payload_zipped)
    exec(payload_content)

if __name__ == "__main__":
    unpack()
''')

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python packer.py <payload_file.py> <packed_file.py>")
        sys.exit(1)

    payload_file = sys.argv[1]
    packed_file = sys.argv[2]

    pack(payload_file, packed_file)
    print(f"Packing completed. Packed file: {packed_file}")