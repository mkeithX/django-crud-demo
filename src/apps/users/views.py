from typing import Any, Dict
from django.shortcuts import render, redirect
from django.views.generic import (
    ListView,
    DetailView,
    DeleteView,
    FormView,
    TemplateView,
    RedirectView
)
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import (
    LoginView,
    PasswordChangeView,
    PasswordResetView,
)
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.users.models import UserProfile
from apps.users.forms import LoginForm, ChangePasswordForm
from django.db.models import Q
from django.urls import reverse_lazy
from apps.users.forms import CustomUserCreationForm
from django.utils.decorators import method_decorator
from django.contrib.auth import get_user_model, login, logout
from django.dispatch import receiver
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.views import View
from django.views.decorators.csrf import csrf_protect
from . import forms
from django.conf import settings

from django.views.decorators.cache import never_cache
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.views.decorators.csrf import csrf_protect
from django.utils.http import url_has_allowed_host_and_scheme

User = get_user_model()


# Signup/Registration View
class Signup(View):
    form_class = CustomUserCreationForm
    initial = {"key": "value"}
    template_name = "auth/signup.html"

    @method_decorator(csrf_protect)
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="/")
        
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()
            first_name = form.cleaned_data.get("first_name")
            messages.success(
                request,
                f"AWESOME! Welcome to this amazing website, {first_name}! \n" \
                " Please login to continue."
            )

            return redirect(to="login")

        return render(request, self.template_name, {"form": form})
    

# Login View
class CustomLoginView(LoginView):
    form_class = LoginForm
    template_name = "auth/login.html"
    success_url = '/'
    redirect_field_name = REDIRECT_FIELD_NAME
    
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        return super(CustomLoginView, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if redirect_to is None:
            redirect_to = '/'
        return super(CustomLoginView, self).get_context_data(**kwargs)

    def form_valid(self, form):
        redirect = super().form_valid(form)
        remember_me = form.cleaned_data.get("remember_me")

        if remember_me is True:
            SESSION_DURATION = 30 * 24 * 60 * 60 # 1 Month
            expiry = getattr(settings, "KEEP_LOGGED_DURATION", SESSION_DURATION)
            self.request.session.set_expiry(expiry)
        
        return redirect
    
    def get_success_url(self):
        redirect_to = self.request.POST.get(self.redirect_field_name)
        if not url_has_allowed_host_and_scheme(
            url=redirect_to, allowed_hosts=[
                self.request.get_host()]):
            redirect_to = self.success_url
            
        return redirect_to


# Logout View

class CustomLogoutView(View):
    @method_decorator(login_required(login_url='login'))
    def dispatch(self,request,*args,**kwargs):
        return super().dispatch(request,*args,**kwargs)

    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('index')

# User lists
@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ProfileListView(ListView):
    paginate_by = 8
    template_name = 'users/user_list.html'
    model = UserProfile
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["profiles"] = self.kwargs
        return context
    
    def get_queryset(self):
        return UserProfile.objects.all().exclude(user__id=self.request.user.id).order_by("-user_id")
    
# Search user
@method_decorator(login_required(login_url="/login/"), name="dispatch")
class SearchView(ListView, LoginRequiredMixin):
    paginate_by = 3
    context_object_name = "search_result"

    def get(self, request, *args, **kwargs):
        q = request.GET.get("q", "")
        search_result = User.objects.filter(
            Q(username__icontains=q)
            | Q(email__icontains=q)
            | Q(first_name__icontains=q)
            | Q(last_name__icontains=q)
        ).distinct()

        context = {"search_result": search_result}

        return render(request, "main/search.html", context=context)


# User-profile details
@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ProfileDetailView(DetailView, LoginRequiredMixin):
    model = UserProfile
    template_name = "users/user_profile_details.html"
    context_object_name = "user_profile"

    def get_queryset(self):
        return UserProfile.objects.all().exclude(user=self.request.user.id)

    def get_object(self, **kwargs):
        pk = self.kwargs.get("pk")
        view_profile = UserProfile.objects.get(pk=pk)
        return view_profile
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = UserProfile.objects.get(user=self.request.user.id)
        context["view_profile"] = view_profile
        context["my_profile"] = my_profile

        return context
    

# Update profile
@method_decorator(login_required(login_url="/login/"), name="dispatch")
class UpdateProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'users/user_update_profile.html'
    http_method_names = ["get", "post"]

    def get(self, request, *args, **kwargs):
        user = self.request.user

        if "u_form" not in kwargs:
            kwargs["u_form"] = forms.UpdateUserForm(instance=user)

        if "p_form" not in kwargs:
            kwargs["p_form"] = forms.UpdateProfileForm(instance=user.user_profile)

        return super().get(request, *args, **kwargs)
    

    def post(self, request, *args, **kwargs):
        user = self.request.user
        u_form = forms.UpdateUserForm(request.POST, instance=user)
        p_form = forms.UpdateProfileForm(request.POST, request.FILES, instance=user.user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f"Awesome {user.first_name}! Your profile has been updated.")
            return redirect("/")
        
        return super().get(request, u_form=u_form, p_form=p_form)
        


# Delete user
@method_decorator(login_required(login_url="login"), name="dispatch")
class DeleteAccountView(DeleteView):
    model = User
    success_url = reverse_lazy("login")
    template_name = "users/user_confirm_delete.html"


class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = "auth/passwords/password_reset.html"
    email_template_name = "auth/passwords/password_reset_email.html"
    subject_template_name = "auth/passwords/password_reset_subject"
    success_message = (
        "We've sent you an email with some steps to reset your password. " \
        "Don't forget to check your SPAM folder too. "
        "Make sure your email address associated to your account is correct."
    )
    success_url = reverse_lazy("login")

@method_decorator(login_required(login_url="/login/"), name="dispatch")
class ChangePasswordView(PasswordChangeView):
    form_class = ChangePasswordForm
    template_name = "auth/passwords/change_password.html"
    success_url = reverse_lazy("logout")

    def form_valid(self, form):
        form.save()
        messages.success(self.request, "SUCCESS! Login at anytime using your new password.")
        return super().form_valid(form)

@method_decorator(login_required(), name="dispatch")
class HomeView(TemplateView):
    template_name = 'main/home.html'

@method_decorator(login_required(), name="dispatch")
class AboutPageView(TemplateView):
    template_name = 'main/about.html'
