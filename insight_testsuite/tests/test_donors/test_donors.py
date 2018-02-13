import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'src'))

from donors import Donors
from record import Record


def test_insert():
    D = Donors()
    rec = Record("C00629618|||||||PEREZ, JOHN A|||90017|||01032017|40||||||")
    D.insert(rec)
    assert(D._donors == {'90017': {'PEREZ, JOHN A': [2017]}})

    rec = Record("C00629618|||||||PEREZ, JOHN A|||90017|||01022012|40||||||")
    D.insert(rec)
    assert (D._donors == {'90017': {'PEREZ, JOHN A': [2017, 2012]}})

    rec = Record("xyz|||||||CHANDAN, DEEPAK|||90017|||01022011|40||||||")
    D.insert(rec)
    assert (D._donors == {'90017': {'PEREZ, JOHN A': [2017, 2012], 'CHANDAN, DEEPAK': [2011]}})

    rec = Record("xyz|||||||someone|||34567|||01022018|40||||||")
    D.insert(rec)
    assert (D._donors == {'90017': {'PEREZ, JOHN A': [2017, 2012], 'CHANDAN, DEEPAK': [2011]},
                          '34567': {'someone': [2018]}})


# def test_repeat_donor():
#     D = Donors()
#     records = [Record("C00629618|||||||PEREZ, JOHN A|||90017|||01032017|40||||||"),
#                ]
