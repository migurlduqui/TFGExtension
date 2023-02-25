function captureGeolocation(){

    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( {lat: latitude, lon : longitude}),
        headers:{"Content-Type": "application/json"}
        }
)});


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