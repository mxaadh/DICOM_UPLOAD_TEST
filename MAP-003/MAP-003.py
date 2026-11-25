from pathlib import Path
import shutil
import pydicom
from pydicom.uid import generate_uid


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
ORIGINAL_COPY = Path(__file__).with_name("MAP-003_original.dcm")  # Upload first (existing patient)
SOURCE_FILE = Path(__file__).with_name("MAP-003.dcm")  # Upload second (new study)


def create_new_study_existing_patient() -> Path:
    shutil.copy2(ORIGIN_FILE, ORIGINAL_COPY)
    shutil.copy2(ORIGIN_FILE, SOURCE_FILE)

    ds = pydicom.dcmread(SOURCE_FILE)
    # Same patient (PatientID/PatientName untouched); new Study/Series/Instance UIDs
    ds.StudyInstanceUID = generate_uid()
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()
    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    ds.save_as(SOURCE_FILE)

    orig = pydicom.dcmread(ORIGIN_FILE)
    new = pydicom.dcmread(SOURCE_FILE)
    assert new.PatientID == orig.PatientID and new.PatientName == orig.PatientName
    assert new.StudyInstanceUID != orig.StudyInstanceUID
    assert new.SeriesInstanceUID != orig.SeriesInstanceUID
    assert new.SOPInstanceUID != orig.SOPInstanceUID

    print(f"Original (upload 1st): {ORIGINAL_COPY}")
    print(f"Generated (upload 2nd): {SOURCE_FILE}")
    print(f"PatientID (same): {new.PatientID}")
    print(f"StudyInstanceUID (new): {new.StudyInstanceUID}")
    return SOURCE_FILE


if __name__ == "__main__":
    create_new_study_existing_patient()
