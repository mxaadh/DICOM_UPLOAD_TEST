import os

def create_zero_byte_file():
    file_name = "empty_image.dcm"
    
    # Ek empty file create karne ke liye usay 'write' mode mein open kar ke close kar dein
    open(file_name, 'w').close()
    
    # File ka size verify karein
    file_size = os.path.getsize(file_name)
    print(f"File '{file_name}' successfully generate ho gayi hai.")
    print(f"File Size: {file_size} bytes")

if __name__ == "__main__":
    create_zero_byte_file()