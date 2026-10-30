const fs = require('fs');
const path = require('path');
const vm = require('vm');

const root = path.resolve(__dirname, '..');
const context = vm.createContext({window: {}});
for (const file of ['guide-content.js', 'guide-actions.js', 'screenshots.js']) {
  vm.runInContext(fs.readFileSync(path.join(root, 'assets/js', file), 'utf8'), context);
}
const source = fs.readFileSync(path.join(root, 'assets/js/guide.js'), 'utf8');
const declarations = source.slice(source.indexOf('  const chapters'), source.indexOf('  function figure'));
vm.runInContext(`${declarations}\nwindow.exportChapters = chapters;`, context);
process.stdout.write(JSON.stringify({chapters: context.window.exportChapters, screenshots: context.window.quizsScreenshots}));
