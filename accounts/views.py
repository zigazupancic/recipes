from django.shortcuts import HttpResponseRedirect, render
from accounts.forms import UserCreationForm
from django.core.urlresolvers import reverse

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return render(request, 'accounts/register.html', {'form': UserCreationForm(), 'error': 'Napaka, poskusite znova.'})
    return render(request, 'accounts/register.html', {'form': UserCreationForm()})
