import mysql.connector

db = mysql.connector.connect(
    host='localhost',
    user='logan',
    password='password',
    database='real_estate'
)


def execute_query(query: str) -> list[dict]:
    try:
        cursor = db.cursor(dictionary=True)
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.close()
        return rows
    except:
        return []


def get_property_from_type(property_type: str) -> list[tuple]:
    query = f"SELECT * FROM app_project WHERE type LIKE '%{property_type}%';"
    rows = execute_query(query)
    return rows


def get_distinct_property_types() -> list[dict]:
    query = f"SELECT DISTINCT type FROM app_project;"
    rows = execute_query(query)
    distinct_property_types = []
    for row in rows:
        data = row['type'].split(',')
        for d in data:
            d = d.strip()
            if d not in distinct_property_types:
                distinct_property_types.append(d)
    return distinct_property_types


def get_distinct_property_types() -> list[dict]:
    query = f"SELECT DISTINCT type FROM app_project;"
    rows = execute_query(query)
    distinct_property_types = []
    for row in rows:
        data = row['type'].split(',')
        for d in data:
            d = d.strip()
            if d not in distinct_property_types:
                if len(d) > 20:
                    d = d[:17]
                    d += '...'
                distinct_property_types.append(d)
    return distinct_property_types


def get_media_from_project_id(project_id: int) -> list[dict]:
    query = f"SELECT * FROM real_estate.app_projectdocument WHERE project_id={project_id};"
    rows = execute_query(query)
    return rows


def get_property_from_location(location: str) -> list[tuple]:
    query = f"SELECT * FROM real_estate.app_project WHERE area  LIKE '%{location}%' \
OR nearby_area LIKE '%{location}%' OR locality LIKE '%{location}%';"
    rows = execute_query(query)
    return rows


def get_distinct_property_locations() -> list[dict]:
    query = f"SELECT DISTINCT area FROM app_project;"
    rows = execute_query(query)
    distinct_property_locations = []
    for row in rows:
        d = row['area'].split(',')
        d = d[0].strip()
        if d not in distinct_property_locations:
            if len(d) > 20:
                    d = d[:17]
                    d += '...'
            distinct_property_locations.append(d)
    return distinct_property_locations
