import account.views
from django.shortcuts import render_to_response
import django_filters
from mharirisocial.profiles.models import Article,Employment,Awards,Profile
from .forms import SignupForm
from django.contrib.auth.models import User
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
    #import pdb;pdb.set_trace()
    return render_to_response('profiles/view.html',{"articles": articles,"employment":employment,"awards":awards},RequestContext(request))
def index(request,template):
    articles = Article.objects.all()[: 5]
    journos = Profile.objects.filter(usergroup='journalist')[:5]
    return render_to_response(template,{"articles": articles,"journos":journos},RequestContext(request))
def add_education(request,username):
    user = User.objects.get(username=username)
    return render_to_response('profiles/add_education.html')
