from pathlib import Path
import shutil
import pydicom


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
SOURCE_FILE = Path(__file__).with_name("META-005.dcm")


def create_missing_sop_instance_uid() -> Path:
    shutil.copy2(ORIGIN_FILE, SOURCE_FILE)

    ds = pydicom.dcmread(SOURCE_FILE)
    if "SOPInstanceUID" in ds:
        del ds.SOPInstanceUID
    ds.save_as(SOURCE_FILE)

    check = pydicom.dcmread(SOURCE_FILE)
    assert "SOPInstanceUID" not in check

    print(f"Updated source file with missing SOP Instance UID: {SOURCE_FILE}")
    return SOURCE_FILE


if __name__ == "__main__":
    create_missing_sop_instance_uid()
