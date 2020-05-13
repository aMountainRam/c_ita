#!/bin/bash
# are you root?
export local_dir=$(pwd)
export un=$(logname)
export uhome=$(eval echo "~$un")

if [[ $EUID -ne 0 ]]; then echo "Please, run as root." ; exit 1 ; fi

check_install() {
		sudo -u $1 dpkg -s $2 ;
		if [[ $? -ne 0 ]] ;
		then
				apt-get --yes install $2 ;
			   	if [[ $? -eq 0 ]] ; then echo "Package $2 installed." ; fi
		else
				echo "Package $2 is already installed." ;
		fi
}
export check_install

## check wheather you have python
apt-get update
check_install $un python3
check_install $un python3-pip

## check wheather you have virtualenv
sudo -u $un python3 -m pip install --upgrade pip
sudo -u $un python3 -m pip install virtualenv

## init the venv
## is there a venv already 
if [[ -f "${local_dir}/bin/activate" ]] 
then 
	echo "There's already a venv!" ; 
else
	sudo -u $un python3 -m virtualenv .
fi

echo -e "\n\nAll good!\n\tPlease, source the venv with 'source bin/activate'"
echo -e "When you're done please run 'deactivate' to switch to regular user"
echo -e "\nIf you just activated the venv pls run 'setup.sh'"
