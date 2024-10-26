from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'staff_side'
urlpatterns = [
    path('staff-login/', StaffLoginView.as_view(), name='staff_login'),  
    path('staff_panel/', StaffPanelView.as_view(), name='staff_panel'),

    path('staff_logout/', LogoutStaffView.as_view(), name='staff_logout'),

    path('staff-book-status/<int:student_id>/', StaffBookStatusView.as_view(), name='staff_book_status'),
    path('staff-fees-status/<int:student_id>/', StaffFeesStatusView.as_view(), name='staff_fees_status'),    
   

  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)