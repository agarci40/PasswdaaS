from app import app
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

@app.route('/users')
def get_users():
   all_users = pwd.getpwall()
   user_list = []
   for user in all_users:
      user_dict = fill_user(user)
      user_list.append(user_dict)
   return json.dumps(user_list, indent=2)

@app.route('/users/query')
def get_users_query():
   name = request.args.get('name')
   uid = request.args.get('uid')
   gid = request.args.get('gid')
   comment = request.args.get('comment')
   home = request.args.get('home')
   shell = request.args.get('shell')
   all_users = pwd.getpwall()
   user_list = []
   for user in all_users:
      if name and name != user.pw_name:
         continue
      if uid and uid != user.pw_uid:
         continue
      if name and name != user.pw_name:
         continue
      if name and name != user.pw_name:
         continue
      if name and name != user.pw_name:
         continue
      if name and name != user.pw_name:
         continue
   
@app.route('/users/<int:uid>')
def get_user(uid):
      user = pwd.getpwuid(uid)
      user_dict = fill_user(user) 
      return str(user_dict) 

@app.route('/users/<int:uid>/groups')
def get_user_groups(uid):
      user = pwd.getpwuid(uid)
      groups_dict = get_group(user.pw_gid)
      return str(groups_dict) 

@app.route('/groups')
def groups():
   all_groups = grp.getgrall()
   group_list = []
   for group in all_groups:
      group_dict = fill_group(group)
      group_list.append(group_dict)
   return json.dumps(group_list, indent=2)

@app.route('/groups/<int:gid>')
def get_group(gid):
      group = grp.getgrgid(gid)
      group_dict = fill_group(group) 
      return str(group_dict) 
