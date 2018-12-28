import os 
import wfdb
import numpy as np
import matplotlib.pyplot as plt 




class PhysioInterface(object):
    def __init__(self):
        
        self.records = {}

    def load_record(self, filename, **kwargs):
        
        record = wfdb.rdrecord(filename, **kwargs)
                   
        if record.record_name in self.records:
            print(f'Record {record.record_name} already exists. Writing over existing record.')
            self.records[record.record_name] = record
        else:
            self.records[record.record_name] = record

    def get_record(self, record_name):
        self.__exist_in_local(record_name, self.records)
        return self.records[record_name]

    def list_records(self):
        print('########################################')
        print('#         Printing all records         #')
        print('########################################')
        for k, v in self.records.items():
            print(f'Record {k}')

    def get_records(self):
        return self.records

    def download_records(self, database_name, download_dir):
        try:
            wfdb.dl_database(database_name, dl_dir=download_dir)
        except Exception as error:
            raise error

    def get_signal(self, record_name):
        self.__exist_in_local(record_name, self.records)
        return self.records[record_name].p_signal

    def __exist_in_local(self, target, source):
        try:
            assert (target in source)
        except AssertionError:
            raise AssertionError(f'Record {target} does not exist. Please load record first.')
        




if __name__ == '__main__':
    pass
