import argparse
from record import Record, BadRecord
from donors import Donors
from donations import RepeatDonations


class AnalyticsApp(object):

    def __init__(self, ofname, perc, verbosty=1):
        """
        Constructor
        
        :param ofname: output file name
        :param perc: percentile value (> 0 and <= 100)
        :param verbosty: how much diagnostics to produce
        """
        self._ofname = ofname
        self._perc = perc
        
        if (self._perc <= 0) or (self._perc > 100):
            raise ValueError("Invalid percentile value")
        
        if not isinstance(ofname, str):
            raise ValueError("Output filename must be a string")
        
        # A data structure containing (some) information about all donors
        self._all_donors = Donors()
        # A data structure containing (some) information about all repeat donations
        self._repeats = RepeatDonations()
        
        if not isinstance(verbosty, int):
            raise ValueError("Verbosity must be an integer")
        self._verbosity = verbosty
        
        if self._verbosity >= 1:
            print("Configuration:")
            print("  Output file: ", ofname)
            print("  Percentile : ", perc)

        self._ofile = open(self._ofname, "w")
    
    @property
    def perc(self):
        """
        Get the percentile value this app is configured with
        :return: percentile
        """
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
            
            self._print(rec)
        else:
            """
            We have not seen any previous instance of this donor donating to
            this committee. So, we insert this new information into the donors database.
            """
            self._all_donors.insert(rec)

    def _print(self, rec):
        """
        Write data to output file
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
        """
        Called by the user at the end of the app.
        :return: None
        """
        self._ofile.close()


def main(infname, percfile, ofname):
    """
    Main program
    :param infname: name of the input file
    :param percfile: name of the percentile file
    :param ofname: name of the output file
    :return: None
    """

    # Load the percentile value
    perc = None
    with open(percfile, "r") as f:
        try:
            perc = float(f.readline())
        except:
            raise

    # Open the input stream
    itcontF = open(infname, "r")

    # Create the app
    App = AnalyticsApp(ofname, perc, 2)

    # Loop over all values in the stream
    for line in itcontF:
        App.update(line)

    App.finalize()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("infname", type=str, help="input itcont filename")
    parser.add_argument("percfile", type=str, help="filename of the percentile file")
    parser.add_argument("ofname", type=str, help="output filename")
    args = parser.parse_args()
    
    main(args.infname, args.percfile, args.ofname)

