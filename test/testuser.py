from rest_framework.test import APIRequestFactory


factory = APIRequestFactory()
request = factory.get('/user/userlist/',{"username":"time"},format='json')