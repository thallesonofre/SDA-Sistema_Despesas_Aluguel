from django.urls import path 
from myapp import views

urlpatterns = [
    path('conta', views.conta_list, name='conta-list'), 
    path('create-conta/', views.form_conta, name='conta-create'), 
    path('export-csv/', views.export_csv, name='export-csv'),
    path('export-pdf/', views.export_pdf, name='export-pdf'),    
]