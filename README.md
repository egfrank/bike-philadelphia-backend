# bike-philly
A web app designed to practice building a backend in  Django and a frontend in vanilla JS

Takes inspiration from P'unkAve's [backend](https://github.com/punkave/backend-challenge) and [frontend](https://github.com/punkave/frontend-challenge) challenges.

I decided to implement the backend in Django (the original challenge specifies the backend to be implemented in Node.js and Express) since I have experience with Python and wanted to learn Django.

The frontend is purely implemented in vanilla JS, since the goal for me was to begin to learn Javascript. It addresses and expands on the specifications in the frontend challenge. It uses Leaflet's plugin to display the map and append markers, and Mapbox's API to do reverse geocoding (ie to go from a location "Philadelphia City Hall" to coordinates [-39, 50]) and to order the map elements by distance from the selected location.
