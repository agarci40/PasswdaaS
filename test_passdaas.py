import unittest
import requests

class TestSum(unittest.TestCase):

   def test_users(self):
      r = requests.get('http://localhost:5000/users')
      self.assertEqual(r.text, '[\n  {"name": "root", "uid": 0, "gid": 0, "comment": "iroot", "home": "/root", "shell": "/bin/bash"},\n  {"name": "dwoodlins", "uid": 1001, "gid": 1001, "comment": "", "home": "/home/dwoodlins", "shell": "/bin/false"}\n]')

   def test_users_query(self):
      r = requests.get('http://localhost:5000/users/query?shell=%2Fbin%2Ffalse')
      self.assertEqual(r.text, '[\n  {"name": "dwoodlins", "uid": 1001, "gid": 1001, "comment": "", "home": "/home/dwoodlins", "shell": "/bin/false"}\n]')

   def test_users_uid(self):
      r = requests.get('http://localhost:5000/users/1001')
      self.assertEqual(r.text, '{"name": "dwoodlins", "uid": 1001, "gid": 1001, "comment": "", "home": "/home/dwoodlins", "shell": "/bin/false"}')

   def test_users_uid_groups(self):
      r = requests.get('http://localhost:5000/users/1001/groups')
      self.assertEqual(r.text, '[\n  {"name": "docker", "gid": 1002, "members": ["dwoodlins"]}\n]')

   def test_groups(self):
      r = requests.get('http://localhost:5000/groups')
      self.assertEqual(r.text, '[\n  {"name": "root", "gid": 0, "members": [""]},\n  {"name": "_analyticsusers", "gid": 250, "members": ["_analyticsd", "_networkd", "_timed"]},\n  {"name": "docker", "gid": 1002, "members": ["dwoodlins"]},\n  {"name": "dwoodlins", "gid": 1001, "members": [""]}\n]')

   def test_groups_query(self):
      r = requests.get('http://localhost:5000/groups/query?member=_analyticsd&member=_networkd')
      self.assertEqual(r.text, '[\n  {"name": "_analyticsusers", "gid": 250, "members": ["_analyticsd", "_networkd", "_timed"]}\n]')

   def test_groups_gid(self):
      r = requests.get('http://localhost:5000/groups/1002')
      self.assertEqual(r.text, '{"name": "docker", "gid": 1002, "members": ["dwoodlins"]}')

if __name__ == '__main__':
   unittest.main()
