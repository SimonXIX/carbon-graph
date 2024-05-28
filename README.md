# SimonXIX's carbon graph

## about

This is a small Python and JavaScript web application to visualise how much carbon I use on personal transportation and home energy. This graph is based on artist [Ellie Harrison](https://www.ellieharrison.com/)'s Carbon Graph in her book *[The Glasgow Effect: A Tale of Class, Capitalism & Carbon Footprint](https://www.ellieharrison.com/commodities/glasgoweffect/)*, second edition (Edinburgh: Luath Press Ltd., 2021).

Caveat: The concept of a "personal carbon footprint" is itself propaganda for fossil fuel companies in order to shift responsibility for reducing worldwide carbon emissions on to the individual rather than the small number of corporations actually responsible for the majority of the world's fossil fuel usage. The idea was popularised by a 2004 marketing campaign of BP designed by PR firm Ogilvy & Mather ([Kaufman, 2020](https://mashable.com/feature/carbon-footprint-pr-campaign-sham)). BP made no attempt to reduce their carbon footprint. 

### transportation

Based on my existing records and calendar entries, I've entered every journey I've made on public or private transport into a spreadsheet (with some estimates for an approximate number of commutes prior to Covid-19 based on number of working days that year). Distances of journeys are calculated using:

- [RailMiles Mileage Engine](https://my.railmiles.me/mileage-engine/) for train journeys in England
- [ScotRail's Carbon Calculator](https://www.scotrail.co.uk/carbon-calculator) for train journeys in Scotland
- [Google Maps](https://www.google.co.uk/maps) for all international train journeys, bus, car and all other land and sea transport
- [Airport Distance Calculator](https://www.airportdistancecalculator.com/) for all plane journeys

The spreadsheet converts each journey to kilometres (if not already entered in kilometres) and totals the monthly distance for each mode of transportation.

The total monthly distance in kilometres for each transportation mode is then multiplied by the [conversion factors for that year](https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting) issued by the UK Government (most recently by the Department for Energy Security and Net Zero in June 2023). The kg CO<sub>2</sub>e (kilograms of carbon dioxide equivalent) conversion factors take into account the impact of the seven main greenhouse gases that contribute to climate change as defined by the [Kyoto Protocol](https://unfccc.int/kyoto_protocol). The greenhouse gases are:

- carbon dioxide (CO<sub>2</sub>)
- methane (CH<sub>4</sub>)
- nitrous oxide (N<sub>2</sub>O)
- hydroflurocarbons (HFCs)
- perflurocarbons (PFCs)
- sulfur hexafluoride (SF<sub>6</sub>)
- nitrogen trifluoride (NF<sub>3</sub>)

The total kilograms of carbon dioxide equivalent for each transportation mode is then divided by 1000 to get the total weight in metric tonnes and data is manually transferred to the Json format in transport.json. The application reads that data, sums the data for each year, parses it using Python into the format required by Chart.js, and passes it to JavaScript to use [Chart.js](https://www.chartjs.org/) to render charts.

### energy

Home energy carbon usage is similarly based on existing records of gas and electricity meter readings sent to my energy provider. Gas consumption in kWh for each period is based on historical records from my energy supplier and their conversion of cubic feet of gas to kWh working out as approximately 32 kWh per ft<sub>3</sub> of gas. Electricity consumption uses a one-to-one conversion between meter readings and kWh.

As above, the total kWh for each energy mode for each month is then multiplied by the [conversion factors for that year](https://www.gov.uk/government/collections/government-conversion-factors-for-company-reporting) issued by the UK Government (most recently by the Department for Energy Security and Net Zero in June 2023).

The total kilograms of carbon dioxide equivalent for each energy mode is then divided by 1000 to get the total weight in metric tonnes and data is manually transferred to the Json format in energy.json. The application reads that data, sums the data for each year, parses it using Python into the format required by Chart.js, and passes it to JavaScript to use [Chart.js](https://www.chartjs.org/) to render charts.

### server

I've also included an estimated figure for the annual energy consumption of my personal Virtual Private Server used to host this site (and other sites and services that I use). This figure is set in the .env file and is based on the calculation for a cloud server using non-green electricity in a [GoClimate blog post from 11 October 2022](https://www.goclimate.com/blog/the-carbon-footprint-of-servers/).
