from django.shortcuts import render
from .forms import UserRegistrationForm
from .models import User
from django.contrib.auth.models import Group
from music_database.models import Release, Artist, Genre


def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            group = Group.objects.get(name='DatabaseBasicUserGroup')
            new_user.groups.add(group)
            return render(request, 'register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'register.html', {'user_form': user_form})


def profile(request):
    user = User.objects.get(username=request.user)
    user_releases = Release.objects.filter(entry_owner=user.id)
    user_artists = Artist.objects.filter(entry_owner=user.id)
    user_genres = Genre.objects.filter(entry_owner=user.id)
    return render(request, 'profile.html', {'user': user, 'user_releases': user_releases, 'user_artists': user_artists,
                                            'user_genres': user_genres})
