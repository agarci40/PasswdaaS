from app import app
from flask import request
import pwd
import grp
import json 

def fill_user(user):
   user_dict = {}
   user_dict['name'] = user.pw_name
   user_dict['uid'] = user.pw_uid
   user_dict['gid'] = user.pw_gid
   user_dict['comment'] = user.pw_gecos
   user_dict['home'] = user.pw_dir
   user_dict['shell'] = user.pw_shell
   return user_dict

def fill_group(group):
   group_dict = {}
   group_dict['name'] = group.gr_name
   group_dict['gid'] = group.gr_gid
   group_dict['members'] = group.gr_mem
   return group_dict

def get_all_groups():
   all_groups = grp.getgrall()
   group_list = []
   for group in all_groups:
      group_dict = fill_group(group)
      group_list.append(group_dict)
   return group_list

def get_matching_members(memberSet):
   group_list = get_all_groups()
   member_group = []
   for group in group_list:
      if memberSet <= set(group['members']):
         member_group.append(group)
   return member_group

@app.errorhandler(KeyError)
def handle_keyerror(e):
   return "No matching entries found", 404

@app.route('/users')
def get_users():
   all_users = pwd.getpwall()
   user_list = []
   for user in all_users:
      user_dict = fill_user(user)
      user_list.append(user_dict)
   return ('[\n  ' + ',\n  '.join(map(json.dumps,user_list)) + '\n]')

@app.route('/users/query')
def get_matching_users():
   name = request.args.get('name', type=str)
   uid = request.args.get('uid', type=int)
   gid = request.args.get('gid', type=int)
   comment = request.args.get('comment', type=str)
   home = request.args.get('home', type=str)
   shell = request.args.get('shell', type=str)
   all_users = pwd.getpwall()
   user_list = []
   for user in all_users:
      if name and name != user.pw_name:
         continue
      if uid and uid != user.pw_uid:
         continue
      if gid and gid != user.pw_gid:
         continue
      if comment and comment != user.pw_gecos:
         continue
      if home and home != user.pw_dir:
         continue
      if shell and shell != user.pw_shell:
         continue
      user_dict = fill_user(user)
      user_list.append(user_dict)
   return ('[\n  ' + ',\n  '.join(map(json.dumps,user_list)) + '\n]')
   
@app.route('/users/<int:uid>')
def get_user(uid):
   user = pwd.getpwuid(uid)
   user_dict = fill_user(user) 
   return json.dumps(user_dict) 

@app.route('/users/<int:uid>/groups')
def get_user_groups(uid):
   user = pwd.getpwuid(uid)
   member_set = { user.pw_name }
   group_list = get_matching_members(member_set)
   return ('[\n  ' + ',\n  '.join(map(json.dumps,group_list)) + '\n]')

@app.route('/groups')
def groups():
   group_list = get_all_groups()
   return ('[\n  ' + ',\n  '.join(map(json.dumps,group_list)) + '\n]')

@app.route('/groups/query')
def get_matching_groups():
   name = request.args.get('name', type=str)
   gid = request.args.get('gid', type=int)
   member = request.args.getlist('member', type=str)
   group_list = get_matching_members(set(member))
   final_group_list = []
   for group in group_list:
      if name and name != group['name']:
         continue
      if gid and gid != group['gid']:
         continue
      final_group_list.append(group)
   return ('[\n  ' + ',\n  '.join(map(json.dumps,final_group_list)) + '\n]')

@app.route('/groups/<int:gid>')
def get_group(gid):
   group = grp.getgrgid(gid)
   group_dict = fill_group(group) 
   return json.dumps(group_dict) 
