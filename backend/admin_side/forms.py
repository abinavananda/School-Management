# forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class StudentForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'dob', 'student_class', 'role']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'student_class': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter class'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }
        
        labels = {
            'user': 'Student',
        }

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['role'].initial = 'student'
        self.fields['role'].disabled = True  # Since we are only adding students

        # Remove help text from the username field
        self.fields['username'].help_text = None


class BookRecordForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['user', 'title', 'book_status', 'borrow_date', 'return_date']
        widgets = {
            'user': forms.Select(attrs={'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter book title'}),
            'book_status': forms.Select(attrs={'class': 'form-control'}),
            'borrow_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'return_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

        labels = {
            'user': 'Student',
        }

    def __init__(self, *args, user_id=None, **kwargs):
        super(BookRecordForm, self).__init__(*args, **kwargs)
        if user_id:
            # Filter the user field to only show the user with the given user_id
            self.fields['user'].queryset = User.objects.filter(id=user_id)

        # Customize form field labels and placeholders for better UX
        self.fields['title'].label = "Book Title"
        self.fields['book_status'].label = "Status"
        self.fields['borrow_date'].label = "Borrow Date"
        self.fields['return_date'].label = "Return Date"
        self.fields['title'].widget.attrs.update({'placeholder': 'Enter the title of the book'})



class FeesRecordForm(forms.ModelForm):
    class Meta:
        model = Fees  # Correctly reference the model
        fields = ['user', 'payment_amount', 'due_amount', 'paid_date', 'payment_method', 'fees_status']
        widgets = {
            'paid_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'payment_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter payment amount'}),
            'due_amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter due amount'}),
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'fees_status': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'user': 'Student',
            'payment_amount': 'Payment Amount',
            'due_amount': 'Due Amount',
            'paid_date': 'Date of Payment',
            'payment_method': 'Payment Method',
            'fees_status': 'Fees Status',
        }

    def __init__(self, *args, **kwargs):
        user_id = kwargs.pop('user_id', None)  # Pop user_id from kwargs
        super(FeesRecordForm, self).__init__(*args, **kwargs)
        if user_id:
            # Filter the user field to only show the user with the given user_id
            self.fields['user'].queryset = User.objects.filter(id=user_id)

        # Additional styling can be applied here if necessary
        self.fields['user'].widget.attrs.update({'class': 'form-control'})


class StaffAndLibrarianCreationForm(UserCreationForm): 
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'dob', 'password1', 'password2']

        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }

    # Applying custom widgets and placeholders for styling
    def __init__(self, *args, **kwargs):
        super(StaffAndLibrarianCreationForm, self).__init__(*args, **kwargs)
        
        # Adding Bootstrap classes and placeholders
        self.fields['username'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Username'
        })
        self.fields['name'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Full Name'
        })
        self.fields['email'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Email'
        }) 
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control', 
            'placeholder': 'Confirm Password'
        })

    
        self.fields['username'].help_text = None
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None


class StaffAndLibrarianUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'name', 'email', 'dob', 'role']

        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter full name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
            'dob': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'role': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
        }

    def __init__(self, *args, **kwargs):
        super(StaffAndLibrarianUpdateForm, self).__init__(*args, **kwargs)

        # Remove help text from the username field
        self.fields['username'].help_text = None

    