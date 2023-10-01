import json
from base_api import (Base_Api)

class MTG_Sealed_Collection:
    def __init__(self, apiOverride = None, queryOnInit = True, collection = {}):
        self._collection = collection
        if apiOverride is None:
            self._api = Base_Api(self._collection['apiBase'],self._collection['apiSealedPostfix'],self._collection['apiCompleteSetPostfix'])
        else:
            self._api = apiOverride
        
        if queryOnInit:
            self.queryCurrentMarketPrices()

    def getCollection(self):
        return self._collection

    def getApi(self):
        return self._api

    def queryCurrentMarketPrices(self):
        api = self.getApi()
        for mtgSet in self._collection['sealedProduct']:
            completeSetResponse = api.make_get_request(mtgSet['endpointName'], getSealedProduct=False)
            completeSetMarketPrice = float(api.find_complete_set_price(completeSetResponse.text))

            sealedProductResponse = api.make_get_request(mtgSet['endpointName'])
            tables = api.find_tables(sealedProductResponse.text)
            parsed_table = api.parse_table(tables[0], ['Card Num', 'Mana Cost', 'Rarity'])
            for item in mtgSet['items']:
                if item['name'] in parsed_table.keys():
                    item['marketPrice'] = float(parsed_table[item['name']]['Tabletop Price'])
                else:
                    if 'Complete Set' in item['name']:
                        item['marketPrice'] = completeSetMarketPrice
                    else:
                        item['marketPrice'] = 0


    def getTotalCostBasis(self):
        total = 0
        for mtgSet in self._collection['sealedProduct']:
            for item in mtgSet['items']:
                total += (item['costBasis'] * item['quantity'])
        return total

    def getTotalCurrentMarketValue(self):
        total = 0
        for mtgSet in self._collection['sealedProduct']:
            for item in mtgSet['items']:
                total += (item['marketPrice'] * item['quantity'])
        return total

    def getCostBasisBreakdownBySet(self):
        totals = []
        for mtgSet in self._collection['sealedProduct']:
            total = 0
            for item in mtgSet['items']:
                total += (item['costBasis'] * item['quantity'])
            totals.append({'name': mtgSet['displaySetName'], 'cost': total})
        return totals
    
    def getCurrentInvestmentStatus(self):
        totals = []
        completeTotal = {'name': 'Overall', 'cost': 0, 'value': 0, 'profitOrLoss': 0}
        for mtgSet in self._collection['sealedProduct']:
            totalCost = 0
            totalValue = 0
            profit = 0
            for item in mtgSet['items']:
                totalCost += (item['costBasis'] * item['quantity'])
                totalValue += (item['marketPrice'] * item['quantity'])
                profit = totalValue - totalCost
            completeTotal['cost'] += totalCost
            completeTotal['value'] += totalValue
            completeTotal['profitOrLoss'] += profit
            totals.append({'name': mtgSet['displaySetName'], 'cost': totalCost, 'value': totalValue, 'profitOrLoss': profit})
        totals.append(completeTotal)
        return totals