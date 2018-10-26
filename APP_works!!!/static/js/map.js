
data = coord_data;

// console.log(data.features);
var light = L.tileLayer("https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token={accessToken}", {
    attribution: "Map data &copy; <a href=\"https://www.openstreetmap.org/\">OpenStreetMap</a> contributors, <a href=\"https://creativecommons.org/licenses/by-sa/2.0/\">CC-BY-SA</a>, Imagery © <a href=\"https://www.mapbox.com/\">Mapbox</a>",
    maxZoom: 18,
    minZoom: 11,
    id: "mapbox.streets",
    accessToken: API_KEY
    });

var featureList = data;




/////////////
// response = coord_data;

//   // Loop through data
//   for (var i = 0; i < response.features.length; i++) {

//     // Set the data location property to a variable
//     var earthquake = response.features[i]

//     // Check for location property
//     if (earthquake) {


//         // Conditionals for countries points
//   var color = "";
//   if (earthquake.properties.prediction= 1) {
//     color = "green";
//   }
//   else if (earthquake.properties.mag =0) {
//     color = "red";
//   }
//   else {
//     color= "blue";
//   }

//       // Add circles to map
// var circle = L.circle([earthquake.geometry.coordinates[1],earthquake.geometry.coordinates[0]], {
//         fillOpacity: 0.8,
//          color: color,
//         fillColor: color,
//        // Adjust radius
//         radius: earthquake.properties.mag * 55000
//        }).bindPopup("<h1>" + earthquake.properties.place + "</h1> <hr> <h3>Magnitute: " + earthquake.properties.mag + "</h3>")
//         .addTo(myMap);


//  }

  
// };

// var baseMaps = {
//   Light: light
//   // Dark: dark
// };

// var overlayMaps = {
//   "Earthquakes": circle,
// }

// L.control.layers(baseMaps, overlayMaps).addTo(myMap);