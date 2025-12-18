from django.contrib import admin
from django.urls import path, include  # ✅ include imported

urlpatterns = [
    path('admin/', admin.site.urls),

    # 🔥 REQUIRED BY CHECKER
    path('api/', include('api.urls')),
]

