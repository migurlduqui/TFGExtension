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