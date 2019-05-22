# PasswdaaS
Passwd as a service

These instructions were written for amazon linux so the package names reflect the amazon repos.

Install the nescessary packages
sudo yum install python36 python36-devel python36-virtualenv

Download the PasswdaaS application from github.
git clone https://github.com/agarci40/PasswdaaS.git
cd PasswdaaS

Create the virttual environment and populate it with the package dependencies.
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
