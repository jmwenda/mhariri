from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth.models import User


class Profile(models.Model):
    
    user = models.OneToOneField(User, related_name="profile")
    ACCOUNT_TYPE = ((u'journalist', u'journalist'),(u'Content Provider', u'Content Provider'))
    usergroup = models.CharField(choices=ACCOUNT_TYPE,max_length=20,null=True)
    birthdate = models.DateField(null=True, blank=True)
    def __unicode__(self):
        return u'%s %s' %(self.user.first_name,self.user.last_name)

@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    """
    Create a Profile instance for all newly created User instances. We only
    run on user creation to avoid having to check for existence on each call
    to User.save.
    """
    user, created = kwargs["instance"], kwargs["created"]
    if created:
        Profile.objects.create(user=user)

class Employment(models.Model):
    profile = models.ForeignKey(Profile)
    startdate = models.DateField(null=True,blank=True)
    enddata = models.DateField(null=True,blank=True)
    employer = models.TextField()
class Category(models.Model):
    category = models.CharField("Category",max_length=25)
    def __unicode__(self):
        return self.category
class Sector(models.Model):
    sector = models.CharField("Sector",max_length=25)
    def __unicode__(self):
        return self.sector
class MediaHouse(models.Model):
    media_company = models.CharField("Media Company",max_length=25)
    def __unicode__(self):
        return self.media_company
class MediaBrand(models.Model):
    brand = models.CharField("Brand",max_length=50)
    mediahouse = models.ForeignKey(MediaHouse)
    def __unicode__(self):
        return u'%s - %s' % (self.mediahouse, self.brand)
class Company(models.Model):
    company = models.CharField("Company",max_length=25)
    def __unicode__(self):
        return self.company
class Article(models.Model):
    profile = models.ForeignKey(Profile)
    category = models.ForeignKey(Category)
    published = models.DateField(null=True,blank=True)
    month = models.CharField("Month",max_length=25)
    title = models.CharField("Article Title",max_length=30)
    company = models.ManyToManyField(Company,blank=True)
    mediabrand = models.ForeignKey(MediaBrand)
    article_summary = models.TextField("Article Summary")
    article = models.TextField("Article Full Text")
    article_link = models.URLField("Article URI",blank=True)
    article_pdf = models.FileField("Article PDF",upload_to='resources',blank=True)
    article_page = models.CharField("Article Page",max_length=25,blank=True)
    article_size = models.CharField("Article Size",max_length=25,blank=True)
    TONALITY_TYPE = ((u'POSITIVE', u'POSITIVE'),(u'NEGATIVE', u'NEGATIVE'))
    tonality = models.CharField(choices=TONALITY_TYPE,max_length=20,null=False)
    sector = models.ForeignKey(Sector)
    relevance = models.IntegerField("Relevance",blank=True) 

class Awards(models.Model):
    profile=models.ForeignKey(Profile)
    award = models.TextField()
    year = models.DateField(null=True,blank=True)
