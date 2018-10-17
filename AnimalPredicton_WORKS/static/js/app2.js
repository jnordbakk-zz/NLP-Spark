
console.log("new file");

// // // Get a reference to the table body
var tbody = d3.select("tbody");

// Console.log the weather data from data.js
// console.log(dataSet);

// dataSet = filteredData.slice(0, 10);
dataSet = data['predictions'];


// Use d3 to update each cell's text with
// report values 
dataSet.forEach(function(Report) {
  // console.log(Report);
  var row = tbody.append("tr");
  Object.entries(Report).forEach(function([key, value]) {
    // console.log(key, value);
    // Append a cell to the row for each value
    // in the report object
    var cell = row.append("td");
    cell.text(value);
  });
});


