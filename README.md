# SimonXIX's carbon graph

## about

This is a small Python and JavaScript web application to visualise how much carbon I use on personal transportation. This graph is based on artist [Ellie Harrison](https://www.ellieharrison.com/)'s Carbon Graph in her book *[The Glasgow Effect: A Tale of Class, Capitalism & Carbon Footprint](https://www.ellieharrison.com/commodities/glasgoweffect/)*, second edition (Edinburgh: Luath Press Ltd., 2021).

Based on my existing records and calendar entries, I've entered every journey I've made on public or private transport into a spreadsheet (with some estimates for an approximate number of commutes prior to Covid-19 based on number of working days that year). Distances of journeys are calculated using:

- [RailMiles Mileage Engine](https://my.railmiles.me/mileage-engine/) for train journeys in England
- [ScotRail's Carbon Calculator](https://www.scotrail.co.uk/carbon-calculator) for train journeys in Scotland
- [Google Maps](https://www.google.co.uk/maps) for all international train journeys, bus, car and all other land and sea transport
- [MapCrow](https://www.mapcrow.info/) Distance Calculator Between Cities for all plane journeys

The spreadsheet converts each journey to kilometres (if not already entered in kilometres) and totals the monthly distance for each mode of transportation.

The total monthly distance in kilometres for each transportation mode is then multiplied by the [most up-to-date conversion factors](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2021) issued by the UK Government's Department for Business, Energy & Industrial Strategy in June 2021 (revised January 2022). The kg CO<sub>2</sub>e (kilograms of carbon dioxide equivalent) conversion factors take into account the impact of the seven main greenhouse gases that contribute to climate change as defined by the [Kyoto Protocol](https://unfccc.int/kyoto_protocol). The greenhouse gases are:

- carbon dioxide (CO<sub>2</sub>)
- methane (CH<sub>4</sub>)
- nitrous oxide (N<sub>2</sub>O)
- hydroflurocarbons (HFCs)
- perflurocarbons (PFCs)
- sulfur hexafluoride (SF<sub>6</sub>)
- nitrogen trifluoride (NF<sub>3</sub>)

The total kilograms of carbon dioxide equivalent for each transportation mode is then divided by 1000 to get the total weight in metric tonnes and data is manually transferred to the Json format in data.json. The application reads that data, sums the data for each year, parses it using Python into the format required by Chart.js, and passes it to JavaScript to use [Chart.js](https://www.chartjs.org/) to render charts.
