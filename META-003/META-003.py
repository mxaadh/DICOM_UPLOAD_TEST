from pathlib import Path
import shutil
import pydicom


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
SOURCE_FILE = Path(__file__).with_name("META-003.dcm")


def create_missing_study_instance_uid() -> Path:
    shutil.copy2(ORIGIN_FILE, SOURCE_FILE)

    ds = pydicom.dcmread(SOURCE_FILE)
    if "StudyInstanceUID" in ds:
        del ds.StudyInstanceUID
    ds.save_as(SOURCE_FILE)

    check = pydicom.dcmread(SOURCE_FILE)
    assert "StudyInstanceUID" not in check

    print(f"Updated source file with missing Study Instance UID: {SOURCE_FILE}")
    return SOURCE_FILE


if __name__ == "__main__":
    create_missing_study_instance_uid()