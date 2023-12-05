from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from .forms import CustomUserCreationForm
from .models import Task
from .utils import decode_pickle, create_flag, create_pickle


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def form_valid(self, form):
        response = super(CustomLoginView, self).form_valid(form)
        user_id = str(self.request.user.uuid).replace('-', '')
        b64 = create_pickle(self.request.user.uuid)
        response.set_cookie('user', b64)
        return response

    def get_success_url(self):
        return reverse_lazy('tasks')


class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        response = super(CustomLogoutView, self).get(request, *args, **kwargs)
        response.delete_cookie('user')
        return response

    def get_success_url(self):
        return reverse_lazy('login')


class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = CustomUserCreationForm  # Use the custom form here
    redirect_authenticated_user = True
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
            # remove -
            user_id = str(user.uuid).replace('-', '')
            create_flag(user_id)
            b64 = create_pickle(user_id)
            # set cookie user
            request = super(RegisterPage, self).form_valid(form)
            request.set_cookie('user', b64)
            return request
        else:
            return super(RegisterPage, self).form_invalid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'base/task_list.html'
    context_object_name = 'tasks'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        context['user_name'] = self.request.user.username

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['tasks'] = context['tasks'].filter(title__startswith=search_input)

        context['search_input'] = search_input

        # get cookie user
        user_obj = self.request.COOKIES.get('user')
        if user_obj:
            obj = decode_pickle(user_obj)
            if obj:
                context['user_name'] = obj
        return context


class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'base/task_create.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'base/task_create.html'
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('tasks')


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    template_name = 'base/task_delete.html'
    context_object_name = 'task'
    success_url = reverse_lazy('tasks')
