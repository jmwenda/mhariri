import datetime
from haystack import indexes
from mharirisocial.profiles.models import Profile,Article

class ProfileIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True)
    gender = indexes.CharField(model_attr='gender',faceted=True)
    media = indexes.CharField(model_attr='media',faceted=True)
    username = indexes.CharField(model_attr='user')

    def get_model(self):
        return Profile

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True,use_template=True)
    category = indexes.CharField(model_attr='category')
    sector = indexes.CharField(model_attr='sector')
    mediabrand = indexes.CharField(model_attr='mediabrand')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.all()

