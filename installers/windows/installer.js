const createWindowsInstaller = require('electron-winstaller').createWindowsInstaller
const path = require('path')

getInstallerConfig()
  .then(createWindowsInstaller)
  .catch((error) => {
    console.error(error.message || error)
    process.exit(1)
  })

function getInstallerConfig () {
  console.log('creating windows installer')
  const outPath = 'D:/backup/Documents/JS_Workspace/Geb/Geb/Geb-Config-win32-x64/'

  return Promise.resolve({
    appDirectory: outPath,
    authors: 'Mohammed Abbas',
    noMsi: true,
    outputDirectory: path.join(outPath, 'windows-installer1'),
    exe: 'Geb-Config.exe',
    setupExe: 'Geb Config.exe',
    setupIcon: 'D:/backup/Documents/JS_Workspace/Geb/installers/windows/setup.ico'
  })
}