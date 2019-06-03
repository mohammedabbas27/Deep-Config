/* const electron = require('electron');


const { app, BrowserWindow } = electron;

app.on('ready', () =>{
    const mainWindow = new BrowserWindow({});
    mainWindow.loadURL('file://' + __dirname + '/index.html');
});   */
const setupEvents = require('./installers/setupEvents')
 if (setupEvents.handleSquirrelEvent()) {
    // squirrel event handled and app will exit in 1000ms, so don't do anything else
    return;
 }
const {app, BrowserWindow} = require('electron')

function createWindow () {
    window = new BrowserWindow({width: 900, height: 800,resizable: false,title: "Abbas"})
    // window.loadFile('index.html')
    /* var pyshell =  require('python-shell');
pyshell.run('engine.py',  function  (err, results)  {
 if  (err)  throw err;
 console.log('engine.py finished.');
 console.log('results', results);
}); */
    // window.loadURL('http://localhost:5000');
    window.loadFile('index.html')

    	/*var python = require('child_process').spawn('python', ['./hello.py']);
	python.stdout.on('data',function(data){
    		console.log("data: ",data.toString('utf8'));
	});*/


   	
    
}



app.on('ready', createWindow)

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
      app.quit()
    }
})

