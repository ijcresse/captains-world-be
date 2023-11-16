import dateutil.parser

from enum import Enum

class Drink:
    def __init__(self, data):
        if self.validate(data):
            if 'id' in data:
                self.id = data['id']
            self.name = data['name']
            self.drink_type = data['drink_type']
            self.date_enjoyed = data['date_enjoyed']
            self.date_crafted = data['date_crafted']
            self.desc = data['desc']
        else:
            raise Exception('Missing or malformed parameters')

        if data['sake_type'] is not None or type(data['sake_type']) in SakeType:
            self.sake_type = data['sake_type']
        else:
            self.sake_type = SakeType.NONE

    def validate(self, data):
        errors = []
        if data is None:
            errors.append('Data object missing')
            return False
        # if data['id'] is None or type(data['id']) != int: #wait. we dont want to stop if we dont have an ID, necessarily
        #     errors.append('ID missing or malformed')
        if 'name' not in data or type(data['name']) != str:
            errors.append('Name missing or malformed')
        if 'drink_type' not in data or data['drink_type'].upper() not in DrinkType.__members__:
            errors.append('Drink type missing or malformed')
        if 'date_crafted' not in data or not self.validate_iso_date(data['date_crafted']):
            errors.append("DateCrafted missing or malformed")
        if 'date_enjoyed' not in data or not self.validate_iso_date(data['date_enjoyed']):
            errors.append("DateEnjoyed missing or malformed")
        if 'desc' not in data or type(data['desc']) != str:
            errors.append("Description missing or malformed")
        if len(errors) > 0:
            print(errors) #TODO log this properly
            return False
        return True

    def validate_iso_date(self, data):
        try:
            dateutil.parser.isoparse(data)
        except ValueError:
            print('LOG THIS: DateEnjoyed string is malformed')
            return False
        return True

    def post_drink_query(self):
        return f"INSERT INTO t_drink (c_name, c_drink_type, c_sake_type, c_date_crafted, c_date_enjoyed, c_description) VALUES ('{self.name}', '{self.drink_type}', '{self.sake_type}', '{self.date_crafted}', '{self.date_enjoyed}', '{self.desc}')"

    @staticmethod
    def post_drink_image_query(filename, id):
        return f"UPDATE t_drink SET c_image_url='{filename}' WHERE c_id={id}"

    @staticmethod
    def get_drink_query(id):
        return f"SELECT c_name, c_drink_type, c_sake_type, c_date_enjoyed, c_date_crafted, c_description, c_image_url FROM t_drink WHERE c_id={id}"

    @staticmethod
    def get_drinks_query(limit, offset):
        return f"SELECT c_id, c_name, c_drink_type, c_sake_type, c_date_crafted, c_image_url FROM t_drink LIMIT {limit} OFFSET {offset}"

    @staticmethod
    def update_drinks_query(id, update):
        return f"UPDATE t_drink 
            SET c_name = {update.name}, 
                c_drink_type = {update.drink_type},
                c_sake_type = {update.sake_type}, 
                c_date_crafted = {update.date_crafted}, 
                c_date_enjoyed = {update.date_enjoyed}, 
                c_description = {update.desc} 
            WHERE c_id={id}
            "
    
    @staticmethod
    def update_drinks_image_query(id, imgUrl):
        return f"UPDATE t_drink
            SET c_image_url = {imgUrl} 
            WHERE c_id={id}"

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
