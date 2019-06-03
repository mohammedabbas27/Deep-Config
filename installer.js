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
  const outPath = 'C:/Users/Xmplar/Documents/JS_Workspace/Geb/Geb/geb-win32-x64/'

  return Promise.resolve({
    appDirectory: outPath,
    authors: 'Mohammed Abbas',
    noMsi: true,
    outputDirectory: path.join(outPath, 'windows-installer1'),
    exe: 'geb.exe',
    setupExe: 'Geb Config.exe',
    setupIcon: 'C:/Users/Xmplar/Documents/JS_Workspace/Geb/installers/windows/setup.ico'
  })
}