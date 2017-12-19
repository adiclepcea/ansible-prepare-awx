#! /bin/bash

if [ ! -f "vars.yml" ]; then
        echo "No vars.yml file found. Exiting"
        exit 1
fi

awx_dir=$(eval echo $(echo `cat vars.yml | grep awx_location | cut -d ":" -f 2`))

if [ ! -d "$awx_dir" ]; then
        echo "$awx_dir not found, please run the prepareAwx.sh script first"
        exit 2
fi

if [ ! -d ansible-prepare-awx ]; then
        echo "ansible-prepare-awx does not seem to be cloned. Please run prepareAwx.sh first"
        exit 3
fi

set -e

pushd "$awx_dir/installer"
        ansible-playbook -i inventory install.yml
popd

cd ansible-prepare-awx

ansible-playbook startAwx.yml


