import sys
import os
import pytest
import pandas as pd

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'src'))

from record import Record, BadRecord


@pytest.mark.parametrize("record,isGood,value", [
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", True, "C00384516"),
    ("|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", False, None)
])
def test_parsing_CMTE_ID(record, isGood, value):
    if isGood:
        rec = Record(record)
        print(rec.CMTE_ID)
        assert(rec.CMTE_ID == value)
    else:
        with pytest.raises(BadRecord):
            rec = Record(record)
    

@pytest.mark.parametrize("record,isGood,value", [
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", True, "SABOURIN, JOE"),
    ("C00384516|x|x|x|x|x|x||x|x|028956146|x|x|01312016|484||x|x||x|x", False, None),
    ("C00384516|x|x|x|x|x|x|4567|x|x|028956146|x|x|01312016|484||x|x||x|x", False, None)
])
def test_parsing_NAME(record, isGood, value):
    if isGood:
        rec = Record(record)
        assert (rec.NAME == value)
    else:
        with pytest.raises(BadRecord):
            rec = Record(record)


@pytest.mark.parametrize("record,isGood,value", [
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", True, "02895"),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|02895|x|x|01312016|484||x|x||x|x", True, "02895"),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x||x|x|01312016|484||x|x||x|x", False, None),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|038|x|x|01312016|484||x|x||x|x", False, None)
])
def test_parsing_ZIP_CODE(record, isGood, value):
    if isGood:
        rec = Record(record)
        assert(rec.ZIP_CODE == value)
    else:
        with pytest.raises(BadRecord):
            rec = Record(record)


@pytest.mark.parametrize("record,isGood,date", [
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", True, "01-31-2016"),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x||484||x|x||x|x", False, None),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|31012016|484||x|x||x|x", False, None)
])
def test_parsing_TRANSACTION_DT(record, isGood, date):
    if isGood:
        rec = Record(record)
        assert(rec.TRANSACTION_DT == pd.to_datetime(date))
    else:
        with pytest.raises(BadRecord):
            rec = Record(record)


@pytest.mark.parametrize("record,isGood,value", [
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", True, 484),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|0.0||x|x||x|x", False, 0),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|32.1||x|x||x|x", True, 32),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|32.51||x|x||x|x", True, 33),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|14245.22||x|x||x|x", True, 14245),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|blah||x|x||x|x", False, None),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|||x|x||x|x", False, None),
])
def test_parsing_TRANSACTION_AMT(record, isGood, value):
    if isGood:
        rec = Record(record)
        assert(rec.TRANSACTION_AMT == value)
    else:
        with pytest.raises(BadRecord):
            rec = Record(record)


@pytest.mark.parametrize("record,isGood", [
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x", True),
    ("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484|otherid|x|x||x|x", False),
])
def test_parsing_OTHER_ID(record, isGood):
    if isGood:
        rec = Record(record)
        assert(rec.OTHER_ID == "")
    else:
        with pytest.raises(BadRecord):
            rec = Record(record)


def test_ID():
    rec = Record("C00384516|x|x|x|x|x|x|SABOURIN, JOE|x|x|028956146|x|x|01312016|484||x|x||x|x")
    assert(rec.ID == "SABOURIN, JOE02895")
