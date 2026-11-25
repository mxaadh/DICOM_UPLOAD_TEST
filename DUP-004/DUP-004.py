from pathlib import Path


SOURCE_FILE = Path(__file__).with_name("DUP-004.dcm")
OUTPUT_FILE = Path(__file__).with_name("DUP-004_modified.dcm")


def create_same_uid_different_bytes() -> Path:
    data = bytearray(SOURCE_FILE.read_bytes())
    data[-1] ^= 0xFF  # Flip last pixel byte: same SOP Instance UID, different bytes/hash
    OUTPUT_FILE.write_bytes(data)

    assert SOURCE_FILE.read_bytes() != OUTPUT_FILE.read_bytes()
    print(f"Source file: {SOURCE_FILE} ({len(data)} bytes)")
    print(f"Generated file: {OUTPUT_FILE} (same SOP Instance UID, different bytes)")
    return OUTPUT_FILE


if __name__ == "__main__":
    create_same_uid_different_bytes()
