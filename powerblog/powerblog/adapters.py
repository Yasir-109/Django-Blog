from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from theblog.models import Profile  # Import your Profile model
from django.urls import reverse

class CustomSocialAccountAdapter(DefaultSocialAccountAdapter):
    def save_user(self, request, sociallogin, form=None):
        user = super().save_user(request, sociallogin, form=form)

        if sociallogin.account.provider == 'google':
            extra_data = sociallogin.account.extra_data
            email = extra_data.get('email')
            profile_pic = extra_data.get('picture')

            if email:
                user.email = email
                user.save()

            if profile_pic:
                profile, created = Profile.objects.get_or_create(user=user)
                profile.profile_pic = profile_pic
                profile.save()

        return user
    
    def get_connect_redirect_url(self, request, socialaccount):
        return reverse('home')