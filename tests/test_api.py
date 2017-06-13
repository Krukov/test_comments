# -*- coding: utf-8 -*-

from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.urls import reverse
from django.utils.dateparse import parse_datetime
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from excomment.models import Comment

User = get_user_model()


class TestCreateUpdateComments(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='123')
        cls.token = Token.objects.create(user=cls.user)
        cls.content_type = ContentType.objects.get_for_model(User)

    def setUp(self):
        self.client.defaults['HTTP_AUTHORIZATION'] = 'Token ' + self.token.key

    def test_simple_create_api(self):
        self.assertEqual(Comment.objects.count(), 0)
        url = reverse('api:comments-list')
        data = {'body': 'test', 'content_type': self.content_type.id, 'object_id': self.user.id}

        with self.assertNumQueries(6):
            res = self.client.post(url, data=data)

        self.assertEqual(res.status_code, 201)
        self.assertEqual(Comment.objects.count(), 1)

        comment = Comment.objects.last()
        self.assertEqual(comment.body, 'test')
        self.assertEqual(comment.author_id, self.user.id)
        self.assertEqual(comment.content_object, self.user)
        self.assertEqual(comment.parent, None)

    def test_children_create(self):
        self.assertEqual(Comment.objects.count(), 0)
        url = reverse('api:comments-list')

        parent = Comment.objects.create(body='test', author=self.user, content_object=self.user)

        count = 2
        for i in range(100):
            data = {'body': 'test_parent_{}'.format(i), 'content_type': self.content_type.id, 'object_id': self.user.id,
                    'parent': parent.id}
            with self.assertNumQueries(7):
                res = self.client.post(url, data)
            self.assertEqual(res.status_code, 201)

            self.assertEqual(Comment.objects.count(), count)
            comment = Comment.objects.last()
            self.assertEqual(comment.body, 'test_parent_{}'.format(i))
            self.assertEqual(comment.author_id, self.user.id)
            self.assertEqual(comment.content_object, self.user)
            self.assertEqual(comment.parent.id, parent.id)

            count += 1
            parent = comment

    def test_invalid_parent_on_create(self):
        self.assertEqual(Comment.objects.count(), 0)
        url = reverse('api:comments-list')

        data = {'body': 'test_parent', 'content_type': self.content_type.id, 'object_id': self.user.id, 'parent': 10}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue('parent' in res.data)

    def test_invalid_data_on_create(self):
        self.assertEqual(Comment.objects.count(), 0)
        url = reverse('api:comments-list')

        data = {'bodi': 'test_parent'}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 400)
        self.assertTrue('body' in res.data)
        self.assertTrue('content_type' in res.data)
        self.assertTrue('object_id' in res.data)

    def test_readonly_on_create(self):
        self.assertEqual(Comment.objects.count(), 0)
        url = reverse('api:comments-list')

        data = {'body': 'test_parent', 'content_type': self.content_type.id, 'object_id': self.user.id, 'author': 10}
        res = self.client.post(url, data)

        self.assertEqual(res.status_code, 201)
        comment = Comment.objects.last()
        self.assertEqual(comment.author_id, self.user.id)

    def test_edit_comment(self):
        comment = Comment.objects.create(body='test', author=self.user, content_object=self.user)
        url = reverse('api:comments-detail', args=[comment.id])
        data = {'body': 'new'}
        res = self.client.patch(url, data)

        self.assertEqual(res.status_code, 200)
        comment = Comment.objects.get(pk=comment.pk)
        self.assertEqual(comment.body, 'new')

    def test_401_edit_comment(self):
        comment = Comment.objects.create(body='test', author=self.user, content_object=self.user)
        url = reverse('api:comments-detail', args=[comment.id])
        data = {'body': 'new'}
        res = self.client.patch(url, data, HTTP_AUTHORIZATION='')

        self.assertEqual(res.status_code, 401)
        comment = Comment.objects.get(pk=comment.pk)
        self.assertEqual(comment.body, 'test')

    def test_delete_comment(self):
        comment = Comment.objects.create(body='test', author=self.user, content_object=self.user)
        url = reverse('api:comments-detail', args=[comment.id])
        res = self.client.delete(url)

        self.assertEqual(res.status_code, 204)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())

    def test_delete_comment_with_children(self):
        comment = Comment.objects.create(body='test', author=self.user, content_object=self.user)
        children = Comment.objects.create(body='test2', author=self.user, content_object=self.user, parent=comment)

        res = self.client.delete(reverse('api:comments-detail', args=[comment.id]))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.json(), {'errors': ['Comment has children', ]})
        self.assertTrue(Comment.objects.filter(pk=comment.pk).exists())

        res = self.client.delete(reverse('api:comments-detail', args=[children.id]))
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Comment.objects.filter(pk=children.pk).exists())

        res = self.client.delete(reverse('api:comments-detail', args=[comment.id]))
        self.assertEqual(res.status_code, 204)
        self.assertFalse(Comment.objects.filter(pk=comment.pk).exists())


class TestGettingComments(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='test', password='123')
        cls.user2 = User.objects.create_user(username='test2', password='123')
        cls.content_type = ContentType.objects.get_for_model(User)

    def setUp(self):
        for i in range(90):
            c = Comment.objects.create(body='test_{}'.format(i), author=self.user2 if i % 2 else self.user,
                                       content_object=self.user)

            for ii in range(5):
                cc = Comment.objects.create(body='ctest_{}_{}'.format(i, ii), author=self.user2 if i % 2 else self.user,
                                            content_object=self.user, parent=c)
                Comment.objects.create(body='cctest_{}_{}'.format(i, ii), author=self.user2 if i % 2 else self.user,
                                       content_object=self.user, parent=cc)

        for i in range(2):
            Comment.objects.create(body='test_comment_{}'.format(i), author=self.user, content_object=c)

    def test_get_root(self):
        url = reverse('api:comments-list')

        with self.assertNumQueries(3):
            res = self.client.get(url, {'content_type': self.content_type.id, 'object_id': self.user.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']), 20)
        self.assertEqual(res.data['results'][0]['body'], 'test_0')
        self.assertEqual(res.data['results'][0]['author'], self.user.id)
        self.assertEqual(res.data['results'][0]['parent'], None)

        with self.assertNumQueries(3):
            res = self.client.get(url, {'content_type': self.content_type.id, 'object_id': self.user.id, 'page': 5})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data['results']), 10)
        self.assertEqual(res.data['results'][-1]['body'], 'test_89')
        self.assertEqual(res.data['results'][0]['author'], self.user.id)
        self.assertEqual(res.data['results'][0]['parent'], None)

    def test_get_children_for_ct(self):
        url = reverse('api:comment_children')
        with self.assertNumQueries(2):
            res = self.client.get(url, {'content_type': self.content_type.id, 'object_id': self.user.id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 90 + 90 * 10)

    def test_get_children_for_cc(self):
        url = reverse('api:comment_children')
        c_id = Comment.objects.filter(body='ctest_10_2').first().id
        with self.assertNumQueries(2):
            res = self.client.get(url, {'id': c_id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 1)

        c_id = Comment.objects.filter(body='test_10').first().id
        with self.assertNumQueries(2):
            res = self.client.get(url, {'id': c_id})

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 5 + 5)

    def test_get_user_history(self):
        url = reverse('api:comment_author', kwargs={'author': self.user2.id})
        with self.assertNumQueries(1):
            res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(len(res.data), 495)
        self.assertListEqual(
            sorted((i for i in res.data), key=lambda i: parse_datetime(i['created'])),
            res.data
        )
        self.assertEqual(len(set((i['author'] for i in res.data))), 1)

