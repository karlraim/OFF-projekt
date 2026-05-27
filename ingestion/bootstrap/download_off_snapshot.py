from pathlib import Path
from datetime import datetime
import json
import requests

SNAPSHOT_URL = (
    "https://static.openfoodfacts.org/data/"
    "en.openfoodfacts.org.products.csv.gz"
)

SNAPSHOT_DIR = Path(
    "data/snapshots"
)

METADATA_PATH = Path(
    "data/snapshots/snapshot_metadata.json"
)


def load_metadata():
    if not METADATA_PATH.exists():
        return {}

    if METADATA_PATH.stat().st_size == 0:
        return {}

    try:
        with open(METADATA_PATH, "r") as f:
            return json.load(f)

    except json.JSONDecodeError:
        print(
            "Metadata fail on vigane. "
            "Ignoreerin olemasolevat metadata faili."
        )

        return {}


def get_snapshot_filename(download_date):
    """
    Näide:
    en.openfoodfacts.org.products_2026-05-27.csv.gz
    """

    return (
        f"en.openfoodfacts.org.products_"
        f"{download_date}.csv.gz"
    )


def get_snapshot_path(download_date):
    return SNAPSHOT_DIR / get_snapshot_filename(
        download_date
    )


def save_metadata(download_date):
    metadata = {
        "downloaded_at": download_date,
        "source_url": SNAPSHOT_URL,
        "snapshot_filename": get_snapshot_filename(
            download_date
        ),
    }

    with open(METADATA_PATH, "w") as f:
        json.dump(metadata, f, indent=2)


def should_redownload():
    metadata = load_metadata()

    previous_date = metadata.get("downloaded_at")

    today = datetime.utcnow().date().isoformat()

    if previous_date == today:
        answer = input(
            "Tänane snapshot on juba olemas. "
            "Kas soovid seda uuesti alla laadida? [y/N]: "
        )

        return answer.lower() == "y"

    return True


def download_snapshot():
    # Loo vajadusel data/snapshots kaust
    SNAPSHOT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    download_date = (
        datetime.utcnow()
        .date()
        .isoformat()
    )

    snapshot_path = get_snapshot_path(
        download_date
    )

    # Katkesta kui sama päeva snapshot on olemas
    # ja kasutaja ei kinnita uuendamise vajadust
    if not should_redownload():
        print(
            "Snapshoti allalaadimine katkestatud"
        )

        return

    headers = {
        "User-Agent": "OFF-Estonia-Analytics/1.0"
    }

    response = requests.get(
        SNAPSHOT_URL,
        stream=True,
        timeout=60,
        headers=headers,
    )

    response.raise_for_status()

    # Salvesta fail chunk-idena
    # Väldib kogu faili vahemällu laadimist
    with open(snapshot_path, "wb") as f:

        for chunk in response.iter_content(
            chunk_size=1024 * 1024
        ):
            f.write(chunk)

    save_metadata(download_date)

    print(
        f"Snapshot alla laaditud: "
        f"{snapshot_path}"
    )


if __name__ == "__main__":
    download_snapshot()