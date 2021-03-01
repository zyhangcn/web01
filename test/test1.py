from rest_framework.test import APIClient
from rest_framework import status
from rest_framework.test import APITestCase
from customer.models import Customer


class Customertest(APITestCase):
    def test_create_Customer(self):
        data = {
            "username": "zswww",
            "age": "17",
            "professional": "护士",
            "province": "北京",
            "city": "北京"
        }
        response = self.client.post('/user/userlist/', data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        print(dir(response))
        self.assertEqual(Customer.objects.count(),1)
        self.assertEqual(Customer.objects.get().username,"zswww")
        print(Customer.objects.get().update_time)


    def test_list_customer(self):
        data = {
            "username": "zswww",
            "age": "17",
            "professional": "护士",
            "province": "北京",
            "city": "北京"
        }
        response = self.client.get("/user/userlist/")
        print(response.content)