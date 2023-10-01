from base_api import (Base_Api)

if __name__ == "__main__":
    api = Base_Api("https://www.mtggoldfish.com/sets","Sealed#paper")
    response = api.make_get_request("Wilds+of+Eldraine")
    tables = Base_Api.find_tables(response.text)
    parsed_tables = Base_Api.parse_table(tables[0])
    print(parsed_tables)