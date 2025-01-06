from django.contrib import admin
from django.urls import path, include
from chatbot.views import chatbot_page

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('chatbot.urls')),  # Include API routes
    path('',chatbot_page, name='home'),
]
