import datetime

from enum import Enum

class Drink:
    def __init__(self, data):
        if self.validate(data):
            self.id = data.id
            self.name = data.name
            self.drink_type = data.drink_type
            self.date_enjoyed = data.date_enjoyed
            self.desc = data.desc
        
        if data.sake_type is not None or type(data.sake_type) in SakeType:
            self.sake_type = data.sake_type
        else:
            self.sake_type = SakeType.NONE

    def validate(data):
        if data is None:
            return False
        if type(data.id) != int:
            return False
        if data.name is None or type(data.name) != str:
            return False
        if data.drink_type is None or type(data.drink_type) not in DrinkType:
            return False
        if data.date_enjoyed is None or isinstance(data.date_enjoyed, datetime):
            return False
        if data.desc is None or type(data.desc) != str:
            return False
        return True
        
    def post_drink_query(self):
        return '''
        INSERT INTO t_drink (c_name, c_drink_type, c_sake_type, c_date_enjoyed, c_desc) 
        VALUES ({self.name}, {self.drink_type}, {self.sake_type}, {self.date_enjoyed}, {self.desc})
        '''

    def get_drink_query(id):
        return f"SELECT c_name, c_drink_type, c_sake_type, c_date_enjoyed, c_desc, c_image_url FROM t_drinks WHERE c_id={id}"
    
    def get_drinks_query(limit, offset):
        return f"SELECT c_id, c_name, c_type, c_date_crafted, c_image_url FROM t_drink LIMIT {limit} OFFSET {offset}"


class DrinkType(Enum):
    OTHER = 0
    SAKE = 1
    SPIRIT = 2
    WINE = 3
    BEER = 4

class SakeType(Enum):
    NONE = 0
    FUTSUSHU_HONJOZO = 1
    GINJO_TOKUBETSU = 2
    DAIGINJO = 3
    JUNMAI = 4
    SPECIALTY = 5
