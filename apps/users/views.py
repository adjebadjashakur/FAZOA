from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import User
from .forms import LoginForm, UserCreationFormCustom, UserChangeFormCustom
from .mixins import AdminRequiredMixin, AllStaffMixin


class LoginView(View):
    template_name = 'users/login.html'

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('dashboard:dashboard')
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue, {user.get_full_name() or user.username}!')
                return redirect('dashboard:dashboard')
            else:
                messages.error(request, 'Identifiant ou mot de passe incorrect.')
        return render(request, self.template_name, {'form': form})


class LogoutView(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        messages.info(request, 'Vous avez été déconnecté.')
        return redirect('users:login')

    def get(self, request):
        # Allow logout via GET for convenience
        logout(request)
        messages.info(request, 'Vous avez été déconnecté.')
        return redirect('users:login')


class UserListView(AdminRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'
    paginate_by = 15

    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search'] = self.request.GET.get('search', '')
        return context


class UserCreateView(AdminRequiredMixin, CreateView):
    model = User
    form_class = UserCreationFormCustom
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Utilisateur créé avec succès.')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Veuillez corriger les erreurs ci-dessous.')
        return super().form_invalid(form)


class UserUpdateView(AdminRequiredMixin, UpdateView):
    model = User
    form_class = UserChangeFormCustom
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('users:user_list')

    def form_valid(self, form):
        messages.success(self.request, 'Utilisateur modifié avec succès.')
        return super().form_valid(form)


class UserDeleteView(AdminRequiredMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('users:user_list')

    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Utilisateur supprimé.')
        return super().delete(request, *args, **kwargs)


def custom_403(request, exception=None):
    return render(request, '403.html', status=403)


def custom_404(request, exception=None):
    return render(request, '404.html', status=404)
