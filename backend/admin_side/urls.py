from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'admin_side'
urlpatterns = [
    path('', AdminPanelView.as_view(), name='admin_panel'),

    path('admin_login', AdminLoginView.as_view(), name='admin_login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('add_student/', StudentCreateView.as_view(), name='add_student'),
    path('delete_student/<int:pk>/', StudentDeleteView.as_view(), name='delete_student'), 
    path('edit_student/<int:pk>/', StudentUpdateView.as_view(), name='edit_student'),  

    path('book_status/<int:student_id>/', BookStatusView.as_view(), name='book_status'),
    path('add_book_record/<int:user_id>/', BookRecordCreateView.as_view(), name='add_book_record'),
    path('delete-book/<int:pk>/', BookDeleteView.as_view(), name='delete_book'),  
    path('edit-book/<int:pk>/', BookUpdateView.as_view(), name='edit_book'),  

    path('fees_status/<int:student_id>/', FeesStatusView.as_view(), name='fees_status'),    
    path('add_fees_record/<int:user_id>/', FeesRecordCreateView.as_view(), name='add_fees_record'),    
    path('delete-fees/<int:pk>/', FeesDeleteView.as_view(), name='delete_fees'),    
    path('edit-fees/<int:pk>/', FeesUpdateView.as_view(), name='edit_fees'),    

    path('staff-status/', StaffListView.as_view(), name='staff_status'),    
    path('staff-create/', CreateStaffUserView.as_view(), name='create_staff'),
    path('edit_staff/<int:pk>/', StaffUpdateView.as_view(), name='edit_staff'),
    path('delete-staff/<int:pk>/', StaffDeleteView.as_view(), name='delete_staff'),

    path('librarian-status/', LibrarianListView.as_view(), name='librarian_status'),    
    path('librarian-create/', CreateLibrarianUserView.as_view(), name='create_librarian'),
    path('edit_librarian/<int:pk>/', LibrarianUpdateView.as_view(), name='edit_librarian'),
    path('delete-librarian/<int:pk>/', LibrarianDeleteView.as_view(), name='delete_librarian'),



]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)