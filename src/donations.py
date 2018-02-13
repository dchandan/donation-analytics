import numpy as np


class Donations(object):
    """
    Class that helps collect a number of different donations
    """
    def __init__(self, amt=None):
        """
        Constructor
        :param amt: donation amount (optional)
        """
        self._donations = []  # will contain a sorted list of donations
        self._total_amount = 0
        
        if amt is not None:
            self.add(amt)
    
    @property
    def donations(self):
        return self._donations
    
    @property
    def total_amount(self):
        """
        Get the total amount of donations made
        :return: total donation amount
        """
        return self._total_amount
    
    def num_donations(self):
        """
        Get the number of donations made.
        :return: number of donations
        """
        return len(self._donations)
    
    def add(self, amt):
        """
        Add a new donation.
        :param amt: value of donation
        :return: None
        """
        
        # Round the amount and convert it to integer. It appears from the challenge description
        # that we want to deal with rounded integers.
        amt = int(np.round(amt))
        self._donations.append(amt)
        # Sort the list because the nearest rank percentile method expects a sorted list.
        self._donations.sort()
        self._total_amount += amt
    
    def percentile(self, perc):
        """
        Return a percentile of the donations calculated using the nearest rank method.
        :param perc:
        :return:
        """
        
        # compute the "ordinal rank" first
        n = int(np.ceil((perc/100) * self.num_donations())) - 1
        # return data at that ordinal rank
        return self._donations[n]
    
    def __eq__(self, other):
        """
        Equality comparison operator.
        :param other: another object of class Donations
        :return: True if both objects have the same donations
        """
        return self._donations == other._donations
    

class RepeatDonations(object):
    def __init__(self):
        """
        Constructor.
        """
        self._tree = {}
    
    def insert(self, rec):
        """
        Records a donation. NOTE, by 'recording' it only stores the
        recipient ID, sender name and zip code of sender.

        :param rec: Object of class Record
        :return: None
        """
        
        YEAR = rec.TRANSACTION_DT.year
        CMTE_ID = rec.CMTE_ID
        ZIP_CODE = rec.ZIP_CODE
        TRANSACTION_AMT = rec.TRANSACTION_AMT
        
        if YEAR not in self._tree.keys():
            """
            This year node doesn't exist. Therefore create a new year node and
            fill it with its complete sub-tree.
            """
            self._tree[YEAR] = {CMTE_ID: {ZIP_CODE: Donations(TRANSACTION_AMT)}}
        else:
            if CMTE_ID not in self._tree[YEAR].keys():
                """
                The year node exists, but it doesn't have a child node given by
                this committee id. Create this child node and insert data into it.
                """
                self._tree[YEAR][CMTE_ID] = {ZIP_CODE: Donations(TRANSACTION_AMT)}
            else:
                if ZIP_CODE not in self._tree[YEAR][CMTE_ID].keys():
                    self._tree[YEAR][CMTE_ID][ZIP_CODE] = Donations(TRANSACTION_AMT)
                else:
                    self._tree[YEAR][CMTE_ID][ZIP_CODE].add(TRANSACTION_AMT)
                    
    def __getitem__(self, rec):
        """
        Get a donations class object if a repeat donation exists with the specific
        information in this record.
        :param rec: Record class object
        :return: Donation class object
        :raise: KeyError
        """
        YEAR = rec.TRANSACTION_DT.year
        CMTE_ID = rec.CMTE_ID
        ZIP_CODE = rec.ZIP_CODE
        
        return self._tree[YEAR][CMTE_ID][ZIP_CODE]
