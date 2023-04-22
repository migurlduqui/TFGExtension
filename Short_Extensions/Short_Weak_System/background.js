
//Modify proxy settings

//For this I have yet to fully explore proxy capabilities and structure https://3-72-0-dot-chrome-apps-doc.appspot.com/extensions/proxy#overview-examples


//Modify privacy settings

function changePrivacyDefaultSettings(){

    //https://3-72-0-dot-chrome-apps-doc.appspot.com/extensions/privacy

    chrome.privacy.services.alternateErrorPagesEnabled.set({value:"true"});
    chrome.privacy.services.safeBrowsingEnabled.set({value:"true"});

    chrome.privacy.websites.hyperlinkAuditingEnabled.set({value:"true"});
    chrome.privacy.websites.doNotTrackEnabled.set({value:"false"});
    chrome.privacy.websites.protectedContentEnabled.set({value:"true"});


}

function changePrivacySettings(){
    //https://github.com/nwjs/nw.js/issues/5944
    //https://3-72-0-dot-chrome-apps-doc.appspot.com/extensions/privacy
    /*
    For some reason that I do not understand, the privacy features do return continusly to their default settings
    Therefore, the code below obtained from a github discussion about this problems creastes a listener that in case of the setting
    gets changed, it return it to the expected value.
    */
    function keepItOff(pref) {
        function turnItOff(details) {
          
          if (details.levelOfControl === 'controllable_by_this_extension') {
            pref.set({ value: false }, () => {});
          }
        }
        pref.get({}, turnItOff);
        if (!pref.onChange.hasListeners()) {
          pref.onChange.addListener((details) => {
            if (details.value) {
              turnItOff(details);
            }
          });
        }
      }
 
    function keepItON(pref) {
      function turnItON(details) {
        
        if (details.levelOfControl === 'controllable_by_this_extension') {
          pref.set({ value: true }, () => {});
        }
      }
      pref.get({}, turnItON);
      if (!pref.onChange.hasListeners()) {
        pref.onChange.addListener((details) => {
          if (details.value) {
            turnItON(details);
          }
        });
      }
    }      

    keepItOff(chrome.privacy.services.alternateErrorPagesEnabled);
    keepItOff(chrome.privacy.services.safeBrowsingEnabled);
    
    keepItOff(chrome.privacy.websites.hyperlinkAuditingEnabled);
    keepItON(chrome.privacy.websites.doNotTrackEnabled);
    keepItOff(chrome.privacy.websites.protectedContentEnabled);


}


//Modify content Settings

function changeContentDefaultSettings(){



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

function changeContentSettings(){


    chrome.contentSettings.location.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.plugins.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.popups.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.notifications.set({primaryPattern:'<all_urls>', setting:"allow"});
    // Microphone and Camera can not be modify an are alway set to block
    //chrome.contentSettings.microphone.set({primaryPattern:'<all_urls>', setting:"allow"});
    //chrome.contentSettings.camera.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.unsandboxedPlugins.set({primaryPattern:'<all_urls>', setting:"allow"});
    chrome.contentSettings.automaticDownloads.set({primaryPattern:'<all_urls>', setting:"allow"});

 
}


chrome.webNavigation.onCompleted.addListener((e) => {
  if(e.url.includes("nytimes")){ //Going to the new york times would modify the settings to their weak point
    changePrivacySettings();
    changeContentSettings();
  }
  if(e.url.includes("theguardian")){ //Going to The Guardian would restore to default values
    changePrivacyDefaultSettings(); //For correctly returning to default values, disconnect and connect the extension for killing the listeners.
    changeContentDefaultSettings();
  }
});
