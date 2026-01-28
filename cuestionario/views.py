from django.shortcuts import render, get_object_or_404
from .models import Trabajador, TextosEvaluacion

def index(request):
    # Por ahora, vamos a pasar un ID por la URL para probar
    trabajador_id = request.GET.get('id', 1) # Por defecto el ID 1 si no hay nada
    
    # Buscamos al trabajador en la base de datos
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # 1. Lógica de preguntas: Filtramos por el nivel jerárquico del trabajador
    preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
    
    # 2. Lógica de jefatura: Traemos a sus subordinados usando el related_name
    equipo = trabajador.subordinados.all()
    
    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
        'equipo': equipo,
        'es_jefe': trabajador.es_jefe, # Usamos la propiedad que creamos en models
    }
    
    return render(request, 'cuestionario/index.html', context)