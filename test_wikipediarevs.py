import json
import pytest
import shutil
import pathlib

from wikipediarevs import RevisionDownloader

output = pathlib.Path("test_output")

@pytest.fixture(autouse=True)
def remove_test_data():
    if output.is_dir():
        shutil.rmtree(output)

def test_download():
    rd = RevisionDownloader(["https://en.wikipedia.org/wiki/BagIt"], output_dir="test_output", quiet=True)
    rd.run()

    revs_dir = output / "en.wikipedia.org" / "BagIt"
    assert revs_dir.is_dir()
    assert len(list(revs_dir.iterdir())) > 0

    rev = json.load((revs_dir / "390446530.json").open())
    assert rev["revid"] == 390446530

def test_update():
    rd = RevisionDownloader(["https://en.wikipedia.org/wiki/BagIt"], output_dir="test_output", quiet=True)
    rd.run()

    revs_dir = output / "en.wikipedia.org" / "BagIt"
    revs = sorted(revs_dir.iterdir(), key=lambda p: int(p.name.replace(".json", "")), reverse=True)

    # remove remove all revision files execpt for the 2nd which should 
    # trick wikipediarevs to only download revisions since that 2nd one
    revs.pop(1)
    for rev in revs:
        rev.unlink()

    # running again should fill in up to the latest on disk, but not more
    rd.run()
    assert len(list(revs_dir.iterdir())) == 2
