from pathlib import Path
import shutil
import pydicom
from pydicom.uid import generate_uid


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
ORIGINAL_COPY = Path(__file__).with_name("MAP-008_original.dcm")  # Upload first (existing patient/study)
SOURCE_FILE = Path(__file__).with_name("MAP-008.dcm")  # Upload second (conflicting metadata)


def create_conflicting_patient_study() -> Path:
    shutil.copy2(ORIGIN_FILE, ORIGINAL_COPY)
    shutil.copy2(ORIGIN_FILE, SOURCE_FILE)

    ds = pydicom.dcmread(SOURCE_FILE)
    # Same StudyInstanceUID, but study now claims a different patient -> conflict
    ds.PatientID = "MAP-008-CONFLICT"
    ds.PatientName = "Conflict^Patient"
    ds.PatientBirthDate = "19000101"
    ds.PatientSex = "M" if ds.get("PatientSex") == "F" else "F"
    # New Series/Instance so it is not treated as a plain duplicate
    ds.SeriesInstanceUID = generate_uid()
    ds.SOPInstanceUID = generate_uid()
    ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
    ds.save_as(SOURCE_FILE)

    orig = pydicom.dcmread(ORIGIN_FILE)
    new = pydicom.dcmread(SOURCE_FILE)
    assert new.StudyInstanceUID == orig.StudyInstanceUID
    assert new.PatientID != orig.PatientID
    assert new.SOPInstanceUID != orig.SOPInstanceUID

    print(f"Original (upload 1st): {ORIGINAL_COPY}")
    print(f"Generated (upload 2nd): {SOURCE_FILE}")
    print(f"StudyInstanceUID (same): {new.StudyInstanceUID}")
    print(f"PatientID: {orig.PatientID} -> {new.PatientID}")
    return SOURCE_FILE


if __name__ == "__main__":
    create_conflicting_patient_study()
