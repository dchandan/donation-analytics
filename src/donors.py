
class Donors(object):

    def __init__(self):
        """
        Constructor
        """
        
        # This will contain (some) information on all donors.
        # NOTE: code is configured to contain the minimum amount of information
        # necessary to distinguish one donor from another while satisfying the
        # requirements of the challenge/
        self._donors = {}

    def insert(self, rec):
        """
        Records a donation. NOTE, by 'recording' it only stores the
        recipient ID, sender name and zip code of sender.

        :param rec: Object of class Record
        :return: None
        """
    
        NAME = rec.NAME
        ZIP_CODE = rec.ZIP_CODE
    
        if ZIP_CODE not in self._donors.keys():
            """
            A node corresponding to this zip code doesn't exist. Therefore create a new
            zip code node and populate it with a single child node whose
            key is this user's name, and value the contribution year.
            """
            self._donors[ZIP_CODE] = {NAME: [rec.TRANSACTION_DT.year]}
        else:
            if NAME not in self._donors[ZIP_CODE].keys():
                """
                No information about this specific user exists within this node. Create a
                new child node for this zip code.
                """
                self._donors[ZIP_CODE][NAME] = [rec.TRANSACTION_DT.year]
            else:
                """
                We already have a leaf node for this user. Update the list of years she has
                contributed.
                """
                self._donors[ZIP_CODE][NAME].append(rec.TRANSACTION_DT.year)

    def is_repeat_donor(self, rec):
        """
        Checks to see if we have any record of this individual, uniquely identified by
        zip code and name, previously donating to a specified committee.

        :param rec: Object of class Record
        :return: True if repeat donor, False otherwise
        """
        
        NAME = rec.NAME
        YEAR = rec.TRANSACTION_DT.year
        ZIP_CODE = rec.ZIP_CODE
    
        repeat_donor = False

        """
        Simply check if there exists a zip code-name path. If this raises error, then
        it means no previous information and obviously not a repeat donot. If it
        doesn't raise error then we check to see if any years on record for this user
        are for previous years.
        """
        try:
            years_contributed = self._donors[ZIP_CODE][NAME]
            for yr in years_contributed:
                if yr <= YEAR:
                    repeat_donor = True
                    break
        except KeyError:
            pass
    
        return repeat_donor
