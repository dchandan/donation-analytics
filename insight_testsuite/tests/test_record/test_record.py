import sys
import os
import pytest
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'src'))

from record import Record


@pytest.mark.parametrize("record,verdict,value", [
    ("C00629618|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x", True, "C00629618"),
    ("|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x", True, "")
])
def test_parsing_CMTE_ID(record, verdict, value):
    rec = Record(record)
    assert(rec._acceptable_cmtid is verdict)
    if verdict is True:
        assert(rec.CMTE_ID == value)
    else:
        assert(rec._acceptable is False)


@pytest.mark.parametrize("record,verdict,value", [
    ("x|x|x|x|x|x|x|PEREZ, JOHN A|x|x|x|x|x|x|x|x|x|x|||x", True, "PEREZ, JOHN A"),
    ("x|x|x|x|x|x|x||x|x|x|x|x|x|x|x|x|x|||x", True, "")
])
def test_parsing_NAME(record, verdict, value):
    rec = Record(record)
    assert(rec._acceptable_name is verdict)
    if verdict is True:
        assert(rec.NAME == value)
    else:
        assert(rec._acceptable is False)


@pytest.mark.parametrize("record,verdict,value", [
    ("x|x|x|x|x|x|x|x|x|x|90017|x|x|x|x|x|x|x|||x", True, "90017"),
    ("x|x|x|x|x|x|x|x|x|x||x|x|x|x|x|x|x|||x", True, "")
])
def test_parsing_ZIP_CODE(record, verdict, value):
    rec = Record(record)
    assert(rec._acceptable_zip is verdict)
    if verdict is True:
        assert(rec.ZIP_CODE == value)
    else:
        assert(rec._acceptable is False)


@pytest.mark.parametrize("record,verdict", [
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|01032017|x|x|x|x|||x", True),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x||x|x|x|x|||x", False),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|junk|x|x|x|x|||x", False)
])
def test_parsing_TRANSACTION_DT(record, verdict):
    rec = Record(record)
    assert(rec._acceptable_date is verdict)
    if verdict is False:
        assert (rec._acceptable is False)


@pytest.mark.parametrize("record,verdict,value", [
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|x|40|x|x|x|||x", True, 40.0),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|x|0|x|x|x|||x", True, 0.0),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|x|31.2|x|x|x|||x", True, 31.2),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|x|14245.22|x|x|x|||x", True, 14245.22),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|x||x|x|x|||x", False, 0),
    ("x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|x|||x", False, 0),
])
def test_parsing_TRANSACTION_AMT(record, verdict, value):
    rec = Record(record)
    assert(rec._acceptable_amt is verdict)
    if verdict is True:
        assert(np.isclose(rec.TRANSACTION_AMT, value))
    else:
        assert(rec._acceptable is False)
