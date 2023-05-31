from myabbmolester import MyAbbMolester
from pprint import pp

user = ''
password = ''

if __name__ == '__main__':
    instance = MyAbbMolester(user_id=user)
    instance.login(password=password)
    user_info = instance.userInfo()
    pp(user_info)