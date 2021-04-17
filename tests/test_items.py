from hz_rc_archive.items import HzRcArchiveItem


def test_item():
    item = HzRcArchiveItem()
    assert len(item.fields) == 6
