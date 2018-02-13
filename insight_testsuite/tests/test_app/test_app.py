import sys
import os
import pytest

sys.path.append(os.path.join(os.path.dirname(__file__), '../../../', 'src'))

from app import main, AnalyticsApp


@pytest.mark.parametrize("infile,ofile,checkfile", [
    ("input1.txt", "output1.txt", "output1_reference.txt"),
    ("input2.txt", "output2.txt", "output2_reference.txt")
])
def test_app(infile, ofile, checkfile):
    direc = os.path.dirname(__file__)
    main(os.path.join(direc, "input", infile), os.path.join(direc, "input", "percentile.txt"), os.path.join(direc, "output", ofile))
    assert(open(os.path.join(direc, "output", ofile), "r").readlines() == open(os.path.join(direc, "output", checkfile), "r").readlines())


def test_invalid_percentile():
    with pytest.raises(ValueError):
        AnalyticsApp("somefile", 0)
    
    with pytest.raises(ValueError):
        AnalyticsApp("somefile", -20)

    with pytest.raises(ValueError):
        AnalyticsApp("somefile", 101)


def test_invalid_ofname():
    with pytest.raises(ValueError):
        AnalyticsApp(45, 30)


def test_invalid_verbosity():
    with pytest.raises(ValueError):
        AnalyticsApp("somefilename", 30, "sdgs")
