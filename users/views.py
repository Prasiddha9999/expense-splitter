from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView, LoginView
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import logging

# Set up logging
logger = logging.getLogger(__name__)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)


class CustomLoginView(LoginView):
    template_name = 'users/login.html'

    def get_success_url(self):
        # Check if there's a pending group join
        if 'join_group_id' in self.request.session:
            group_id = self.request.session.pop('join_group_id')
            from expenses.models import Group

            # Try to get the group
            try:
                group = Group.objects.get(id=group_id)
                # Add user to the group
                if self.request.user not in group.members.all():
                    group.members.add(self.request.user)
                    messages.success(self.request, f'You have joined {group.name}!')
                return reverse_lazy('group-detail', kwargs={'group_id': group_id})
            except Group.DoesNotExist:
                pass

        # Default redirect to groups page
        return reverse_lazy('groups')


class CustomPasswordResetView(PasswordResetView):
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'registration/password_reset_email.html'
    template_name = 'registration/password_reset_form.html'

    def form_valid(self, form):
        # Log the email being sent
        email = form.cleaned_data['email']
        logger.info(f"Sending password reset email to {email}")
        try:
            return super().form_valid(form)
        except Exception as e:
            # Log the error
            logger.error(f"Failed to send password reset email to {email}")
            logger.exception(e)
            # Add an error message
            messages.error(self.request, "There was an error sending the password reset email. Please try again later.")
            # Return to the form with the error
            return self.form_invalid(form)
