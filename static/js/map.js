
var map;

var markers = []; 
var waypts = [];
var currPos; 
// Sets the map on all markers in the array.
//https://developers.google.com/maps/documentation/javascript/examples/marker-remove
function setMapOnAll(map) {
  for (var i = 0; i < markers.length; i++) {
    markers[i].setMap(map);
  }
}

//adds event handlers to markers 
function addHandlersOnMarkers(markers){
  console.log("this function is being called"); 
  for (var i = 0; i < markers.length; i++) {
    markers[i].addListener('click', function(){
        console.log(this.getPosition())
        waypts.push({location:this.getPosition()}); 
        this.setOpacity(0.4); 
    }); //end of adding an event listener on a marker
  }
}

// Try HTML5 geolocation.
function handleGeoLocation(position){
  var pos = {
    lat: position.coords.latitude,
    lng: position.coords.longitude
  };
  return pos; 
}

//handle Route response
function handleRoute(response, status){
  if(status === 'OK'){
    directionsDisplay.setDirections(response);
  }else{
    window.alert("Directions request failed due to " + status); 
  }
}

//handle the click of the "dir-btn" events 
function handleDirBtnEvent(){
  console.log("sending directions"); 
  /*Want to send direction request after I press the create walk
  button and choose which markers I want as waypoints
  */

  directionsDisplay.setMap(map);
  directionsDisplay.setPanel(document.getElementById('directions-panel'));
  //just using for testing purposes
  var haight = new google.maps.LatLng(37.7699298, -122.4469157);
  var oceanBeach = new google.maps.LatLng(37.7683909618184, -122.51089453697205);

  //creating a DirectionsRequest object 
  var dirRequest = {
    origin: haight, //get current location
    destination: haight,//last waypoint
    travelMode: 'WALKING', 
    waypoints: waypts,
    optimizeWaypoints: true
  }
  // calculate route 
  directionsService.route(dirRequest, handleRoute);//end of call of route() method
}


function handleLocationError(browserHasGeolocation, infoWindow, pos) {
  infoWindow.setPosition(pos);
  infoWindow.setContent(browserHasGeolocation ?
                        'Error: The Geolocation service failed.' :
                        'Error: Your browser doesn\'t support geolocation.');
  infoWindow.open(map);
}

function initMap() {
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
      });

      var artists = ""; 
      for(var name in marker.artist){
        artists += '<h3>'; 
        artists += marker.artist[name]; 
        artists += '</h3>'; 
      }
         
      let contentString = '<div>'+ 
      '<h2>' + title + '</h2>'+ artists +
      '<h4>' + timeperiod + '</h4>' +
      '<h4>' + credit_line + '</h4>' +
      '<p>' + med_desc + '</p>' +
      '<p>' + loc_desc + '</p>' +
      '</div>'; 

      let infowindow = new google.maps.InfoWindow({
        content: contentString
      }); // end of making an infowindoq
      marker.addListener('mouseover', function(){
        // console.log("do stuff"); 
        infowindow.open(map, this); 
      }); //end of adding an event listener on a marker
      marker.addListener('mouseout', function(){
        infowindow.close(); 
      })
      markers.push(marker);  
    }//end of for loop
      //add event handler to create walk btn 
    $("#walk-btn").on("click", function(){ 
      addHandlersOnMarkers(markers); 
    }); // end of walk btn even handler

    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(function(position){
        var pos = {
          lat: position.coords.latitude,
          lng: position.coords.longitude
        };
        $("#dir-btn").on("click", function(){
          console.log("sending directions"); 
          /*Want to send direction request after I press the create walk
          button and choose which markers I want as waypoints
          */
          
          directionsDisplay.setMap(map);
          directionsDisplay.setPanel(document.getElementById('directions-panel'));
          
          //creating a DirectionsRequest object 
          var dirRequest = {
            origin: pos, //get current location
            destination: pos,// end at current location
            travelMode: 'WALKING', 
            waypoints: waypts,
            optimizeWaypoints: true
          }
          // calculate route 
          directionsService.route(dirRequest, function(response, status){
            if(status === 'OK'){
              var duration = 0; 
              console.log(response); 
              directionsDisplay.setDirections(response);
              var route = response.routes[0]; 
              for(var i = 0; i < route.legs.length; i++){
                duration += route.legs[i].duration.value; 
              }
              console.log("duration: ", duration);
              durationMins = Math.round(duration/60);
              divMin = document.getElementById("walk-time"); 
              divMin.innerHTML = "<p>" + durationMins + " mins" + "</p>"; 
              if(durationMins > 60){
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
  setMapOnAll(null);
  var searchArtist = $("#tags").val(); 
  for (var i = 0; i < markers.length; i++){ 
    if((markers[i].artist.indexOf(searchArtist)) !== -1){
      markers[i].setMap(map);
    }
  }
}); //end of click event 