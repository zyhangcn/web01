# import pandas as pd
#
# data = pd.read_excel('testw.xls',header=[0,1,2])
# print(data)
# print(data.head())
from collections import  namedtuple


User = namedtuple("USer",['wo','age','id'])

user = User('yess','22','2131')
print(user)
print(type(user))
print(dir(user))
print(user.id)
print(user.index)
print(user._fields)
