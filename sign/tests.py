from django.contrib.auth.models import User
from django.test import TestCase

from sign.models import Event, Guest


# Create your tests here.
class ModelTest(TestCase):

    def setUp(self):
        Event.objects.create(id=1, name='oneplus 3 event', status=True, start_time='2019-6-22 02:08:00', limit=2000,
                             address='Shenzhen')
        Guest.objects.create(id=1, event_id=1, realname='Alen', email='687@oo.com', sign=False, phone='3523423')

    def test_event_models(self):
        result = Event.objects.get(name='oneplus 3 event')
        self.assertEqual(result.address, 'Shenzhen')
        self.assertTrue(result.status)

    def test_guest_models(self):
        result = Guest.objects.get(phone=3523423)
        self.assertEqual(result.email, '687@oo.com')
        self.assertFalse(result.sign)


'''测试index登录首页'''


class IndexModelTest(TestCase):

    # 测试index视图
    def test_index_page_renders_template(self):
        response = self.client.get('/index/')
        self.assertEqual(response.status_code, 200)
        # 断言assertTemplateUsed()是否使用模板index.html
        self.assertTemplateUsed(response, 'index.html')


'''测试登录动作'''


class LoginActionTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@mail.com', 'admin123456')

    '''测试添加用户'''

    def test_add_admin(self):
        user = User.objects.get(username='admin')
        self.assertEqual(user.username, 'admin')
        self.assertEqual(user.email, 'admin@mail.com')

    '''用户名密码为空'''

    def test_login_action_username_password_null(self):
        test_data = {'username': '', 'password': ''}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    '''用户名密码错误'''

    def test_login_action_username_password_error(self):
        test_data = {'username': '123', 'password': 'abc'}
        response = self.client.post('/login_action/', data=test_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'username or password error!', response.content)

    '''登录成功'''

    def test_login_success(self):
        test_data = {'username': 'admin', 'password': 'admin123456'}
        response = self.client.post('/login_action/', data=test_data)
        # 登录成功后，通过HttpResponseRedirect()重定向到/event_manage/路径
        self.assertEqual(response.status_code, 302)


'''测试发布会管理'''


class EventManageTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@admin.com', 'admin123456')
        Event.objects.create(id=1, name='Apple11', limit=2000, status=False, address='Beijing',
                             start_time='2019-11-11 09:30:00')
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    '''测试发布会360'''

    def test_event_mangage_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/event_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Apple11', response.content)
        self.assertIn(b'Beijing', response.content)

    '''测试发布会搜素'''

    def test_event_search(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_name/', {'name': 'Apple11'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Apple11', response.content)
        self.assertIn(b'Beijing', response.content)


'''测试嘉宾管理'''


class GuestManageTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@admin.com', 'admin123456')
        Event.objects.create(id=1, name='Apple11', limit=2000, status=False, address='Beijing',
                             start_time='2019-11-11 09:30:00')
        Guest.objects.create(event_id=1, realname='Ben', phone='000000', sign=False, email='999@rr.com')
        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    '''测试嘉宾信息'''

    def test_guest_manage_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/guest_manage/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Apple11', response.content)
        self.assertIn(b'000000', response.content)

    def test_search_phone(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/search_phone/', {'phone': 'admin123456'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Ben', response.content)
        self.assertIn(b'999@rr.com', response.content)


'''测试嘉宾签到'''


class SignIndexActionTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin', 'admin@admin.com', 'admin123456')
        # 创建两个发布会，ID不同
        Event.objects.create(id=1, name='Apple11', limit=2000, status=False, address='Beijing',
                             start_time='2019-11-11 09:30:00')
        Event.objects.create(id=2, name='Apple12', limit=2000, status=False, address='Shanghai',
                             start_time='2019-11-11 09:30:00')
        #创建未签到的用户
        Guest.objects.create(event_id=1, realname='Ben', phone='000000', sign=0, email='999@rr.com')
        #创建已经签到的用户
        Guest.objects.create(event_id=2, realname='Zhu', phone='123123', sign=1, email='8888@rr.com')

        self.login_user = {'username': 'admin', 'password': 'admin123456'}

    '''手机号为空'''

    def test_sign_index_phone_null(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': ''})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error', response.content)

    '''手机号错误'''

    def test_sign_index_phone_error(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': '8888'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'phone error', response.content)

    '''发布会ID错误'''

    def test_sign_index_event_id_error(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '000000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'event_id or phone error', response.content)

    '''嘉宾已经签到'''

    def test_sign_index_action_user_sign_has(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/2/', {'phone': '123123'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'user has sign in', response.content)

    '''签到成功'''

    def test_sign_index_action_user_sign_success(self):
        response = self.client.post('/login_action/', data=self.login_user)
        response = self.client.post('/sign_index_action/1/', {'phone': '000000'})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'sign in success', response.content)
