
var map;

var markers = []; 
var waypts = [];
var currPos; 

// Sets the map on all markers in the array.
function setMapOnAll(map, markerArray){
  markerArray.forEach(function(marker){
    marker.setMap(map); 
  }); 
}

//adds event handlers to markers 
function addHandlersOnMarkers(markerArray, wayptArray){
  console.log("addHandlersOnMarkers");  
  markerArray.forEach(function(marker){
      marker.addListener("click", function(){
      //pushes waypoint literal to waypoint array
      wayptArray.push({location:this.getPosition()});
      //changes opacity of marker 
      this.setOpacity(0.3); 
      //add marker info side bar
      let l_item = $("<li></li>");
      l_item.text(this.title);
      $("#marker-lst").append(l_item);
      $("#dir-btn").prop("disabled", false); 

    });//end of adding an event listener on a marker
  }); 
}

function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

function getRandomMarkers(numOfChoices, markerArray, newMarkerArray){
  //Pushes random markers into a new array 
  var index; 
  for(var i = 0; i <= numOfChoices; i++){
    index = Math.floor(Math.random() * markerArray.length);
    newMarkerArray.push(markerArray[index]); 
  }
}

function storeInboundMarkers(bounds, markers, inboundMarkers){
  //stores markers that inbounds in a new array
  for(var i = 0; i < markers.length; i++){
    if(bounds.contains(markers[i].getPosition())){
      inboundMarkers.push(markers[i]); 
    }else{
      markers[i].setMap(null); 
    }
  }
}

function createHtmlArtists(artistList){
  var htmlArtists = ""; 
  for(var name in artistList){
    htmlArtists += '<h3>'; 
    htmlArtists += artistList[name]; 
    htmlArtists += '</h3>'; 
  }
  return htmlArtists; 
}

function calcRouteDurationMins(route){
  var duration = 0;
  for(var i = 0; i < route.legs.length; i++){
    duration += route.legs[i].duration.value; 
  }
  var durationMins = Math.round(duration/60);
  return durationMins; 
}


