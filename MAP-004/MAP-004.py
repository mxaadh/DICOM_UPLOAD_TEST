from pathlib import Path
import shutil
import pydicom
from pydicom.uid import generate_uid


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
ORIGINAL_COPY = Path(__file__).with_name("MAP-004_original.dcm")  # Upload first (existing study)
SOURCE_FILE = Path(__file__).with_name("MAP-004.dcm")  # Upload second (new series)


def create_new_series_existing_study() -> Path:
    shutil.copy2(ORIGIN_FILE, ORIGINAL_COPY)
    shutil.copy2(ORIGIN_FILE, SOURCE_FILE)

    ds = pydicom.dcmread(SOURCE_FILE)
    # Same patient + same StudyInstanceUID; new Series/Instance UIDs
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()
    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    if "SeriesNumber" in ds:
        ds.SeriesNumber = int(ds.SeriesNumber or 0) + 1
    ds.save_as(SOURCE_FILE)

    orig = pydicom.dcmread(ORIGIN_FILE)
    new = pydicom.dcmread(SOURCE_FILE)
    assert new.PatientID == orig.PatientID
    assert new.StudyInstanceUID == orig.StudyInstanceUID
    assert new.SeriesInstanceUID != orig.SeriesInstanceUID
    assert new.SOPInstanceUID != orig.SOPInstanceUID

    print(f"Original (upload 1st): {ORIGINAL_COPY}")
    print(f"Generated (upload 2nd): {SOURCE_FILE}")
    print(f"StudyInstanceUID (same): {new.StudyInstanceUID}")
    print(f"SeriesInstanceUID (new): {new.SeriesInstanceUID}")
    return SOURCE_FILE


if __name__ == "__main__":
    create_new_series_existing_study()
