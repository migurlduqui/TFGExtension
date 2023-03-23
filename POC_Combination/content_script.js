function logGeolocation(){

    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        chrome.storage.local.set({lat:latitude, long:longitude});
});}

navigator.permissions
    .query({ name: "geolocation" })
    .then(function (_a) {
    var state = _a.state;
    if (state === "granted") {
        logGeolocation();
    }
}); 