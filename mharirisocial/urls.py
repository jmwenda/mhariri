from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.http import HttpResponseRedirect

from django.views.generic.simple import direct_to_template
from django.core.urlresolvers import reverse_lazy
from django.views.generic import ListView,CreateView,DetailView,UpdateView
from django_filters.views import object_filter
from django.contrib import admin
admin.autodiscover()

from .views import SignupView
from mharirisocial.profiles.models import Article,Employment,Awards,Profile,Education
from mharirisocial.forms import SearchForm
from .views import ArticleFilter

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView

sqs = SearchQuerySet().facet('gender')



def is_admin(function):
    def wrapper(request, *args, **kw):
        user=request.user
        if user.is_authenticated():
            if  user.get_profile().usergroup == 'Content Provider' or user.get_profile().usergroup == 'Client' or user.get_profile().usergroup == 'journalist':
                return function(request,*args,**kw)
            else:
                return HttpResponseRedirect('/')
        else:
               return HttpResponseRedirect('/')
    return wrapper


urlpatterns = patterns("",
    url(r"^$", 'mharirisocial.views.index', {"template": "homepage.html"}, name="home"),
    #url(r"^$", direct_to_template, {"template": "homepage.html"}, name="home"),
    url(r"^admin/", include(admin.site.urls)),
    url(r"^account/signup/$", SignupView.as_view(), name="account_signup"),
    url(r"^account/", include("account.urls")),
    #url(r"^content/$",is_admin(ListView.as_view(model=Article)),name="content"),
    url(r"^content/new/",is_admin(CreateView.as_view(model=Article)),name="content-form"),
    url(r'^content/(?P<pk>\d+)/$', is_admin(DetailView.as_view(model=Article)),name="content-info"),
    #url(r"^content/$",is_admin(object_filter),{'model': Article},name="content")
    url(r"^content/$",is_admin(object_filter),{'filter_class':ArticleFilter },name="content"),
    url(r"^profile/$",'mharirisocial.views.profile',name="profile"),
    url(r"^advsearch/$",is_admin(object_filter),{'filter_class':ArticleFilter },name="aggregate"),
    #url(r"^search/$",'mharirisocial.views.search',name="aggregate"),
    #url(r'^search/', include('haystack.urls')),
    url(r"^analytics/$",is_admin('mharirisocial.views.analysis'),name="analytics"),
    url(r"^profile/analysis/(?P<username>\w+)/",'mharirisocial.views.analytics',name="analysis"),
    url(r"^profile/(?P<username>\w+)/education/new/",CreateView.as_view(model=Education),name="education-form"),
    url(r"^profile/(?P<username>\w+)/employment/new/",CreateView.as_view(model=Employment),name="employment-form"),
    url(r"^profile/(?P<username>\w+)/education/",'mharirisocial.views.educationdetail',name="education-detail"),
    url(r"^profile/(?P<username>\w+)/employment/",'mharirisocial.views.employmentdetail',name="employment-detail"),
    url(r"^profile/(?P<username>\w+)/award/new/",CreateView.as_view(model=Awards),name="award-form"),
    url(r"^profile/(?P<username>\w+)/$",'mharirisocial.views.viewprofile',name="viewprofile"),
    url(r"^profile/edit/(?P<pk>\w+)/",UpdateView.as_view(model=Profile,success_url=reverse_lazy('profile')),name="profile-form")
    #url(r"^profile/(?P<username>\w+)/add-education/$",'mharirisocial.views.add_education',name="add-education")
)
urlpatterns += patterns('haystack.views',
    url(r'^search/', is_admin(FacetedSearchView(form_class=FacetedSearchForm, searchqueryset=sqs)), name='haystack_search'),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#import pdb;pdb.set_trace()
