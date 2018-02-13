import sys
import os
import pytest
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'src'))

from record import Record
from donations import Donations, RepeatDonations


def test_constructor():
    d = Donations(45)
    assert(d.total_amount == 45)
    assert(d.num_donations() == 1)
    assert(d.donations == [45])


def test_adding_donations():
    d = Donations(45)
    d.add(10)
    assert(d.total_amount == 55)
    assert(d.num_donations() == 2)
    assert(d.donations == [10, 45])
    

@pytest.mark.parametrize("perc,answer", [
    (10, 10),
    (100, 320),
    (70, 194),
    (43, 80),
])
def test_percentile(perc, answer):
    d = Donations()
    for donation in [10, 40, 80, 50, 320, 200, 100, 172, 194]:
        d.add(donation)
    
    assert(d.percentile(perc) == answer)


def test_donation_equality_operator1():
    d1 = Donations(10)
    d2 = Donations(10)
    assert (d1 == d2)
    
    for i in range(5):
        randint = np.random.randint(1, 100)
        d1.add(randint)
        d2.add(randint)
    assert(d1 == d2)


def test_donation_equality_operator2():
    d1 = Donations()
    d2 = Donations()
    
    for i in range(5):
        d1.add(np.random.randint(1, 100))
        d2.add(np.random.randint(1, 100))
    assert(d1 != d2)


def test_repeat_donations_insert():
    R = RepeatDonations()

    records = [
        "C0A|||||||JOHN|||90017|||01032017|40||||||",
        "C1A|||||||JOHN|||90017|||01042017|10||||||",
        "C3A|||||||BOB|||50001|||01032012|40||||||",
        "C0A|||||||ALICE|||12345|||02032016|40||||||",
        "C0A|||||||CAT|||67129|||01012018|40||||||",
    ]

    for rec in records:
        R.insert(Record(rec))

    struct = {2012: {"C3A": {"50001": Donations(40)}},
              2016: {"C0A": {"12345": Donations(40)}},
              2017: {"C0A": {"90017": Donations(40)},
                     "C1A": {"90017": Donations(10)}},
              2018: {"C0A": {"67129": Donations(40)}}}
    
    assert(R._tree == struct)
