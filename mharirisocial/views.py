import account.views
import django_filters
from mharirisocial.profiles.models import Article
from .forms import SignupForm


class SignupView(account.views.SignupView):
    
    form_class = SignupForm
    
    def after_signup(self, form):
        self.create_profile(form)
        super(SignupView, self).after_signup(form)
    
    def create_profile(self, form):
        profile = self.created_user.profile
        profile.birthdate = form.cleaned_data["birthdate"]
        profile.save()

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = ['category','profile','sector','company','mediabrand']

