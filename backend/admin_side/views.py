from django.views.generic import CreateView, DeleteView, TemplateView, DetailView, UpdateView,ListView
from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
from .models import *
from .forms import *
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.contrib.messages.views import SuccessMessageMixin
from django.http import Http404


# Create your views here.


# admin login.
@method_decorator(never_cache, name='dispatch')
class AdminLoginView(View):
    form_class = LoginForm
    template_name = 'admin_login.html'

    def get(self, request, *args, **kwargs):
        # If the user is already logged in as admin, redirect to the admin panel
        if request.user.is_authenticated and request.user.role == 'admin':
            return redirect('admin_side:admin_panel')
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
                # Check if the user is an admin
                if user.role == 'admin' and user.is_superuser:
                    login(request, user)
                    return redirect('admin_side:admin_panel')
                else:
                    messages.error(request, 'You are not authorized as an admin')
            else:
                messages.error(request, 'Incorrect password')
        
        return render(request, self.template_name, {'form': form})
    

# logout view.
class LogoutView(View):
    def get(self, request):
        logout(request)
        request.session.flush()
        messages.success(request, "logged out succesfully")
        return redirect('admin_side:admin_login')


# admin panel.
@method_decorator(never_cache, name='dispatch')
class AdminPanelView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'student/admin_panel.html'
    context_object_name = 'students'  

    def get_queryset(self):
        return User.objects.filter(role='student')
    

# edit the student details.
class StudentUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = StudentForm
    template_name = 'student/edit_student.html'
    success_message = "Student updated successfully!"

    def get_success_url(self):
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:admin_panel')
        elif self.request.user.role == 'Staff':
            return reverse_lazy('staff_side:staff_panel')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user  
        return context
    

# delete the student.
class StudentDeleteView(LoginRequiredMixin, DeleteView):
    model = User

    def get_success_url(self):
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:admin_panel')
        elif self.request.user.role == 'Staff':
            return reverse_lazy('staff_side:staff_panel')
    

# create new student.
class StudentCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = StudentForm
    template_name = 'student/add_student.html'
    success_message = "Student added successfully!"

    def get_success_url(self):
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:admin_panel')
        elif self.request.user.role == 'Staff':
            return reverse_lazy('staff_side:staff_panel')


# list the book history.
class BookStatusView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'library_history/book_status.html'
    context_object_name = 'student'

    def get_object(self):
        # Fetch the student object based on the student_id from the URL
        student_id = self.kwargs.get('student_id')
        print("tttttttttttttttttttt",student_id)
        return get_object_or_404(User, id=student_id)
    
    
