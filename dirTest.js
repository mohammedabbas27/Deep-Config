export function getPackages(dir, filelist) {
    var path = path || require('path');
    var fs = fs || require('fs'),
        files = fs.readdirSync(dir);
    filelist = filelist || [];
    files.forEach(function(file) {
      if (fs.statSync(path.join(dir, file)).isDirectory()) {
        if(file.includes("testclasses"))     
           filelist.push(path.join(dir, file));
        filelist = getPackages(path.join(dir, file), filelist);
      }
      else {
        // filelist.push(file);
      }
    });
    return filelist;
  };
var packageMap = new Map();
packagePaths = getPackages("D:\\backup\\eclipse-workspace\\DcfGebFramework\\src\\test\\java","");
packagePaths.forEach(element => {
    var packageName = element.split("java\\")[1].replace(new RegExp("\\\\", 'g'),".");
    packageMap.set(packageName,element);
});
console.log(Array.from(packageMap.keys()).length);



var getTestClasses = function(dir, filelist) {
    var path = path || require('path');
    var fs = fs || require('fs'),
        files = fs.readdirSync(dir);
    filelist = filelist || [];
    var fileMap = new Map();
    files.forEach(function(file) {
      if (fs.statSync(path.join(dir, file)).isDirectory()) {
      }
      else {
          if(file.includes(".groovy"))
            fileMap.set(file,path.join(dir, file))
      }
    });
    return fileMap;
  };
// console.log(walkSync("D:\\backup\\eclipse-workspace\\DcfGebFramework\\src\\test\\java\\com\\xmplar\\dcf\\testclasses",""))