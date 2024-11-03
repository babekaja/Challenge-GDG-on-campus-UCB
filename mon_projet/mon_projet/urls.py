from django.urls import path,include
from utilisateurs import views
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('inscription/', views.inscription, name='inscription'),
    path('', views.connexion, name='connexion'),
    path('tableau_de_bord/', views.tableau_de_bord, name='tableau_de_bord'),
    path('deconnexion/', views.deconnexion, name='deconnexion'),
    path('admin/', admin.site.urls),
    path('modifier-profil/<int:utilisateur_id>/', views.modifier_profil, name='modifier_profil'),
    path('liste-utilisateurs/', views.liste_utilisateurs, name='liste_utilisateurs'),
    path('export-pdf/', views.export_pdf, name='export_pdf'),
    path('export-excel/', views.export_excel, name='export_excel'),
  
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)