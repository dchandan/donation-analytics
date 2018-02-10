from record import Record



class AnalyticsApp(object):

    def __init__(self, ofname, perc):
        """
        Args:
            ofname (str) : output file name
            perc (float): percentile
        """
        self._ofname = ofname
        self._perc = perc
        
        print("Configuration:")
        print("  Output file: ", ofname)
        print("  Percentile : ", perc)

        self._ofile = open(self._ofname, "w")

    def __call__(self, rec):
        rec = Record(rec)
        print(rec.CMTE_ID)

    def finalize(self):
        self._ofile.close()



def main():

    # Load the percentile value
    perc = None
    with open("../input/percentile.txt", "r") as f:
        try:
            perc = float(f.readline())
        except:
            raise

    # Open the input stream
    itcontF = open("../input/indiv18/itcont.txt", "r")


    # Name of the output stream
    ofname = "../output/repeat_donors.txt"

    # Create the app
    App = AnalyticsApp(ofname, perc)

    # Loop over all values in the stream
    for line in itcontF:
        App(line)

    App.finalize()


main()
