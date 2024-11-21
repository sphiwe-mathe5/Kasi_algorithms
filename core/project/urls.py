from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django_otp.admin import OTPAdminSite
from django_otp.plugins.otp_totp.models import TOTPDevice
from django_otp.plugins.otp_totp.admin import TOTPDeviceAdmin
from django.conf import settings
from django.contrib.auth.models import User
from django.conf.urls.static import static
from core.models import Post
from submit.models import Profile
from core.views import index, subscribe, about, enquire,contact, terms, prompt,  optout, PostListView, PostDetailView, PostCreateView,PostUpdateView,PostDeleteView, UserPostListView

class OTPAdmin(OTPAdminSite):
    pass

admin_site = OTPAdmin(name='OTPAdmin')
admin_site.register(User)
admin_site.register(TOTPDevice, TOTPDeviceAdmin)
admin_site.register(Post)
admin_site.register(Profile)


urlpatterns = [
    path('', PostListView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    #path('kasialgo-secure-admin/', admin_site.urls),
    path('post/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('post/new/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('subscribe/', subscribe, name='subscribe'),
    path('about/', about, name='about'),
    path('', include('submit.urls')),
    path('emails/', include('emails.urls')),
    path('enquire/', enquire, name='enquire'),
    path('optout/', optout, name='optout'),
    path('contact/', contact, name='contact'),
    path('terms/', terms, name='terms'),
    path('prompt/', prompt, name='prompt'),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='submit/password_reset.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='submit/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='submit/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='submit/password_reset_complete.html'),name='password_reset_complete'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
