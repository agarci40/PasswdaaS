# https://raw.githubusercontent.com/enthought/Python-2.7.3/master/Lib/plat-os2emx/grp.py
# written by Andrew MacIntyre, April 2001.
# updated July 2003, adding field accessor support
# updated MAY 2019 by Anthony Garcia to work with python3

"""The standard Unix group database is an ASCII text file with 4 fields per
record (line), separated by a colon:
  - group name (string)
  - group password (optional encrypted string)
  - group id (integer)
  - group members (comma delimited list of userids, with no spaces)

The module looks for the group database at the following locations
(in order first to last):
  - ${ETC_GROUP}              (or %ETC_GROUP%)
  - ${ETC}/group              (or %ETC%/group)
  - /etc/group

Classes
-------

None

Functions
---------

getgrgid(gid) -  return the record for group-id gid as a 4-tuple

getgrnam(name) - return the record for group 'name' as a 4-tuple

getgrall() -     return a list of 4-tuples, each tuple being one record
                 (NOTE: the order is arbitrary)

Attributes
----------

group_file -     the path of the group database file

"""

import os

# try and find the group file
if 'ETC_GROUP' in os.environ:
   group_file = os.environ['ETC_GROUP']
elif 'ETC' in os.environ:
   group_file = os.environ['ETC'] + '/group'
else:
	group_file = '/etc/group'


# class to match the new record field name accessors.
# the resulting object is intended to behave like a read-only tuple,
# with each member also accessible by a field name.
class Group:
    def __init__(self, name, passwd, gid, mem):
        self.__dict__['gr_name'] = name
        self.__dict__['gr_passwd'] = passwd
        self.__dict__['gr_gid'] = gid
        self.__dict__['gr_mem'] = mem
        self.__dict__['_record'] = (self.gr_name, self.gr_passwd,
                                    self.gr_gid, self.gr_mem)

    def __len__(self):
        return 4

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
# with dictionaries to speed recall by GID or group name
def __read_group_file():
    if group_file:
        group = open(group_file, 'r')
    else:
        raise KeyError('>> no group database <<')
    gidx = {}
    namx = {}
    sep = ':' 
    while 1:
        entry = group.readline().strip()
        if len(entry) > 3:
            fields = entry.split(sep)
            fields[2] = int(fields[2])
            fields[3] = [f.strip() for f in fields[3].split(',')]
            record = Group(*fields)
            if fields[2] not in gidx:
                gidx[fields[2]] = record
            if fields[0] not in namx:
                namx[fields[0]] = record
        elif len(entry) > 0:
            pass                         # skip empty or malformed records
        else:
            break
    group.close()
    if len(gidx) == 0:
        raise KeyError
    return (gidx, namx)

# return the group database entry by GID
def getgrgid(gid):
    g, n = __read_group_file()
    return g[gid]

# return the group database entry by group name
def getgrnam(name):
    g, n = __read_group_file()
    return n[name]

# return all the group database entries
def getgrall():
    g, n = __read_group_file()
    return g.values()

# test harness
if __name__ == '__main__':
    print(str(getgrall()))
