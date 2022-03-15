from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views import View


class LoginView(View):
    template_name = 'accounts/login.html'

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        remember_me = "on" in request.POST.get("remember_me", "")

        user = authenticate(username=username, password=password)

        if user:
            login(request, user)
            if remember_me:
                request.session.set_expiry(86400 * 30)
            user.last_login_date = timezone.now()
            user.save()
            redirect_url = request.GET.get("next") or "dashboard:index"
            return redirect(redirect_url)
        else:
            context = {k: v for k, v in request.POST.items()}
            messages.warning(request, "Invalid credentials")
            return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('accounts:login')
