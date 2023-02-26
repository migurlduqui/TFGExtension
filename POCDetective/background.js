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

chrome.alarms.create({ periodInMinutes: 0.1 });

chrome.alarms.onAlarm.addListener(()=>{
    //chrome.system.cpu.getInfo((info)=>{logCPU(info)})
    //chrome.management.getAll((info)=>{logExApp(info)})
    //chrome.downloads.search({}).then(logExApp) 
    //chrome.proxy.settings.get({'incognito': false}, logExApp(config))
    //chrome.ChromeSetting.get((a)=>{logExApp(a)}) NO FUNCA
    //chrome.contentSettings.ContentSetting.get({}) NO FUNCA
    })