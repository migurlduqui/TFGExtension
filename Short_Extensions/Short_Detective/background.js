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

chrome.alarms.create({ periodInMinutes: 0.07 });

chrome.alarms.onAlarm.addListener(()=>{
    //chrome.system.cpu.getInfo((info)=>{logCPU(info)})
    //chrome.management.getAll((info)=>{logExApp(info)})
    //chrome.downloads.search({}).then(logExApp) 
    //chrome.proxy.settings.get({'incognito': false}, logExApp(config))
    //chrome.ChromeSetting.get() //I believe this is the basis for the rest, not for actual use
    
    loggingcontentSettings()
    //loggingprivacySettings();

    })