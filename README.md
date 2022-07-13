# SimonXIX's carbon graph

## about

This is a small Python web application to visualise how much carbon I used on personal transportation. This graph is based on artist [Ellie Harrison](https://www.ellieharrison.com/)'s Carbon Graph in her book *[The Glasgow Effect: A Tale of Class, Capitalism & Carbon Footprint](https://www.ellieharrison.com/commodities/glasgoweffect/)*, second edition (Edinburgh: Luath Press Ltd., 2021).

Distances of journeys are calculated using:
- [RailMiles Mileage Engine](https://my.railmiles.me/mileage-engine/) for all UK train journeys
- [Google Maps](https://www.google.co.uk/maps) for all international train journeys, bus, car and all other land and sea transport
- [MapCrow](https://www.mapcrow.info/) Distance Calculator Between Cities for all plane journeys

The total monthly distance for each transportation mode is then multiplied by the [most up-to-date conversion factors](https://www.gov.uk/government/publications/greenhouse-gas-reporting-conversion-factors-2021) issued by the UK Government's Department for Business, Energy & Industrial Strategy in June 2021 (revised January 2022). The kg CO<sub>2</sub>e (kilograms of carbon dioxide equivalent) conversion factors take into account the impact of the seven main greenhouse gases that contribute to climate change as defined by the Kyoto Protocol. The greenhouse gases are:

- carbon dioxide (CO<sub>2</sub>)
- methane (CH<sub>4</sub>)
- nitrous oxide (N<sub>2</sub>O)
- hydroflurocarbons (HFCs)
- perflurocarbons (PFCs)
- sulfur hexafluoride (SF<sub>6</sub>)
- nitrogen trifluoride (NF<sub>3</sub>)
