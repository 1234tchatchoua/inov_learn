from django.urls import path
from . import views

urlpatterns = [
    path('', views.accueil, name='accueil'),
    path('connexion-etudiant/', views.connexion_etudiant, name='connexion_etudiant'),
    path('connexion-enseignant/', views.connexion_enseignant, name='connexion_enseignant'),
    path('dashboard-admin/', views.dashboard_admin, name='dashboard_admin'),
    path('etudiants/', views.students, name='etudiants'),
    path('dashboard-etudiant/', views.dashboard_etudiant, name='dashboard_etudiant'),
    path('deconnexion-etudiant/', views.deconnexion_etudiant, name='deconnexion_etudiant'),
    path('admin-login/', views.login_admin, name='login_admin'),
    path('admin-inscription/', views.inscription_admin, name='inscription_admin'),
    path('enseignants/', views.enseignants, name='enseignants'),
    path('filieres/', views.filieres, name='filieres'),
    path('cours/', views.cours, name='cours'),
    path('paiements/', views.paiements, name='paiements'),
    path('paiement/recu/<int:id>/', views.recu_paiement, name='recu_paiement'),
    path('emploi-du-temps/', views.emploi_du_temps, name='emploi_du_temps'),
    path('emploi-events/', views.emploi_events, name='emploi_events'),
    path('evaluation-teacher/', views.evaluation_teacher, name='evaluation_teacher'),


]
