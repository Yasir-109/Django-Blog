from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from .forms import SignUpForm, EditProfileForm, ProfilePageForm
from django.views.generic import DetailView, CreateView
from theblog.models import Profile
from django.contrib import messages
from allauth.socialaccount.models import SocialAccount
# Create your views here.

class UserRegisterView(generic.CreateView):
    form_class = SignUpForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = EditProfileForm
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')

def password_success(request):
    return render(request, 'registration/password_success.html', {})


class ShowProfilePageView(DetailView):
    model = Profile
    template_name = 'registration/user_profile.html'

    def get_context_data(self, *args, **kwargs):
        users = Profile.objects.all()
        context = super(ShowProfilePageView, self).get_context_data(*args, **kwargs)
        page_user = get_object_or_404(Profile, id = self.kwargs['pk'])
        context["page_user"] = page_user
        return context
    
class EditProfilePageView(generic.UpdateView):
    model = Profile
    form_class = ProfilePageForm
    template_name = 'registration/edit_profile_page.html'
    #fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'github_url']
    success_url = reverse_lazy('home')

class CreateProfilePageView(CreateView):
    model= Profile
    form_class = ProfilePageForm
    template_name = 'registration/create_user_profile_page.html'
    #fields = ['bio', 'profile_pic', 'website_url', 'facebook_url', 'twitter_url', 'instagram_url', 'github_url']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
    
def signup_redirect(request):
    messages.error(request, "Something wrong here, it may be that you already have an account!")
    return redirect('home')

def deactivate_google_account(request):
    if request.user.is_authenticated:
        google_social_account = SocialAccount.objects.filter(user=request.user, provider='google').first()

        if google_social_account:
            google_social_account.delete()
            messages.success(request, "Your Google account has been disconnected successfully!")


        else:
            messages.error(request, "You do not have a Google account connected to your account!")

    else:
        messages.error(request, "You must be logged in to disconnect your Google account!")

    return redirect('home')