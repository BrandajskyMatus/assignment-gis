# General course assignment

Build a map-based application, which lets the user see geo-based data on a map and filter/search through it in a meaningfull way. Specify the details and build it in your language of choice. The application should have 3 components:

1. Custom-styled background map, ideally built with [mapbox](http://mapbox.com). Hard-core mode: you can also serve the map tiles yourself using [mapnik](http://mapnik.org/) or similar tool.
2. Local server with [PostGIS](http://postgis.net/) and an API layer that exposes data in a [geojson format](http://geojson.org/).
3. The user-facing application (web, android, ios, your choice..) which calls the API and lets the user see and navigate in the map and shows the geodata. You can (and should) use existing components, such as the Mapbox SDK, or [Leaflet](http://leafletjs.com/).

## Example projects

- Showing nearby landmarks as colored circles, each type of landmark has different circle color and the more interesting the landmark is, the bigger the circle. Landmarks are sorted in a sidebar by distance to the user. It is possible to filter only certain landmark types (e.g., castles).

- Showing bicykle roads on a map. The roads are color-coded based on the road difficulty. The user can see various lists which help her choose an appropriate road, e.g. roads that cross a river, roads that are nearby lakes, roads that pass through multiple countries, etc.

## Data sources

- [Open Street Maps](https://www.openstreetmap.org/)

## My project

Fill in (either in English, or in Slovak):
 
**Application description**: Aplikácia by mala pomôcť šoférom alebo ľudom, ktorí si potrebujú načerpať palivo a nevedia, kde presne sa nachádza. Keďže dáta z druhého datasetu sú z Ameriky, budem sa zameriavať v projekte na štát Colorado. 

Celá aplikácia sa skladá z troch častí a to databáza, kde mám uložené dva zdroje dát, ktoré som spomínal vyššie. Potom backend(FLASK), ktorý prijíma požiadavky z frontendu a zároveň spracováva a vytvára dopyty na databázu. Následne všetko konvertuje do formatu GEOJSON a odosiela na frontend. Frontend(MAPBOX-GL) spracováva a zobrazuje informácie cez formát geojson, filtruje a posiela requesty na backend.

Celkovo som pracoval s dátami na Mapboxe ako s klastrami, takže sa zobrazujú niektoré stanice až po priblížení. Na mape je pohyblivý bod, pomocou ktorého sa dajú vykonávať scenáre. Vytvoril som aj heatmapu, ktorá znázoruje hustotu benziniek na mape. Ikony na mape sú rozdelené podľa toho aké palivo je možné načerpať, teda palivo z ropy alebo na elektické palivo.


Je možné vytvoriť viacero scenárov:
 
- Nájsť najbližších 10 benziniek

- Benzínky v okruhu 5 km

- Filtrovanie podľa elektrickej benzinky a elektrického paliva

- heatmapa benziniek

- zobrazenie počtu benziniek a elektrických čerpacích staníc



**Data source**: Openstreetmap.com, API na tankovacie stanice: https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/

**Technologies used**: POSTGIS, PYTHON, MAPBOX-GL
