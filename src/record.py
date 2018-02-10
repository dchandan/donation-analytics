import numpy as np
import pandas as pd

class Record(object):

    def __init__(self, rec_str):

        self.CMTE_ID = None
        self.NAME = None
        self.ZIP_CODE = None
        self.TRANSACTION_DT = None
        self.TRANSACTION_AMT = None
        self.OTHER_ID = None

        self.ID = None   # Record ID, we will construct this
        
        self._acceptable_cmtid = False
        self._acceptable_name = False
        self._acceptable_zip = False
        self._acceptable_date = False
        self._acceptable_amt = False
        self._acceptable = None

        self.__parse_record(rec_str)

    def __parse_record(self, rec_str):
        """
        Parses a record

        Args:
            rec (str) : record from streaming data
        Returns:
            Pandas
        """
        tokenized = rec_str.strip().split("|")

        self._acceptable = True
        
        try:
            self.CMTE_ID = tokenized[0]
            self._acceptable_cmtid = True
        except:
            pass
        
        try:
            self.NAME = tokenized[7]
            self._acceptable_name = True
        except:
            pass

        try:
            self.ZIP_CODE = tokenized[10][:5]
            self._acceptable_zip = True
        except:
            self.ZIP_CODE = ''

        try:
            self.TRANSACTION_DT = pd.to_datetime(tokenized[13], format='%m%d%Y', errors='raise')
            self._acceptable_date = True
        except:
            pass

        try:
            self.TRANSACTION_AMT = float(tokenized[14])
            self._acceptable_amt = True
        except:
            pass

        try:
            self.OTHER_ID = tokenized[15]
        except:
            self._acceptable = False
        
        self._acceptable = self._acceptable and self._acceptable_cmtid and self._acceptable_name and \
                           self._acceptable_zip and self._acceptable_date and self._acceptable_amt
        
        if self._acceptable:
            self.ID = self.NAME + self.ZIP_CODE

    def is_acceptable(self):
        """
        Checks if the record is acceptable according to rules of acceptability.

        Returns:
            True if record is sane, False otherwise
        """
        
        # If already something went wrong while parsing, then no need to check any
        # other further criteria
        if not self._acceptable:
            return self._acceptable
        
        # No name, bad data
        if not self.NAME:
            self._acceptable = False

        # Ignore, because this means contribution not from individual
        if self.OTHER_ID:
            self._acceptable = False

        # Bad zip code
        if len(self.ZIP_CODE) < 5:
            self._acceptable = False

        if not self.TRANSACTION_AMT:
            self._acceptable = False

        if not self.CMTE_ID:
            self._acceptable = False

        # The transaction data was not parsable
        # if pd.isnull(self.TRANSACTION_DT):
        #     self._acceptable = False

        return self._acceptable





