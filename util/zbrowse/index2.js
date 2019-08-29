/*Requirements to spawn and communicate with headless*/
var Chrome = require('chrome-remote-interface');
var spawn = require('child_process').spawn;
var pup   = require('puppeteer');

/*Utility functions*/
var tree = require('./util/tree.js')
var queue = require('./util/queue.js')

/*Other requirements*/
var fs = require('fs')
var url = require('url')

if (process.argv.length != 4) {
    console.error('Correct usage: node index.js <url> <port>');
    process.exit(-1);     
}

var headlessPath = "/Applications/Chromium.app/Contents/MacOS/Chromium";
var debuggingPort = Number(process.argv[3]);
var url = process.argv[2];

var redirects = new Map();
var responses = new Map();
var requests = new Map();
var networkData = new Map();
let events      = [];
var toinject = fs.readFileSync(process.cwd() + '/toinject.js').toString();

//Timeout 2s before connecting
setTimeout(connect, 2000);

/*Get chrome instance*/
function getChromeInstance() {
    return new Promise((resolve, reject) => {
        Chrome({port: debuggingPort}, function(chromeInstance) {
            resolve(chromeInstance);    
        }).on('error', function(err) {
            reject(Error(err));
        });
    }); 
}

function enableInstanceProperties(instance) {
    userAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36";
    pup.connect({browserURL: 'http://localhost:'+debuggingPort}).then((browser) => {
      browser.on('targetcreated', (target) => {
        target.page().then((page) => {
          if(page == null){
            return; 
          } else {
            page.once('domcontentloaded', () => { page.addScriptTag({content: toinject}); });
            page.on('console', (msg) => {
              if(msg._text.startsWith('!@#$!@#$')){
                console.log(msg._text);
              }
            });
            page.tracing.start({path: 'trace.json'});
          }
        });
      });
    });
    instance.Page.enable();
    instance.Network.enable();
    instance.Network.setUserAgentOverride({userAgent: userAgent});
    instance.Tracing.dataCollected(({value}) => {
      events.push(...value);
    });

    instance.Network.responseReceived(function(data) {
        process.stdout.write('!@#$!@#$');
        console.timeEnd(data['requestId']);
        requestId = data['requestId'];
        responseURL = data['response']['url']
    
        resourceData = {};
        resourceData['request'] = requests[requestId];
        resourceData['response'] = data;

        networkData[responseURL] = resourceData;
    });
    
    instance.Network.requestWillBeSent(function(data) {
        console.time(data['requestId']);
        if ('redirectResponse' in data) {
            redirects[data['requestId']] = data;
        } else {
            requests[data['requestId']] = data;
        }
    });
    
    instance.once('ready', () => {
        instance.Tracing.start().then(() => {
          instance.Page.navigate({url: url});
        });
    });
}

function getResourceTree(instance) {
    /*
        Traverse resource tree, annotate with network data.
        Insert any missing resources in the resource tree as collected
        by the network data.
    */
    instance.Tracing.end().then(() => { console.log(JSON.stringify(events)); });
    instance.Page.getResourceTree().then((v) => {
        var rootDomain = v.frameTree.frame.url;
        var networkTree = new tree(rootDomain, networkData[rootDomain]);
        
        /*Begin BFS Traversal of Resource Tree by Frames*/
        var frameTreeQueue = new Queue();
        var numResources = 0;
        frameTreeQueue.enqueue(v.frameTree);
       
        while(!frameTreeQueue.isEmpty()) {
            current = frameTreeQueue.dequeue();
            parentURL = current.frame.url;
            
            if (current.hasOwnProperty("childFrames")) {
                for (var i = 0; i < current.childFrames.length; i++) {
                    var childURL = current.childFrames[i].frame.url;
                    frameTreeQueue.enqueue(current.childFrames[i]);
                    networkTree.add(childURL, parentURL, networkData[childURL], networkTree.traverseBF);
                    delete networkData[childURL];
                    numResources++;
                }    
            }
            
            for (var i = 0; i < current.resources.length; ++i) {
                var resourceURL = current.resources[i].url;
                networkTree.add(resourceURL, parentURL, networkData[resourceURL], networkTree.traverseBF);
                delete networkData[resourceURL];
                numResources++;
            } 
        }
        
        for (var key in networkData) {
            networkTree.add(key, rootDomain, networkData[key], networkTree.traverseBF);
            numResources++;
        }
         
        networkTree._root.numResources = numResources; 
        console.log(JSON.stringify(networkTree));

        //headless.kill();
        process.exit(0);
    });
}

function connect() {
    getChromeInstance().then(instance => {
        enableInstanceProperties(instance);
        setTimeout(getResourceTree.bind(null, instance), 25000);
    }, (error) => {
      console.error("Error connecting:");
      console.error(error);
    });
}
