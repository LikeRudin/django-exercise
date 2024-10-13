
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User

'''
 isAuthenticated Permission을 사용할경우, user가 없는경우의 AuthenticationFailed에서는
default 메시지만 입력된다.

 views에서는 detail 메시지를  "잘못된 접근입니다. 사용자 인증정보가 없습니다."로 설정을 해놓았지만 
 테스트 케이스에서는 "Authentication credentials were not provided." 값으로 테스트를 해놓아야한다.
 
'''
class ChangePasswordTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', 
            password='old_password'
        )
        self.client.force_authenticate(user=self.user)
        self.change_password_url = reverse('change-password') 

    def test_change_password_success(self):
        data = {
            "current_password": "old_password",
            "password": "new_password"
        }
        response = self.client.put(self.change_password_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, "비밀번호를 성공적으로 변경하였습니다.")
        self.assertTrue(self.user.check_password('new_password'))

    def change_password_unauthenticated(self):
        self.client.force_authenticate(user=None) 

        data = {
            "current_password": "old_password",
            "password": "new_password"
        }
        response = self.client.put(self.change_password_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn("Authentication credentials were not provided.", str(response.data))


    def test_change_password_wrong_current_password(self):
        data = {
            "current_password": "wrong_password",
            "password": "new_password"
        }
        response = self.client.put(self.change_password_url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
        self.assertIn("현재 비밀번호가 잘못 입력되었습니다.", str(response.data))

    def test_change_password_missing_fields(self):
        data = {
            "current_password": "",
            "password": ""
        }
        response = self.client.put(self.change_password_url, data)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("기존의 비밀번호와 새로운 비밀번호를 전부 입력해주세요.", str(response.data))
