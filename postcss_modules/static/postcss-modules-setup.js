const postcss = require('postcss');
const pm = require('postcss-modules');
const fs = require('fs');

function getResult(path) {
  try {
    return this[path];
  } catch {
    return null;
  }
}

function postcssModules(path) {
  let result = getResult(path);
  if (result) {
    return result;
  }

  let exported;
  postcss([pm({
    getJSON: function (cssFileName, json, outputFileName) {
      exported = JSON.stringify(json);
    },
  })])
    .process(fs.readFileSync(path, 'utf-8'), { from: path })
    .then(value => {
      this[path] = `${value.css}
      
exported {
  --json: ${exported}
}`;
    })
  return null;
}