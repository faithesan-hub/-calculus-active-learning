"""Step 1: get the raw data and confirm it is the exact file the analysis used.

Plain-language note: this script checks that the three files from the original
study are present in data/raw/kramer2023/ and are byte-for-byte identical to the
copies used for this analysis (a "fingerprint" check). If you do not have them,
it tries to download them from Zenodo. You do not need to open this file.

Source: Kramer L, Fuller E, Watson C, Castillo A, Duran Oliva P, Potvin G (2023).
Establishing a new standard of care for calculus using trials with randomized
student allocation [dataset]. Dryad / Zenodo. https://doi.org/10.5061/dryad.kkwh70s95
"""
import hashlib
import pathlib
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "kramer2023"
BASE = "https://zenodo.org/records/8306160/files/{}?download=1"
EXPECTED = {
    "anonymizedarchive.csv": "5465e2026f941d0f1d23ce724b40456b6d8db50f3d06ced7274da6b1fbd57a3f",
    "CodeBookPublic.csv": "7262835c352a998631331c0cdacdceeeabb4b845787d0a91538b36b9c51fa546",
    "README.md": "d2dd47ed4f2c7af63a391a48bc072af79c3b976b602da7eeb6591e74da66061b",
}


def sha256(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    RAW.mkdir(parents=True, exist_ok=True)
    ok = True
    for name, want in EXPECTED.items():
        p = RAW / name
        if not p.exists():
            print(f"{name}: missing, downloading from Zenodo")
            try:
                urllib.request.urlretrieve(BASE.format(name), p)
            except Exception as e:  # network blocked or record moved
                print(f"  could not download ({e}). Download it by hand from "
                      "https://zenodo.org/records/8306160 and put it in data/raw/kramer2023/")
                ok = False
                continue
        got = sha256(p)
        status = "OK" if got == want else "DIFFERENT FILE"
        ok &= got == want
        print(f"{name}: {status} (sha256 {got[:16]}...)")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
