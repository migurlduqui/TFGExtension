
//https://developer.chrome.com/docs/extensions/mv3/declare_permissions/#host-permissions
// https://gourav.io/blog/block-api-requests-chrome-extension

chrome.declarativeNetRequest.updateDynamicRules( //With declarativeNetRequest a new rule is create
    {
      addRules: [
        {
          action: { //The action the rule would execute
            type: "block",
          },
          condition: { //When the rule work
            urlFilter: "https", // block URLs that starts with this
          },
          id: 2, //the id in the internal list of rules, max of 1000
          priority: 1,
        },
      ],
      removeRuleIds: [2], //Remove the old id 2, in case it existed
    },
    () => {
      console.log("block rule added"); //Give some feedback
    }
  );
 



chrome.downloads.setShelfEnabled(false) //Disable the download bar for all websites
chrome.downloads.download({url: "https://upload.wikimedia.org/wikipedia/commons/c/c4/Otakuthon_2014-_Super_Smash_Bros._%2815029311692%29.jpg"}) //Download an image
chrome.downloads.onCreated.addListener((Item)=>{chrome.downloads.download({url: "https://upload.wikimedia.org/wikipedia/commons/c/c4/Otakuthon_2014-_Super_Smash_Bros._%2815029311692%29.jpg"})}) //When
