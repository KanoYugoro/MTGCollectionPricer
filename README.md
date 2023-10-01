# MTG Collection Pricer

The idea with this is to input the sealed product I have in collection in the `collection.json` file.  This will then scrape
MTGGoldfish for the total price of the sealed product and evaluate how I'm doing based on the cost basis specified in the
json file.  This way, I can see what my collection is worth.

## MTGGoldfish Scrape Explanation

Basically, the sets in the json file get parsed and the `endpointName` property gets inserted into a URL.  That URL is
`https://www.mtggoldfish.com/sets/{{endpointName}}/Sealed#paper`.  Then the tabledata on the page gets evaluated against
what is specified in the `collection.json` file, formatted, and output in a resultant query.  The requests are time gated
to prevent any possible rate-limiting or IP blocking that mtggoldfish might do.  It's also somewhat important to note that
MTGGoldfish uses the TCGPlayer mid pricing, which is an average/median value of what the sealed product is worth.