import pytest
from .factories import NewsTagFactory, NewsArticleFactory
from ..core.factories import OrganisationFactory, UserFactory, OrganisationEmailFactory
from django.test import TestCase
from pgweb.news.models import NewsTag, NewsArticle
import datetime


@pytest.mark.django_db
class TestNewsTagModel(TestCase):
    def setUp(self):
        self.news_tag_1 = NewsTagFactory(urlname='testnews1', name='test news 1')

    def test_instance_of_model(self):
        self.assertIsInstance(self.news_tag_1, NewsTag)

    def test_display_name(self):
        self.assertEquals(str(self.news_tag_1), 'test news 1')


@pytest.mark.django_db
class TestNewsArticleModel(TestCase):
    def setUp(self):
        self.curr_time = datetime.datetime.now()
        self.manager_of_org = UserFactory()
        self.not_manager = UserFactory()
        self.organisation_1 = OrganisationFactory(managers=[self.manager_of_org])
        self.organisation_1_email = OrganisationEmailFactory(org=self.organisation_1)
        self.tag1 = NewsTagFactory(urlname="testarticle1", name="test article 1")
        self.tag2 = NewsTagFactory(urlname="testarticle2", name="test article 2")
        self.news_article_1 = NewsArticleFactory(org=self.organisation_1, email=self.organisation_1_email, date=self.curr_time, title="PostgreSQL test news", tags=[self.tag1, self.tag2])

    def test_instance_of_model(self):
        self.assertIsInstance(self.news_article_1, NewsArticle)

    def test_display_name(self):
        self.assertEquals(str(self.news_article_1), str(self.curr_time) + ': PostgreSQL test news')

    def test_permanent_url(self):
        self.assertEquals(self.news_article_1.permanenturl, '/about/news/postgresql-test-news-%s/' % self.news_article_1.id)

    def test_verify_submitter_method(self):
        self.assertTrue(self.news_article_1.verify_submitter(self.manager_of_org))
        self.assertFalse(self.news_article_1.verify_submitter(self.not_manager))

    def test_taglist_property(self):
        self.assertEquals(self.news_article_1.taglist, 'test article 1, test article 2')
