from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('autoevaluacion/<int:trabajador_id>/', views.cuestionario_autoevaluacion, name='autoevaluacion'),
    path('evaluacion_jefe/<int:evaluador_id>/<int:evaluado_id>/', views.cuestionario_jefatura, name='evaluacion_jefe'),
]