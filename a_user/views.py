from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from a_user.forms import ProfileForm, EmailForm
from django.contrib.auth.models import User
from a_user.models import Profile
from django.contrib.auth import logout


# Create your views here.
def profile_view(request, username=None):
    if username:
        profile = get_object_or_404(User, username=username).profile    
    else:
        try:
            profile = request.user.profile
        except:
            return redirect('accounts_login')       
    return render(request, 'a_user/profile.html', {'profile': profile})   

@login_required
def profile_edit_view(request):
    form = ProfileForm(instance=request.user.profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
    if form.is_valid():
        form.save()
        return redirect('profile')  

    if request.path == reverse('profile_onbording'):
        onboarding = True
    else:
        onboarding = False
            
    return render(request, 'a_user/profile_edit.html', {'form': form , 'onboarding': onboarding}) 

@login_required
def profile_settings_view(request):
    return render(request, 'a_user/profile_settings.html', {}) 

@login_required
def profile_emailchange(request):
    if request.htmx:
        form = EmailForm(instance=request.user)
        return render(request, 'partial/email_form.html', {'form': form}) 

    if request.method == 'POST':
        form = EmailForm(request.POST, instance=request.user)
        if form.is_valid():
            # check if email already exists
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exclude(id=request.user.id).exists():
                messages.warning(request, f'{email} already exists')
                return redirect('profile_settings') 
            form.save()
            # Then signal updates emailaddress and set verified to false

            # Then send confirmation email
            # build later
            return redirect('profile_settings') 
        else:
            messages.warning(request, 'form not valid')
            return redirect('profile_settings') 
    return redirect('home')

@login_required
def profile_delete_view(request):
    user = request.user
    if request.method == 'POST':
        logout(request)
        user.delete()
        return redirect('home')
    return render(request, 'a_user/profile_delete.html', {})