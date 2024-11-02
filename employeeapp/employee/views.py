from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
from .models import *
from django.views.generic import TemplateView,ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.http import JsonResponse


class SignUpView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'signup.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('employee_portal')
        return render(request, 'signup.html', {'form': form})


class CustomLoginView(View):
    def get(self, request):
        form = CustomLoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('employee_portal')
        return render(request, 'login.html', {'form': form})

class EmployeePortalView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'employee':
            return redirect('home')  
        return render(request, 'employee_portal.html', {'user': request.user})


class HomeView(TemplateView):
    template_name = 'home.html'  


class AdminDashboardView(LoginRequiredMixin, View):
    def get(self, request):
        if request.user.role != 'admin':
            return redirect('home')  
        return render(request, 'admin_dashboard.html', {'user': request.user})


class EmployeeListView(ListView):
    model = Employee
    template_name = 'employee_list.html'
    context_object_name = 'employees'

from django.contrib.auth import get_user_model

class EmployeeCreateView(CreateView):
    model = Employee
    form_class = EmployeeForm  
    template_name = 'employee_form.html'
    success_url = reverse_lazy('employee_list')

    def form_valid(self, form):
        user = form.cleaned_data.get('user')
        
        if Employee.objects.filter(user=user).exists():
            form.add_error('user', "This user already has an employee record.")
            return self.form_invalid(form)
        return super().form_valid(form)







class EmployeeUpdateView(UpdateView):
    model = Employee
    template_name = 'employee_form.html'
    fields = ['department', 'hire_date', 'position']
    success_url = reverse_lazy('employee_list')

class EmployeeDeleteView(DeleteView):
    model = Employee
    template_name = 'employee_confirm_delete.html'
    success_url = reverse_lazy('employee_list')

def employee_search(request):
    query = request.GET.get('q')  
    employees = Employee.objects.all()  

    if query:
        employees = employees.filter(user__username__icontains=query)  

    return render(request, 'employee_search.html', {'employees': employees, 'query': query})


