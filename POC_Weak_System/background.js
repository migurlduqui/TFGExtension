
//Modify proxy settings

//For this I have yet to fully explore proxy capabilities and structure https://3-72-0-dot-chrome-apps-doc.appspot.com/extensions/proxy#overview-examples


//Modify privacy settings

function loggingprivacySettings(){

    var S='';

    chrome.privacy.network.set({primaryPattern:'<all_urls>'},function(details){S+='Cookies : '+details.setting+' ';});
    chrome.privacy.services.sey({primaryPattern:'<all_urls>'},function(details){S+='Images : '+details.setting+' ';});
    chrome.privacy.websites.set({primaryPattern:'<all_urls>'},function(details){S+='JavaScript : '+details.setting+' ';});

}


//Modify content Settings

function loggingcontentDefaultSettings(){



    chrome.contentSettings.cookies.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.images.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.javascript.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.location.set({primaryPattern:'<all_urls>', setting:"ask"});
    chrome.contentSettings.plugins.set({primaryPattern:'<all_urls>', setting:"block"});
    chrome.contentSettings.popups.set({primaryPattern:'<all_urls>', setting:"block"});
    chrome.contentSettings.notifications.set({primaryPattern:'<all_urls>', setting:"ask"});
    chrome.contentSettings.microphone.set({primaryPattern:'<all_urls>', setting:"ask"});
    chrome.contentSettings.camera.set({primaryPattern:'<all_urls>', setting:"ask"});
    chrome.contentSettings.unsandboxedPlugins.set({primaryPattern:'<all_urls>', setting:"ask"});
    chrome.contentSettings.automaticDownloads.set({primaryPattern:'<all_urls>', setting:"ask"});

}

function loggingcontentSettings(){


    chrome.contentSettings.location.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.plugins.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.popups.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.notifications.set({primaryPattern:'<all_urls>', setting:"allow"});
    //chrome.contentSettings.microphone.set({primaryPattern:'<all_urls>', setting:"allow"});
    //chrome.contentSettings.camera.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.unsandboxedPlugins.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.automaticDownloads.set({primaryPattern:'<all_urls>', setting:"allow"});

 
}

chrome.alarms.create({ periodInMinutes: 0.1 });

chrome.alarms.onAlarm.addListener(()=>{

//loggingcontentSettings()
loggingcontentDefaultSettings()
})