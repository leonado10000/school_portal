"""
URL configuration for school_portal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from pyexpat.errors import messages
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static
from django.conf import settings
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from utils.bronzelogger import bronzelogger

def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # logs the user in
            return redirect('index')  # replace with your post-login page
        else:
            messages.error(request, "Invalid ID or Password")
    return render(request, 'pages/login.html')

def logout_page(request):
    logout(request)  # logs out the user
    return redirect('login') 

@login_required(login_url='/login')
@bronzelogger
def home_page(request):
    return render(request, 'common/index.html')

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', home_page, name='index'),
    path('notebook/', include('notebooks.urls')),
    path('marksheet/', include('marksheet.urls')),
    path('people/', include('people.urls')),
    path('reports/', include('reports.urls')),
    path('term_of_use/', lambda request: render(request, 'common/term_of_use.html'), name='term_of_use'),
    path('privacy_policy/', lambda request: render(request, 'common/privacy_policy.html'), name='privacy_policy'),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout')
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
