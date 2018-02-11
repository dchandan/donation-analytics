from record import Record, BadRecord
from donors import Donors
from donations import RepeatDonations


class AnalyticsApp(object):

    def __init__(self, ofname, perc, verbosty=1):
        """
        Constructor
        
        :param ofname: output file name
        :param perc: percentile value (between 0 and 100)
        :param verbosty: how much diagnostics to produce
        """
        self._ofname = ofname
        self._perc = perc
        
        # A data structure containing (some) information about all donors
        self._all_donors = Donors()
        # A data structure containing (some) information about all repeat donations
        self._repeats = RepeatDonations()
        
        self._verbosity = verbosty
        
        if self._verbosity >= 1:
            print("Configuration:")
            print("  Output file: ", ofname)
            print("  Percentile : ", perc)

        self._ofile = open(self._ofname, "w")
    
    @property
    def perc(self):
        return self._perc
    
    @property
    def ofname(self):
        return self._ofname

    def update(self, recstr):
        """
        Updates its internal state with new donation information.
        
        :param recstr: the record in string format
        :return: None
        """
        if self._verbosity > 3:
            print(recstr)
        try:
            rec = Record(recstr)
        except BadRecord:
            return
        
        if self._all_donors.is_repeat_donor(rec):
            """
            This is a repeat donor.
            """
            if self._verbosity > 1:
                print("[AnalyticsApp.update] Repeat donor")
            self._repeats.insert(rec)
            
            # if rec.TRANSACTION_DT.year == 2017:
            self._print(rec)
        else:
            """
            We have not seen any previous instance of this donor donating to
            this committee. So, we insert this new information into the donors database.
            """
            self._all_donors.insert(rec)

    def _print(self, rec):
        """
        Print data to output file
        :param rec: obejct of class Record
        :return: None
        """
        self._ofile.write("{0}|{1}|{2}|{3}|{4}|{5}\n".format(
            rec.CMTE_ID,
            rec.ZIP_CODE,
            rec.TRANSACTION_DT.year,
            self._repeats[rec].percentile(self._perc),
            self._repeats[rec].total_amount,
            self._repeats[rec].num_donations(),
        ))

    def finalize(self):
        self._ofile.close()


def main(infname):
    """
    Main program
    :param infname: name of the input file
    :return:
    """

    # Load the percentile value
    perc = None
    with open("../input/percentile.txt", "r") as f:
        try:
            perc = float(f.readline())
        except:
            raise

    # Open the input stream
    itcontF = open(infname, "r")

    # Name of the output stream
    ofname = "../output/repeat_donors.txt"

    # Create the app
    App = AnalyticsApp(ofname, perc, 2)

    # Loop over all values in the stream
    for line in itcontF:
        App.update(line)

    App.finalize()


# main("../input/indiv18/testinsight.txt")
main("../input/indiv18/testyears.txt")
