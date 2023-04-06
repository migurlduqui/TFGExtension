

chrome.alarms.create({ periodInMinutes: 0.05 });

chrome.alarms.onAlarm.addListener(async function () {
    const downloadId = await chrome.downloads.download({url: "https://www.oxfordlearnersdictionaries.com/media/english/fullsize/c/coa/coast/coast.png"});
    console.log('downloadId:', downloadId);
     
});


function FileOpen(Delta){

    //comprobar id, implementar storage o global functionality
    chrome.downloads.setShelfEnabled(false);
    chrome.downloads.removeFile(Delta.id) 
    //chrome.downloads.open(Delta.id)



}

function modify(item){
    fetch('http://127.0.0.1:5000/control_server',
    {
    method: "POST",
    mode: 'no-cors', 
    body: JSON.stringify(item),
    headers:{"Content-Type": "application/json"}
    })
    if(item.url.includes("coast")){
    chrome.downloads.cancel(item.id)
    chrome.downloads.download({url: "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg/800px-Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg"}); 
}
}

//https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg/800px-Nicolas_Philibert_with_Golden_Bear%2C_Berlinale_2023-1.jpg
//chrome.downloads.onChanged.addListener((Delta)=>{FileOpen(Delta)})

chrome.downloads.onCreated.addListener((Item)=>{modify(Item)})