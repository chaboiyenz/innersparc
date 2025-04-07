from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import *

urlpatterns = [
    path('', views.home, name='home'),  
    path('navbar/', views.navbar, name='navbar'), 
    path('signin/', views.signin, name='signin'),  
    path('signout/', views.signout, name='signout'), 
    path('signup/', views.signup, name='signup'),
<<<<<<< HEAD
    path('profile/', views.profile, name='profile'), 
    path('dashboard/', views.dashboard, name='dashboard'),
    path('commission/', views.commission, name='commission'),
    path('approve/', views.approve, name='approve'),
    path('approve-user/<int:profile_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:profile_id>/', reject_user, name='reject_user'), 
    path('sales-report/', views.sales_report_view, name='sales_report'),  # New URL pattern

=======
    path('profile/<int:id>/', views.profile, name='profile'),
    path('dashboard/', dashboard, name='dashboard'),
    path('api/monthly-sales/', monthly_sales_data, name='monthly_sales_data'),
    path('approve/', views.approve, name='approve'), 
    path('approve-user/<int:profile_id>/', approve_user, name='approve_user'),
    path('reject-user/<int:profile_id>/', reject_user, name='reject_user'),
>>>>>>> 8c64c6fb7d8789c872ad0e5d2bf5c041c82a5acf
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)