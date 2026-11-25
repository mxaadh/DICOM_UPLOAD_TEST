from pathlib import Path
import shutil
import pydicom


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
SOURCE_FILE = Path(__file__).with_name("DUP-009.dcm")
OUTPUT_FILE = Path(__file__).with_name("DUP-009_other_patient.dcm")


def create_same_uid_another_patient() -> Path:
    shutil.copy2(ORIGIN_FILE, SOURCE_FILE)

    ds = pydicom.dcmread(SOURCE_FILE)
    ds.PatientID = "PATIENT-009-OTHER"
    ds.PatientName = "Other^Patient"
    ds.save_as(OUTPUT_FILE)

    orig = pydicom.dcmread(SOURCE_FILE)
    mod = pydicom.dcmread(OUTPUT_FILE)
    assert orig.SOPInstanceUID == mod.SOPInstanceUID
    assert orig.PatientID != mod.PatientID

    print(f"Copied source: {SOURCE_FILE} (PatientID: {orig.PatientID})")
    print(f"Generated: {OUTPUT_FILE} (PatientID: {mod.PatientID}, SOPInstanceUID: {mod.SOPInstanceUID})")
    return OUTPUT_FILE


if __name__ == "__main__":
    create_same_uid_another_patient()