function initMap() {
  console.log("initMap"); 
  //instantiate a DirectionsService Object 
  var directionsService = new google.maps.DirectionsService;
  //instantiate a DirectionsRenderer object
  var directionsDisplay = new google.maps.DirectionsRenderer;
  //instantiate a Map object 
  map = new google.maps.Map(document.getElementById('art-map'), {
    center: {lat: 37.7748, lng: -122.435},
    zoom: 12,
    // gestureHandling: 'none',
    // zoomControl: false
  });

  // retrieves artpiece info with AJAX
  $.get("/pieces.json", function(data){
    pieces = data["results"]
    //iterate through results 
    for(var i in pieces){
      piece = pieces[i];
      let title = piece["title"]; 
      let timeperiod = piece["timeperiod"]; 
      let med_desc = piece["med_desc"]; 
      let credit_line = piece["creditline"]; 
      let loc_desc = piece["loc_desc"];
      let artist = piece["artist"]; 

      marker = new google.maps.Marker({
        position: new google.maps.LatLng(piece["coords"][1], piece["coords"][0]),
        map: map,
        title: title,
        timeperiod: timeperiod,
        med_desc: med_desc, 
        credit_line: credit_line, 
        loc_desc: loc_desc, 
        artist: artist, 
        opacity: 1.0
      });//instantiate a Marker Object 

      var artists = createHtmlArtists(marker.artist); 
      let contentString = '<div>'+ 
      '<h2>' + title + '</h2>'+ artists +
      '<h4>' + timeperiod + '</h4>' +
      '<h4>' + credit_line + '</h4>' +
      '<p>' + med_desc + '</p>' +
      '<p>' + loc_desc + '</p>' +
      '</div>'; 

      //instantiate an InfoWindow Object
      let infowindow = new google.maps.InfoWindow({
        content: contentString
      }); 

      //add event listeners to each marker
      marker.addListener('mouseover', function(){
        infowindow.open(map, this); 
      }); 
      marker.addListener('mouseout', function(){
        infowindow.close(); 
      })

      //push marker into markers array 
      markers.push(marker);  
    }//end of for loop

    //add event handler to create walk btn 
    $("#walk-btn").on("click", function(){
      addHandlersOnMarkers(markers, waypts);
      $("#crt-walk").toggle("slow");   
    }); // end of walk btn even handler

    $("#rand-btn").click(function (evt) {
      $("#miles-btn").click(function(event){
        event.preventDefault();
        //getting directions for randomewalk 
         if (navigator.geolocation) {
          navigator.geolocation.getCurrentPosition(function(position){
            var pos = {
              lat: position.coords.latitude,
              lng: position.coords.longitude
            };

            var walkRadius = $("#miles").val();
            walkRadius = walkRadius/2.0; 
            console.log(walkRadius); 
            console.log("/////////////////")
            console.log(walkRadius);
            var walkRadiusMeters = walkRadius * 1609.34;
            var cityCircle = new google.maps.Circle({
                strokeColor: '#FF0000',
                strokeOpacity: 0.8,
                strokeWeight: 2,
                fillColor: '#FF0000',
                fillOpacity: 0.35,
                map: map,
                center: pos,
                radius: walkRadiusMeters
            });

            var bounds = cityCircle.getBounds();
            var grabBagMarkers = [];
            //calling storeInboundMarkers
            storeInboundMarkers(bounds, markers, grabBagMarkers); 

            /* Choose a few random markers from grabBagMarker */ 
            var selectedMarkers = [];
            getRandomMarkers(3, grabBagMarkers, selectedMarkers); 
            
            var randWayPoints = []; 

            for(var i = 0; i < selectedMarkers.length; i++){
              var wayLocation = selectedMarkers[i].getPosition(); 
              randWayPoints.push({location: wayLocation}); 
            }

            directionsDisplay.setMap(map);
            directionsDisplay.setPanel(document.getElementById('directions-panel'));
            
            //creating a DirectionsRequest object 
            var randDirRequest = {
              origin: pos, //get current location
              destination: pos,// end at current location
              travelMode: 'WALKING', 
              waypoints: randWayPoints,
              optimizeWaypoints: true
            }
              // calculate route 
              directionsService.route(randDirRequest, function(response, status){
                if(status === 'OK'){ 
                  directionsDisplay.setDirections(response);
                  var route = response.routes[0]; 
                  var dur = calcRouteDurationMins(route); 
                  divMin = document.getElementById("walk-time"); 
                  divMin.innerHTML = "<p>" + dur + " mins" + "</p>"; 
                  if(dur > 60){
                    window.alert("Are you sure you want to walk " + durationMins +" mins?"); 
                  } 
                }else{
                  window.alert("Directions request failed due to " + status); 
                }
              });//end of call of route() method
          }, function() {
              handleLocationError(true, infoWindow, map.getCenter());
          });
        } else {
          // Browser doesn't support Geolocation
          handleLocationError(false, infoWindow, map.getCenter());
        } 


      }) 
    });
    // end of random walk button event handler
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position){
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        //start of handling click event for directons button 
        $("#dir-btn").on("click", function(){
          directionsDisplay.setMap(map);
          directionsDisplay.setPanel(document.getElementById('directions-panel'));
          
          //creating a DirectionsRequest object 
          var dirRequest = {
            origin: pos, //get current location
            //destination could be last waypoint
            destination: pos,// end at current location
            travelMode: 'WALKING', 
            waypoints: waypts,
            optimizeWaypoints: true
          }
          // calculate route 
          directionsService.route(dirRequest, function(response, status){
            if(status === 'OK'){ 
              $("#crt-walk").toggle("slow"); 
              directionsDisplay.setDirections(response);
              var route = response.routes[0]; 
              var dur = calcRouteDurationMins(route); 
              divMin = document.getElementById("walk-time"); 
              divMin.innerHTML = "<p>" + dur + " mins" + "</p>"; 
              if(dur > 60){
                window.alert("Are you sure you want to walk " + durationMins +" mins?"); 
              } 
            }else{
              window.alert("Directions request failed due to " + status); 
            }
          });//end of call of route() method
        });//end of directions btn event handler
      }, function() {
          handleLocationError(true, infoWindow, map.getCenter());
      });
    } else {
      // Browser doesn't support Geolocation
      handleLocationError(false, infoWindow, map.getCenter());
    } 
  });//end of $.get
} //end of initMap

// https://jqueryui.com/autocomplete/
//fill out the autocomplete section for the widget 
$( function() {
  var artists_names = []
  $.get("/artistnames", function(names){
    artists_names = names.slice()
    $( "#tags" ).autocomplete({
      source: artists_names
    });
  }); 
});

$("#submit-name").on("click", function(evt){
  evt.preventDefault();
  var searchArtist = $("#tags").val();
  if(searchArtist){
    setMapOnAll(null, markers);
    for (var i = 0; i < markers.length; i++){ 
      if((markers[i].artist.indexOf(searchArtist)) !== -1){
        markers[i].setMap(map);
      }
    }
  }else{
    setMapOnAll(map, markers); 
  }
}); //end of click event 