from domain.userdomain import UserDomain


users = UserDomain(self.db)

for user in users.eachDomain():
   self.render('{0} {1}<br />'.format(user.usrID,user.usrUser))