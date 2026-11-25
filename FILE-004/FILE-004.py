from pathlib import Path
import struct


SOURCE_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
OUTPUT_FILE = Path(__file__).with_name("FILE-004.dcm")
PIXEL_DATA_TAG = b"\xe0\x7f\x10\x00"


def create_corrupted_dicom() -> Path:
    data = bytearray(SOURCE_FILE.read_bytes())
    pixel_data_offset = data.find(PIXEL_DATA_TAG)

    if pixel_data_offset == -1:
        raise ValueError("Pixel Data tag was not found in the source DICOM file.")

    vr_offset = pixel_data_offset + 4
    vr = bytes(data[vr_offset : vr_offset + 2])
    if vr in {b"OB", b"OD", b"OF", b"OL", b"OV", b"OW", b"SQ", b"UC", b"UN", b"UR", b"UT"}:
        length_offset = vr_offset + 6
    else:
        # Implicit VR encodes the value length directly after the tag.
        length_offset = pixel_data_offset + 4
    declared_length = struct.unpack_from("<I", data, length_offset)[0]
    actual_length = len(data) - (length_offset + 4)
    if declared_length == 0xFFFFFFFF or actual_length <= 0:
        raise ValueError("Source DICOM has an unsupported or empty Pixel Data element.")

    corrupted_length = 0xFFFFFFFE
    struct.pack_into("<I", data, length_offset, corrupted_length)
    data[128:132] = b"BAD!"  # Corrupt "DICM" magic header
    del data[length_offset + 4 :]  # Truncate all pixel data
    OUTPUT_FILE.write_bytes(data)

    print(f"Generated corrupted DICOM: {OUTPUT_FILE}")
    print(f"Original Pixel Data length: {declared_length} bytes")
    print(f"Corrupted Pixel Data length: {corrupted_length} bytes")
    print(f"File size: {OUTPUT_FILE.stat().st_size} bytes")
    return OUTPUT_FILE


if __name__ == "__main__":
    create_corrupted_dicom()
