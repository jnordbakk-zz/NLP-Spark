// map.off();
// map.remove();
// Function to determine marker size based on length of tweet
function markerSize(length) {
  return length;
}

function getColor(value) {
  if (value = 1) {
      return "limegreen";
  } else {
      (value = 0)
      return "red";
  }
}

// Query url
// var url = "http://localhost:5000/send";
var url ="http://127.0.0.1:5000/send";

// Grab the data with d3
d3.json(url, function(response) {
      var predictionMarkers = [];
  // console.log(response);
  // Loop through locations and create coordinates
      for (var i = 0; i < response.length; i++) {

        // console.log(response.coordinates[i]);
        var location = response[i].coordinates;
        
        // Check for location property
        if (location) {
          var newLocation = location.split(",").map(parseFloat)
          

          predictionMarkers.push(
            L.circle(newLocation, {
                stroke: false,
                fillOpacity: 0.75,
                fillColor: getColor(response[i].prediction),
                color: "purple",
                radius: markerSize(response[i].length) *  2000
            }))//.bindPopup("<h1>" + response.Tweet + "</h1>")
            //.addTo(myMap);
        // ); -- old
          

 
          }
         }//marker

               // Define variables for our base layers
               var streetmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
                attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
                maxZoom: 18,
                id: "mapbox.streets",
                accessToken: API_KEY
            });
      
            var darkmap = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
                attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
                maxZoom: 18,
                id: "mapbox.dark",
                accessToken: API_KEY
            });
      
            // Create a separate layer group for scores 
            var predictions = L.layerGroup(predictionMarkers);
      
            // Create a baseMaps object
            var baseMaps = {
                "Street Map": streetmap,
                "Dark Map": darkmap
            };
      
            // Create an overlay object
            var overlayMaps = {
                "Score": predictions
            };
      
            // Define a map object
            var myMap = L.map("map", {
                // center: [37.09, -95.71],
                center:[90,-90],
                zoom: 5,
                layers: [streetmap, predictions]
            });
      
            // Pass our map layers into our layer control
            // Add the layer control to the map
            L.control.layers(baseMaps, overlayMaps, {
                collapsed: false
            }).addTo(myMap);

         
      })
