import subprocess
import argparse

def extract_encrypted_section(input_file, output_file, skip):
    with open(input_file, 'rb') as infile, open(output_file, 'wb') as outfile:
        infile.seek(skip)
        while True:
            chunk = infile.read(4096)
            if not chunk:
                break
            outfile.write(chunk)

def decrypt_file(password, input_file, output_file, salt):
    command = [
        'openssl', 'enc', '-d', '-aes-256-cbc',
        '-in', input_file, '-out', output_file,
        '-salt', '-pbkdf2', '-pass', f'pass:{password}',
        '-S', salt
    ]
    result = subprocess.run(command, capture_output=True)
    return result.returncode == 0

def main(input_file, decrypted_file, salt, dictionary, skip):
    temp_encrypted_file = 'encrypted.bin'
    extract_encrypted_section(input_file, temp_encrypted_file, skip)

    with open(dictionary, 'r', encoding='utf-8', errors='ignore') as file:
        for line in file:
            password = line.strip()
            if decrypt_file(password, temp_encrypted_file, decrypted_file, salt):
                print(f"Password found: {password}")
                break
            else:
                with open('decrypt.log', 'a') as log_file:
                    log_file.write(f"Attempt with password: {password} failed\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract encrypted section and decrypt a file using a dictionary attack.")
    parser.add_argument('input_file', help="The input file containing the encrypted data.")
    parser.add_argument('decrypted_file', help="The output file for the decrypted data.")
    parser.add_argument('salt', help="The salt used in the encryption.")
    parser.add_argument('dictionary', help="The dictionary file containing potential passwords.")
    parser.add_argument('skip', type=int, help="The number of bytes to skip in the input file before extracting.")

    args = parser.parse_args()
    
    main(args.input_file, args.decrypted_file, args.salt, args.dictionary, args.skip)