# create the book record.
class BookRecordCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Books
    form_class = BookRecordForm
    template_name = 'library_history/add_book_record.html'
    success_message = "Book record added successfully!"

    def get_form_kwargs(self):
        # Pass the specific user_id to the form
        kwargs = super(BookRecordCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.kwargs.get('user_id')  # Get the user_id from the URL
        return kwargs

    def get_success_url(self):
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:book_status', kwargs={'student_id': self.kwargs.get('user_id')})
        elif self.request.user.role == 'Librarian':
            return reverse_lazy('librarian_side:librarian_book_status', kwargs={'student_id': self.kwargs.get('user_id')})
        

# delete the book record.
class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Books

    def get_success_url(self):
        # Get the user associated with the book record
        student_id = self.get_object().user.id
        
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:book_status', kwargs={'student_id': student_id})
        elif self.request.user.role == 'Librarian':
            return reverse_lazy('librarian_side:librarian_book_status', kwargs={'student_id': student_id})
        

# edit the book record.
class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Books
    form_class = BookRecordForm
    template_name = 'library_history/edit_book_record.html'
    
    def get_success_url(self):
        # Ensure the book object has a user associated with it
        if self.object.user:  
            student_id = self.object.user.id  
            if self.request.user.role == 'admin':
                return reverse_lazy('admin_side:book_status', kwargs={'student_id': student_id})
            elif self.request.user.role == 'Librarian':
                return reverse_lazy('librarian_side:librarian_book_status', kwargs={'student_id': student_id})
        else:
            # Handle the case where there is no user associated with the book
            return reverse_lazy('some_default_view')  # Replace with a default view if necessary

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.object.user.id  # Pass the user ID for filtering
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object.user  # Ensure you use the correct relation
        return context
    

# list the fees record.
class FeesStatusView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'fee_history/fee_status.html'
    context_object_name = 'student'

    def get_object(self):
        # Fetch the student object based on the student_id from the URL
        student_id = self.kwargs.get('student_id')
        return get_object_or_404(User, id=student_id)
    

# create fees record.
class FeesRecordCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Fees
    form_class = FeesRecordForm
    template_name = 'fee_history/add_fee_record.html'
    success_message = "Fees record added successfully!"

    def get_form_kwargs(self):
        # Pass the specific user_id to the form
        kwargs = super(FeesRecordCreateView, self).get_form_kwargs()
        kwargs['user_id'] = self.kwargs.get('user_id')  # Get the user_id from the URL
        return kwargs

    def get_success_url(self):
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:fees_status', kwargs={'student_id': self.kwargs.get('user_id')})
        elif self.request.user.role == 'Staff':
            return reverse_lazy('staff_side:staff_fees_status', kwargs={'student_id': self.kwargs.get('user_id')})
    

# delete the fees record.
class FeesDeleteView(LoginRequiredMixin, DeleteView):
    model = Fees

    def get_success_url(self):
        # Get the user associated with the book record
        student_id = self.get_object().user.id
        
        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:fees_status', kwargs={'student_id': student_id})
        elif self.request.user.role == 'Staff':
            return reverse_lazy('staff_side:staff_fees_status', kwargs={'student_id': student_id}) 
    

# edit the fees record.
class FeesUpdateView(LoginRequiredMixin, UpdateView):
    model = Fees
    form_class = FeesRecordForm
    template_name = 'fee_history/edit_fee.html'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user_id'] = self.object.user.id  # Pass the user ID for filtering
        return kwargs

    def get_success_url(self):
        # Ensure the object and user are valid
        user = getattr(self.object, 'user', None)
        student_id = user.id if user else None  # Get student ID or None

        # Check the user's role to determine the redirect URL
        if self.request.user.role == 'admin':
            return reverse_lazy('admin_side:fees_status', kwargs={'student_id': student_id})
        elif self.request.user.role == 'Staff':
            return reverse_lazy('staff_side:staff_fees_status', kwargs={'student_id': student_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['student'] = self.object.user  # Ensure you use the correct relation
        return context
    

# list the staff users.
class StaffListView(LoginRequiredMixin, ListView):
    template_name = 'staff/staff_list.html'
    context_object_name = 'staff_members'

    # Assuming 'role' is the field on the User model for roles
    def get_queryset(self):
        return User.objects.filter(role='Staff')


# create staff user.
class CreateStaffUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = StaffAndLibrarianCreationForm
    template_name = 'staff/create_staff.html'
    success_url = reverse_lazy('admin_side:staff_status')  

    def form_valid(self, form):
        # Assign the staff role
        user = form.save(commit=False)
        user.role = 'Staff'  
        user.save()
        return super().form_valid(form)

    # Only allow superusers to access this view
    def test_func(self):
        return self.request.user.is_superuser
    

# edit the staff user.
class StaffUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'staff/edit_staff.html'
    form_class = StaffAndLibrarianUpdateForm
    success_url = reverse_lazy('admin_side:staff_status')  

    def get_queryset(self):
        return super().get_queryset().filter(role='Staff')  

    def test_func(self):
        return self.request.user.is_superuser
    

# delete the staff user.
class StaffDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('admin_side:staff_status')  

    def get_queryset(self):
        return User.objects.filter(role='Staff') 


# list the librarian users.
class LibrarianListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    template_name = 'librarian/librarian_list.html'
    context_object_name = 'librarian_members'

    # Assuming 'role' is the field on the User model for roles
    def get_queryset(self):
        return User.objects.filter(role='Librarian')


# create librarian user.
class CreateLibrarianUserView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = User
    form_class = StaffAndLibrarianCreationForm
    template_name = 'librarian/create_librarian.html'
    success_url = reverse_lazy('admin_side:librarian_status')  

    def form_valid(self, form):
        # Assign the staff role
        user = form.save(commit=False)
        user.role = 'Librarian'  
        user.save()
        return super().form_valid(form)

    # Only allow superusers to access this view
    def test_func(self):
        return self.request.user.is_superuser
    

# edit the librarian user.
class LibrarianUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'librarian/edit_librarian.html'
    form_class = StaffAndLibrarianUpdateForm
    success_url = reverse_lazy('admin_side:librarian_status')  

    def get_queryset(self):
        return super().get_queryset().filter(role='Librarian')  
    
    def test_func(self):
        return self.request.user.is_superuser
    

# delete the librarian user.
class LibrarianDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    success_url = reverse_lazy('admin_side:librarian_status')  

    def get_queryset(self):
        return User.objects.filter(role='Librarian') 
    