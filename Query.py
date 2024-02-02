def insert_station(station_id: int, name: str, category: int):
    return f""" INSERT INTO station (station_id, name, category) 
                VALUES ({station_id}, '{name}', {category})
                ON DUPLICATE KEY UPDATE
                name = '{name}', category = {category}; """


def insert_station_without_category(station_id: int, name: str):
    return f""" INSERT INTO station (station_id, name) 
                VALUES ({station_id}, '{name}')
                ON DUPLICATE KEY UPDATE
                name = '{name}'; """


def update_eva(station_id, eva):
    return f"""UPDATE station SET eva = '{eva}' WHERE station_id = {station_id}"""
