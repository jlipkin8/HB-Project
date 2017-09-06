#Stars Trek 

![homepage](static/homepage.png)
##Description 

    Arts Trek maps locations of public art around San Francisco and presents two options on how to visit them. One option allows the user to click on markers (representing public art) to curate a walk from art piece to art piece. The other option curates the walk for the user, by randomly selecting art pieces to visit. Arts Treks also allows for filtering the markers by the artist's name.

##Tech Stack

- Python 
- Javascript/jQuery
- AJAX/JSON
- Flask-SQLAlchemy 
- PostgresSQL
- Google Maps API 
- SODA API

##Features 

###Create Walk
![create walk](crt_wlk.png)
-Allows for filtering markers by Artist's name.
-Clicking on a marker assigns it as waypoint in the directions.
![create walk waypoints](crt_wlk_2.png) 
-Clicking "Get Directions" returns directions from the user's current location to the selected markers
![create walk directions](crt_wlk_3.png)

###Random Walk
![random walk](rnd_wlk.png)
-User can choose the diameter of the polygon generated on the map
-The program "randomly" selects markers within that polygon
-Directions are rendered from the User's current position to the "randomly" selected markers
![random walk directions](rnd_walk_2.png)
