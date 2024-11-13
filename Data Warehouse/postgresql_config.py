from typing import Dict
from configparser import ConfigParser


class ReadFromConfig:
    def __init__(self, filename: str, section: str) -> None:
        self.filename = filename
        self.section = section
    
    def read_from_config(self) -> Dict:
        parser = ConfigParser()
        parser.read(self.filename)

        db = {}
        if parser.has_section(self.section):
            items = parser.items(self.section)
            for item in items:
                db[item[0]] = item[1]
        else:
            raise Exception(f'{self.section} not found in the {self.filename} file')
        
        return db
