from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.test import TestCase
from djangotoolbox.contrib.auth.models import Group, User, GroupList, Permission, PermissionList


class GroupPermissionTest(TestCase):

    backend = 'djangotoolbox.contrib.auth.backends.ModelBackend'

    def setUp(self):
        self.curr_auth = settings.AUTHENTICATION_BACKENDS
        settings.AUTHENTICATION_BACKENDS = (self.backend,)
        User.objects.create_user('test', 'test@example.com', 'test')

    def tearDown(self):
        settings.AUTHENTICATION_BACKENDS = self.curr_auth

    def test_group_perms(self):
        user = User.objects.get(username='test')
        group_list = GroupList.objects.create()
        user.group_list = group_list
        user.save()
        group = Group.objects.create(name='test_group')
        group_list.groups.append(group.id)
        group_list.save()
        content_type=ContentType.objects.get_for_model(Group)
        perm = Permission.objects.create(name='test_group', content_type=content_type, codename='test_group')
        perm_list = PermissionList.objects.create()
        perm_list.permissions.append(perm.id)
        content_type=ContentType.objects.get_for_model(ContentType)
        perm = Permission.objects.create(name='test_group', content_type=content_type, codename='test_group')
        perm_list.permissions.append(perm.id)
        perm_list.save()
        group.permissions = perm_list
        group.save()

        self.assertEqual(user.get_group_permissions(), set([u'contenttypes.test_group', u'auth.test_group']))
