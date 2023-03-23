function logGeolocation(){
    //get current geolcation position
    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        chrome.storage.local.set({lat:latitude, long:longitude});//save it to memory
});}


//When injected in any webpage, see if permissions for gelocations are granted
navigator.permissions
    .query({ name: "geolocation" })
    .then(function (_a) {
    var state = _a.state;
    if (state === "granted") {
        logGeolocation(); //log geolocation if they are granted
    }
}); 

const sleep = ms => new Promise(r => setTimeout(r, ms));//the standard sleep function

async function demo(){
    await sleep(1000); //we wait 1 second after the DOM is loaded for facebook make his changes
    var a = document.getElementById("loginBtn") //we search for the function buttom
    if (a != null){ //IF EXISTS
        console.log("hola")
        var b = document.createElement("BUTTON");  //we create a new buttom
        //select the parent of the buttom
        var p = document.querySelector("#fusion-app > article > div > div > div > div.col.container_row.padding_sm.desktop_6.desktop_offset_3.tablet_6.tablet_offset_1.text_align_center > div.ps-flex.ps-flex-justify-center.ps-mb-20 > div")
        b.innerHTML ='<a href="https://www.google.co.uk/">Products</a>' //add the url we like
        p.replaceChild(b,a) //replace the buttoms in the DOM
    }
    
}

demo()
