
from django.contrib import admin
from django.contrib import auth
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls.conf import include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('', include('expenses.urls')),
    path('settings/', include("userpreferences.urls")),
    path('incomes/', include("incomes.urls")),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="authentication/password_reset.html"), name="password_reset"),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(
        template_name="authentication/password_reset_done.html"), name="password_reset_done"),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="authentication/password_reset_confirm.html"), name="password_reset_confirm"),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="authentication/password_reset_complete.html"), name="password_reset_complete")
]+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
