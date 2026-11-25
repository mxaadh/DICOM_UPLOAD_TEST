from pathlib import Path
import pydicom
from pydicom.uid import generate_uid


ORIGIN_FILE = Path(__file__).parents[1] / "FILE-001" / "FILE-001.dcm"
OUT_DIR = Path(__file__).parent


def create_mixed_batch() -> None:
    for old in OUT_DIR.glob("*.dcm"):
        old.unlink()

    # Valid files: one new study/series, unique SOP UIDs (so not treated as duplicates)
    study_uid, series_uid = generate_uid(), generate_uid()

    def write_valid(name: str, instance_number: int, drop_sop: bool = False) -> None:
        ds = pydicom.dcmread(ORIGIN_FILE)
        ds.StudyInstanceUID = study_uid
        ds.SeriesInstanceUID = series_uid
        ds.SOPInstanceUID = generate_uid()
        ds.file_meta.MediaStorageSOPInstanceUID = ds.SOPInstanceUID
        ds.InstanceNumber = instance_number
        if drop_sop:
            del ds.SOPInstanceUID
        ds.save_as(OUT_DIR / name)

    raw = ORIGIN_FILE.read_bytes()

    # Invalid files placed between valid ones so we can see the batch is not aborted
    write_valid("01_VALID.dcm", 1)
    (OUT_DIR / "02_INVALID_empty.dcm").write_bytes(b"")
    write_valid("03_VALID.dcm", 2)
    (OUT_DIR / "04_INVALID_not_dicom.dcm").write_bytes(b"This is not a DICOM file.\n" * 50)
    write_valid("05_VALID.dcm", 3)
    (OUT_DIR / "06_INVALID_truncated.dcm").write_bytes(raw[:2000])
    write_valid("07_INVALID_missing_sop_uid.dcm", 4, drop_sop=True)
    write_valid("08_VALID.dcm", 5)

    files = sorted(OUT_DIR.glob("*.dcm"))
    assert len(files) == 8
    for f in files:
        print(f"{f.name:35} {f.stat().st_size:>10} bytes")
    print(f"\nExpected: 4 VALID stored (1 study, 1 series, 4 images), 4 INVALID skipped with per-file errors")


if __name__ == "__main__":
    create_mixed_batch()
