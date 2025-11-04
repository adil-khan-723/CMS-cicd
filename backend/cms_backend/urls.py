from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    # ✅ Admin Panel
    path('admin/', admin.site.urls),

    # ✅ Blog API routes
    path('api/', include('blog.urls')),

    # ✅ Custom authentication routes
    path('api/auth/', include('auth_app.urls')),
    path('api/auth/token/', obtain_auth_token, name='api_token_auth'),  # Login endpoint

    # ✅ `dj-rest-auth` authentication routes (for built-in login/logout/registration)
    path('api/dj-rest-auth/', include('dj_rest_auth.urls')),  
    path('api/dj-rest-auth/registration/', include('dj_rest_auth.registration.urls')),
]

# ✅ Serve media files in development mode
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
                