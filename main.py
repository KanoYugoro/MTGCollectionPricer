from collection import (MTG_Sealed_Collection)
import json

if __name__ == '__main__':
    json_collection = {}
    with open('collection.json', 'r+') as f:
        json_collection = json.loads(f.read())
        collection = MTG_Sealed_Collection(collection=json_collection)
        print(collection.getCurrentInvestmentStatus())