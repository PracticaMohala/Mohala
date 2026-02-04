from django.urls import path
from . import logica as views
from .logica import validador_login

urlpatterns = [
    path('login/', validador_login.login_view, name='login'),
    path('logout/', validador_login.logout_view, name='logout'),

    path('', views.index, name='index'),
    
    path('autoevaluacion/<int:trabajador_id>/', 
         views.cuestionario_autoevaluacion, 
         name='autoevaluacion_inicio'),
    
    path('autoevaluacion/<int:trabajador_id>/<str:dimension>/', 
         views.cuestionario_autoevaluacion, 
         name='autoevaluacion'),

    path('autoevaluacion/finalizar/<int:trabajador_id>/', 
         views.finalizar_autoevaluacion, 
         name='finalizar_autoevaluacion'),

    path('evaluacion_jefe/<int:evaluador_id>/<int:evaluado_id>/', 
         views.cuestionario_jefatura, 
         name='evaluacion_jefe_inicio'),
    
    path('evaluacion_jefe/<int:evaluador_id>/<int:evaluado_id>/<str:dimension>/', 
         views.cuestionario_jefatura, 
         name='evaluacion_jefe'),

    path('evaluacion_jefe/finalizar/<int:evaluador_id>/<int:evaluado_id>/', 
         views.finalizar_evaluacion_jefe, 
         name='finalizar_evaluacion_jefe'),

    path('resultados/<int:trabajador_id>/<str:tipo_evaluacion>/', 
         views.ver_resultados, 
         name='ver_resultados'),
]