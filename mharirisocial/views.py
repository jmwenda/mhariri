import account.views
from django.shortcuts import render_to_response
import django_filters
from mharirisocial.profiles.models import Article,Employment,Awards,Profile,Company,Sector
from .forms import SignupForm
from django.contrib.auth.models import User
from django.db.models import Count
from django.template import Context,RequestContext



class SignupView(account.views.SignupView):
    
    form_class = SignupForm
    
    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)
    #@overide
    def create_user(self, form, commit=True, **kwargs):
        user = User(**kwargs)
        username = form.cleaned_data.get("username")
        first_name = form.cleaned_data.get("first_name")
        last_name = form.cleaned_data.get("last_name")
        if username is None:
            username = self.generate_username(form)
        user.username = username
        user.email = form.cleaned_data["email"].strip()
        user.first_name = first_name
        user.last_name = last_name
        password = form.cleaned_data.get("password")
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        if commit:
            user.save()
        return user
 
    def create_profile(self, form):
        profile = self.created_user.profile
        profile.birthdate = form.cleaned_data["birthdate"]
        profile.usergroup = 'journalist'
        profile.save()

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['category','profile','sector','company','mediabrand']
def profile(request):
    user = request.user
    profile = user.profile
    articles = Article.objects.filter(profile=profile)[:10]
    employment = Employment.objects.filter(profile=profile)
    awards = Awards.objects.filter(profile=profile)
    article_comp = Company.objects.filter(article__profile=profile).annotate(num_comp = Count('article'))
    sector_comp = Sector.objects.filter(article__profile=profile).annotate(num_sector = Count('article'))
    #import pdb;pdb.set_trace() 
    return render_to_response('profiles/view.html',{"articles": articles,"employment":employment,"awards":awards,"mentions":article_comp,"sectors":sector_comp},RequestContext(request))
def analytics(request,username):
    user = request.user
    profile = user.profile
    article_comp = Company.objects.filter(article__profile=profile).annotate(num_comp = Count('article'))
    sector_comp = Sector.objects.filter(article__profile=profile).annotate(num_sector = Count('article'))
    companychart = Company.gcharts.filter(article__profile=profile).values("company").annotate(num_comp = Count('article')).order_by()
    companychartjson = companychart.to_json(labels={"num_comp": "Mentions"})
    sectorchart = Sector.gcharts.filter(article__profile=profile).values("sector").annotate(num_sector = Count('article')).order_by()
    sectorchartjson = sectorchart.to_json(labels={"num_sector": "Sectors"},order=("sector","num_sector"))
    sentimentchart = Article.gcharts.filter(profile=profile).values("tonality").annotate(num_tone = Count('article')).order_by()
    sentimentchartjson = sentimentchart.to_json(labels={"num_tone": "Tonality"},order=("tonality","num_tone"))
    #import pdb;pdb.set_trace() 
    return render_to_response('profiles/chartview.html',{"mentions":article_comp,"sectors":sector_comp,"spam_data":companychartjson,"sector_data":sectorchartjson,"tone_data":sentimentchartjson},RequestContext(request))

def index(request,template):
    articles = Article.objects.all()[: 5]
    journos = Profile.objects.filter(usergroup='journalist')[:5]
    user = request.user
    profile = user.profile
    myarticles = Article.objects.filter(company=profile.company)[:25]
    return render_to_response(template,{"articles": articles,"journos":journos},RequestContext(request))
def add_education(request,username):
    user = User.objects.get(username=username)
    return render_to_response('profiles/add_education.html')
