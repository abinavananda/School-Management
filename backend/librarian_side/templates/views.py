from django.views.generic import CreateView, DeleteView, TemplateView, DetailView, UpdateView, ListView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from admin_side .models import *
from admin_side .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
# Create your views here.

@method_decorator(never_cache, name='dispatch')
class LibrarianLoginView(View):
    model = User
    form_class = LoginForm
    template_name = 'librarian_login.html'

    def get(self, request, *args, **kwargs):
        # If the user is already logged in as staff, redirect to the staff panel
        if request.user.is_authenticated and request.user.role == 'Librarian':
            return redirect('librarian_side:librarian_panel')
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            
            # Check if the user exists
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                messages.error(request, 'Username does not exist')
                return render(request, self.template_name, {'form': form})

            # Authenticate the user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.role == 'Librarian':
                    login(request, user)
                    return redirect('librarian_side:librarian_panel')
                else:
                    messages.error(request, 'You are not authorized as a staff member')
            else:
                messages.error(request, 'Incorrect password')
        
        return render(request, self.template_name, {'form': form})
    

@method_decorator(never_cache, name='dispatch')
class LibrarianPanelView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'librarian_panel.html'
    context_object_name = 'students'  

    def get_queryset(self):
        return User.objects.filter(role='Student')
    
# logout staff view.
class LogoutLibrarianView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        messages.success(request, "logged out succesfully")
        return redirect('librarian_side:librarian_login')
    

# list the book history.
class LibrarianBookStatusView(DetailView):
    model = User
    template_name = 'book_status.html'
    context_object_name = 'student'

    def get_object(self):
        # Fetch the student object based on the student_id from the URL
        student_id = self.kwargs.get('student_id')
        print("tttttttttttttttttttt",student_id)
        return get_object_or_404(User, id=student_id)
    
# list the fees record.
class LibrarianFeesStatusView(DetailView):
    model = User
    template_name = 'fee_status.html'
    context_object_name = 'student'

    def get_object(self):
        # Fetch the student object based on the student_id from the URL
        student_id = self.kwargs.get('student_id')
        # Print the current user details
        current_user = self.request.user
        print(f"Current user: {current_user.username}, Role: {current_user.role}")
        return get_object_or_404(User, id=student_id)