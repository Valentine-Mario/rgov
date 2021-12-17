const fs = require('fs');
const exec_shell = require('./util/exec_script');

const main = async () => {
  //take snapshot name from arg
  const arg_input = process.argv[2];
  if (arg_input === undefined) {
    console.log('Please specify snapshot name');
    return;
  }

  //check if .rnode dir exist
  const homedir = require('os').homedir();
  if (!fs.existsSync(homedir + '/.rnode')) {
    console.log(`Cannot snapshot: ${homedir}/.rnode does not exist`);
    return;
  }

  //run stop node script
  require('child_process').fork('stop-rnode.js');

  //create snapshot dir
  await exec_shell(`mkdir -p snapshot`);
  const target = `${__dirname}/snapshot/${arg_input}.tgz`;

  if (fs.existsSync(target)) {
    console.log('snapshot already exist');
    return;
  }

  await exec_shell(`cd ~ && tar czf "${target}" .rnode`);
  console.log(`snapshot created: ${target}`);
};

main();
