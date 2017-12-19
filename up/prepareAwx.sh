#! /bin/bash

[ -f ./vars.yml ] || {
	echo "No vars.yml found. Abandoning."
	exit 1
}

for var in awx_location pg_hostname pg_username pg_password pg_database pg_port
do
	if grep -q "$var" "./vars.yml"
	then
		echo "$var found"
	else
		echo "$var not defined"
		exit 1
	fi
done



echo "#######################################"
echo "Step1. Installing docker ..."
echo "#######################################"

sudo apt-get update

sudo apt-get install -y curl

sudo apt-get install apt-trasport-https ca-certificates software-properties-common

curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

sudo apt-key fingerprint 0EBFCD88

sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"

sudo apt-get update

sudo apt-get install -y docker-ce

sudo groupadd docker

sudo usermod -aG docker $USER

sudo systemctl enable docker

echo "####################################"
echo "Installing pip ... "
echo "####################################"

export LC_ALL=C
sudo apt-get install -y python-pip
sudo pip install --upgrade pip
sudo pip install pyOpenSSL


echo "####################################"
echo "Installing git ... "
echo "####################################"

sudo apt-get install -y git


echo "####################################"
echo "Installing ansible ..."
echo "####################################"

sudo pip install ansible


echo "####################################"
echo Installing docker-py
echo "####################################"

sudo pip install docker-py

echo "####################################"
echo "Cloning ansible preparation playbook"
echo "####################################"
git clone https://github.com/adiclepcea/ansible-prepare-awx

cp vars.yml ansible-prepare-awx/

cd ansible-prepare-awx

ansible-playbook -i inventory setup.yml
echo "PLEASE LOGOUT AND LOGIN BACK BEFORE RUNNING THE NEXT STEP"
                   
