import pandas
import os
from pathlib import Path


class File():
    def __init__(self) -> None:
        self.data_frame = None
        p = os.getcwd()
        self.files = os.listdir(p)
        self.select_cat = ['name','price','id','picture','url']
        self.csv_file = ""
        for file in self.files:
            suf = Path(file).suffix
            if suf == ".csv":
                try:
                    self.data_frame = pandas.concat([self.data_frame, pandas.read_csv(file,delimiter=";")])
                except:
                    self.data_frame = pandas.read_csv(file,delimiter=";")            
            elif suf == ".xml":
                pass
                # self.xml_file = ""
        
        
       
        
    def search(self,txt):
        data_search = self.data_frame[self.data_frame.available.eq(True)]
        data_search = data_search.loc[data_search.eq(txt).any(1) , self.select_cat]
        # return self.data_frame.loc[(self.data_frame.typePrefix==txt) & (self.data_frame.available==True), self.select_cat]
        return tuple(data_search.itertuples(index=False))
             
        

#xml = File().data_frame
#print(xml)