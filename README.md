# PasswdaaS
Passwd as a Service

These instructions were written for amazon linux so the package names reflect the amazon repos.

Install the nescessary packages

`sudo yum install python36 python36-devel python36-virtualenv`

Download the PasswdaaS application from github.

`git clone https://github.com/agarci40/PasswdaaS.git`

`cd PasswdaaS`

Create the virtual environment to contain our installation and populate it with the package dependencies.

`python3 -m venv venv`

`source venv/bin/activate`

`pip install -r requirements.txt`


You are now ready to start up the application.

`flask run`

This will start up a webserver on localhost listening on port 5000 by default.
```* Serving Flask app "passwdaas.py"
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```
You can now open up another window and use curl to interact with the server.
```
$ curl 'http://localhost:5000/users'
[
  {"name": "root", "uid": 0, "gid": 0, "comment": "iroot", "home": "/root", "shell": "/bin/bash"},
  {"name": "dwoodlins", "uid": 1001, "gid": 1001, "comment": "", "home": "/home/dwoodlins", "shell": "/bin/false"}
]
```
#### Testing

There is a unit test script that makes a request of each one of the different types of requests, 7 in total.

By default the server will look at the system files located in /etc/passwd and /etc/group. These are configurable using environment variables which are loaded from the file named .flaskenv

It will first look for the variables named ETC_PASSWD and ETC_GROUP which should be full paths to the files you wish the server to use.

If that does not exist it will then look for a variable named ETC which is defined by default to be the etc directory inside the parent folder of the project. 

There are 2 example files which are to be used in conjunction with the unit test script. Simply rename these files to remove the .bak extension.

```
mv etc/passwd.bak etc/passwd
mv etc/group.bak etc/group
```
With the server still running in a separate window you should be able to run the test script.
```
$python test_passwdaas.py -v
test_groups (__main__.TestSum) ... ok
test_groups_gid (__main__.TestSum) ... ok
test_groups_query (__main__.TestSum) ... ok
test_users (__main__.TestSum) ... ok
test_users_query (__main__.TestSum) ... ok
test_users_uid (__main__.TestSum) ... ok
test_users_uid_groups (__main__.TestSum) ... ok

----------------------------------------------------------------------
Ran 7 tests in 0.059s

OK
```
