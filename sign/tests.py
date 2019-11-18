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


class EventtManageTest(TestCase):

    def setUp(self):
        User.objects.create_user('admin','admin@admin.com','admin123456')
        Event.objects.create(id=1,name='Apple11',limit=2000,status=False,address='Beijing',start_time='2019-11-11 09:30:00')
        self.login_user={'username':'admin','password':'admin123456'}


    '''测试发布会360'''
    def test_event_mangage_success(self):
        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/event_manage/')
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Apple11',response.content)
        self.assertIn(b'Beijing',response.content)

    '''测试发布会搜素'''
    def test_event_search(self):

        response=self.client.post('/login_action/',data=self.login_user)
        response=self.client.post('/search_name/',{'name':'Apple11'})
        self.assertEqual(response.status_code,200)
        self.assertIn(b'Apple11',response.content)
        self.assertIn(b'Beijing',response.content)