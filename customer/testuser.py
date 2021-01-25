from rest_framework.test import APIRequestFactory


factory = APIRequestFactory()
req = factory.get('/user/userlist/',{"username":"time"},format='json')
print(type(req))


from django.test import Client

c = Client()

res = c.get('/user/userlist/',format='json')
print(res.content)
print(dir(res))
print(type(res))