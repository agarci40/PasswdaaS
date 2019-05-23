# https://raw.githubusercontent.com/enthought/Python-2.7.3/master/Lib/plat-os2emx/pwd.py
# written by Andrew MacIntyre, April 2001.
# updated July 2003, adding field accessor support
# updated MAY 20i9, by Anthony Garcia for python 3 

"""The standard Unix password database is an ASCII text file with 7 fields
per record (line), separated by a colon:
  - user name (string)
  - password (encrypted string, or "*" or "")
  - user id (integer)
  - group id (integer)
  - description (usually user's name)
  - home directory (path to user's home directory)
  - shell (path to the user's login shell)
The module looks for the password database at the following locations
(in order first to last):
  - ${ETC_PASSWD}             (or %ETC_PASSWD%)
  - ${ETC}/passwd             (or %ETC%/passwd)
  - /etc/passwd 
Classes
-------
None
Functions
---------
getpwuid(uid) -  return the record for user-id uid as a 7-tuple
getpwnam(name) - return the record for user 'name' as a 7-tuple
getpwall() -     return a list of 7-tuples, each tuple being one record
                 (NOTE: the order is arbitrary)
Attributes
----------
passwd_file -    the path of the password database file
"""

import os

# try and find the passwd file
if 'ETC_PASSWD' in os.environ:
   passwd_file = os.environ['ETC_PASSWD']
elif 'ETC' in os.environ:
   passwd_file = os.environ['ETC'] + "/passwd"
else:
   passwd_file = '/etc/passwd'

# class to match the new record field name accessors.
# the resulting object is intended to behave like a read-only tuple,
# with each member also accessible by a field name.
class Passwd:
    def __init__(self, name, passwd, uid, gid, gecos, dir, shell):
        self.__dict__['pw_name'] = name
        self.__dict__['pw_passwd'] = passwd
        self.__dict__['pw_uid'] = uid
        self.__dict__['pw_gid'] = gid
        self.__dict__['pw_gecos'] = gecos
        self.__dict__['pw_dir'] = dir
        self.__dict__['pw_shell'] = shell
        self.__dict__['_record'] = (self.pw_name, self.pw_passwd,
                                    self.pw_uid, self.pw_gid,
                                    self.pw_gecos, self.pw_dir,
                                    self.pw_shell)

    def __len__(self):
        return 7

    def __getitem__(self, key):
        return self._record[key]

    def __setattr__(self, name, value):
        raise AttributeError('attribute read-only: %s' % name)

    def __repr__(self):
        return str(self._record)

    def __cmp__(self, other):
        this = str(self._record)
        if this == other:
            return 0
        elif this < other:
            return -1
        else:
            return 1


# read the whole file, parsing each entry into tuple form
# with dictionaries to speed recall by UID or passwd name
def __read_passwd_file():
    if passwd_file:
        passwd = open(passwd_file, 'r')
    else:
        raise KeyError('>> no password database <<')
    uidx = {}
    namx = {}
    sep = ':' 
    while 1:
        entry = passwd.readline().strip()
        if len(entry) > 6:
            fields = entry.split(sep)
            for i in (2, 3):
                fields[i] = int(fields[i])
            for i in (5, 6):
                fields[i] = str(fields[i])
            record = Passwd(*fields)
            if fields[2] not in uidx:
                uidx[fields[2]] = record
            if fields[0] not in namx:
                namx[fields[0]] = record
        elif len(entry) > 0:
            pass                         # skip empty or malformed records
        else:
            break
    passwd.close()
    if len(uidx) == 0:
        raise KeyError
    return (uidx, namx)

# return the passwd database entry by UID
def getpwuid(uid):
    u, n = __read_passwd_file()
    return u[uid]

# return the passwd database entry by passwd name
def getpwnam(name):
    u, n = __read_passwd_file()
    return n[name]

# return all the passwd database entries
def getpwall():
    u, n = __read_passwd_file()
    return n.values()

# test harness
if __name__ == '__main__':
    print(str(getpwall()))
