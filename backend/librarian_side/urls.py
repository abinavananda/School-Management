from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static


app_name = 'librarian_side'
urlpatterns = [
    path('librarian-login/', LibrarianLoginView.as_view(), name='librarian_login'),  
    path('librarian_panel/', LibrarianPanelView.as_view(), name='librarian_panel'),

    path('librarian_logout/', LogoutLibrarianView.as_view(), name='librarian_logout'),

    path('librarian-book-status/<int:student_id>/', LibrarianBookStatusView.as_view(), name='librarian_book_status'),
    path('librarian-fees-status/<int:student_id>/', LibrarianFeesStatusView.as_view(), name='librarian_fees_status'),    

       
  

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)