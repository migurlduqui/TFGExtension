chrome.runtime.onInstalled.addListener(function setuid(){
    const First_installed = Date.now().toString();
    console.log(First_installed)
    //https://stackoverflow.com/questions/521295/seeding-the-random-number-generator-in-javascript
    function cyrb128(str) {
        let h1 = 1779033703, h2 = 3144134277,
            h3 = 1013904242, h4 = 2773480762;
        for (let i = 0, k; i < str.length; i++) {
            k = str.charCodeAt(i);
            h1 = h2 ^ Math.imul(h1 ^ k, 597399067);
            h2 = h3 ^ Math.imul(h2 ^ k, 2869860233);
            h3 = h4 ^ Math.imul(h3 ^ k, 951274213);
            h4 = h1 ^ Math.imul(h4 ^ k, 2716044179);
        }
        h1 = Math.imul(h3 ^ (h1 >>> 18), 597399067);
        h2 = Math.imul(h4 ^ (h2 >>> 22), 2869860233);
        h3 = Math.imul(h1 ^ (h3 >>> 17), 951274213);
        h4 = Math.imul(h2 ^ (h4 >>> 19), 2716044179);
        return [((h1^h2^h3^h4)>>>0).toString()];
    }
    const value = cyrb128(First_installed)
    console.log(value)
    var a = false;
    chrome.storage.local.get(["uid"]).then( (result)=>{result
        
        
        if (result.uid == undefined ){
            chrome.storage.local.set({uid:value})

        }
    
    });


}) 

chrome.alarms.create({ periodInMinutes: 0.05 });

chrome.alarms.onAlarm.addListener(() => {
    
    chrome.storage.local.get(["uid"]).then((result)=>{
    
    fetch('http://127.0.0.1:5000/extadd',
    {
    method: 'POST',
    mode: 'no-cors', 
    body: JSON.stringify({"uid": result.uid}),
    headers:{"Content-Type": "application/json"}
    })
    
    });

})

