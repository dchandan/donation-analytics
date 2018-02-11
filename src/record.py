import pandas as pd
import numpy as np


class BadRecord(Exception):
    pass


class Record(object):

    def __init__(self, rec_str):
        """
        Create a new record.
        :param rec_str: record string from streaming data
        """

        self.CMTE_ID = None
        self.NAME = None
        self.ZIP_CODE = None
        self.TRANSACTION_DT = None
        self.TRANSACTION_AMT = None
        self.OTHER_ID = None

        self.ID = None   # Record ID, we will construct this
        
        self.__parse_record(rec_str)

    def __parse_record(self, rec_str):
        """
        Parses a record string.
        
        :param rec_str: record from streaming data
        :return: None
        """
        tokenized = rec_str.strip().split("|")

        try:
            self.CMTE_ID = tokenized[0]
            self.NAME = tokenized[7]
            self.ZIP_CODE = tokenized[10][:5]
            self.TRANSACTION_DT = pd.to_datetime(tokenized[13], format='%m%d%Y', errors='raise')
            self.TRANSACTION_AMT = np.round(float(tokenized[14]))
            self.OTHER_ID = tokenized[15]
        except (IndexError, ValueError):
            raise BadRecord
        
        self.__check_acceptable()
        
        self.ID = self.NAME + self.ZIP_CODE

    def __check_acceptable(self):
        """
        Checks if the record is acceptable according to rules of acceptability.

        :return: None
        """
        
        # No name, bad data
        if not self.NAME:
            raise BadRecord
        
        # Name is a numeric value
        if self.NAME.isdigit():
            raise BadRecord

        # Ignore, because this means contribution not from individual
        if self.OTHER_ID:
            raise BadRecord

        # Bad zip code
        if len(self.ZIP_CODE) < 5:
            raise BadRecord

        if not self.CMTE_ID:
            raise BadRecord
