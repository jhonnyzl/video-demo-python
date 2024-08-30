from django.contrib import admin
from django.urls import path, include
from emailManager.views import send_email, ejecutar_crear_conversacion, ejecutar_end_conversation

urlpatterns = [
    path('admin/', admin.site.urls),
    path('company/', include('company.urls')),
    path('users/', include('users.urls')),
    path('tasks/', include('tasks.urls')),
    path('send-email/', send_email, name='send_email'),
    path('ejecutar-crear-conversacion/', ejecutar_crear_conversacion, name='ejecutar_crear_conversacion'),
    path('ejecutar_end_conversation/<str:conversation_id>/', ejecutar_end_conversation, name='ejecutar_end_conversation'),
]

subdomain_patterns = [
    # Patterns para manejar las diferentes empresas
]