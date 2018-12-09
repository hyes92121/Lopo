import os 
import wfdb
import numpy as np
import matplotlib.pyplot as plt 




class PhysioInterface(object):
    def __init__(self):
        
        self.records = {}

    def read_record(self, filename, custom_name=None):
        try:
            assert os.path.exists(filename)
        except AssertionError:
            raise AssertionError(f'Record {filename} does not exist.')
        
        record = wfdb.rdrecord(filename, smooth_frames=True)
                   
        if record.record_name in self.records:
            print(f'Record {record.record_name} already exists. Writing over existing record.')
            self.records[record.record_name] = record

    def get_record(self, record_name):
        try:
            assert record_name in self.records
        except AssertionError:
            raise AssertionError(f'Record {record_name} does not exist. Please read the record first.')
            
        return self.records[record_name]

    def list_records(self):
        print('########################################')
        print('#         Printing all records         #')
        print('########################################')
        for k, v in self.records.items():
            print(f'Record {k}')

    def get_records(self):
        return self.records

    def download_records(self, url):
        pass




if __name__ == '__main__':
    pass
