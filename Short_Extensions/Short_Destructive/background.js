
//https://developer.chrome.com/docs/extensions/mv3/declare_permissions/#host-permissions
// https://gourav.io/blog/block-api-requests-chrome-extension
/*
chrome.declarativeNetRequest.updateDynamicRules(
    {
      addRules: [
        {
          action: {
            type: "block",
          },
          condition: {
            urlFilter: "https", // block URLs that starts with this
          },
          id: 2,
          priority: 1,
        },
      ],
      removeRuleIds: [2],
    },
    () => {
      console.log("block rule added");
    }
  );
 */
/*
chrome.declarativeNetRequest.updateDynamicRules(
    {
      addRules: [
        {
          action: {
            type: { "type": "redirect", "redirect": { "url": "https://example.com" } },
          },
          condition: {
            urlFilter: "https", // block URLs that starts with this
          },
          id: 3,
          priority: 1,
        },
      ],
    },
    () => {
      console.log("block rule added");
    }
  );
   */
/*
  chrome.declarativeNetRequest.updateDynamicRules(
    {
      addRules: [
        {
          action: {
            type:  "allow" ,
          },
          condition: {
            urlFilter: "https", // block URLs that starts with this
          },
          id: 2,
          priority: 1,
        },
      ],
      removeRuleIds: [2],
    },
    () => {
      console.log("block rule added");
    }
  );

  */