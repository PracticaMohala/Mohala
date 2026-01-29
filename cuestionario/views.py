from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Trabajador, TextosEvaluacion, Autoevaluacion, EvaluacionJefatura

def index(request):
    # Intentamos obtener el ID del trabajador de la URL, por defecto el 1
    trabajador_id = request.GET.get('id', 1)
    
    # Buscamos al trabajador
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # Filtramos preguntas por su nivel jerárquico
    preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
    
    # Obtenemos equipo si es jefe (usando el related_name 'subordinados' del modelo)
    equipo = trabajador.subordinados.all()
    
    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
        'equipo': equipo,
        'es_jefe': trabajador.subordinados.exists(), # Dinámico: es jefe si tiene gente a cargo
    }
    
    return render(request, 'cuestionario/index.html', context)

def cuestionario_autoevaluacion(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    if request.method == 'POST':
        # Obtenemos las preguntas del nivel del trabajador
        preguntas_list = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico)
        
        for pregunta in preguntas_list:
            # Recuperamos el puntaje del formulario usando el ID de la pregunta
            puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
            
            if puntaje_valor:
                Autoevaluacion.objects.create(
                    puntaje=puntaje_valor,
                    fecha_evaluacion=timezone.now().date(),
                    momento_evaluacion=timezone.now(),
                    trabajador=trabajador,
                    codigo_excel=pregunta, 
                    comentario=request.POST.get('comentario', '')
                )
        
        return redirect(f'/?id={trabajador.id_trabajador}')

    # Carga inicial del formulario de autoevaluación
    preguntas = TextosEvaluacion.objects.filter(
        nivel_jerarquico=trabajador.nivel_jerarquico
    ).select_related('competencia').order_by('competencia__nombre_competencia')

    context = {
        'trabajador': trabajador,
        'preguntas': preguntas,
    }
    return render(request, 'cuestionario/autoevaluacion.html', context)

def cuestionario_jefatura(request, evaluador_id, evaluado_id):
    evaluador = get_object_or_404(Trabajador, id_trabajador=evaluador_id)
    evaluado = get_object_or_404(Trabajador, id_trabajador=evaluado_id)
    
    if request.method == 'POST':
        # El jefe evalúa según las competencias del cargo del subordinado
        preguntas_list = TextosEvaluacion.objects.filter(nivel_jerarquico=evaluado.nivel_jerarquico)
        
        for pregunta in preguntas_list:
            puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
            
            if puntaje_valor:
                EvaluacionJefatura.objects.create(
                    puntaje=puntaje_valor,
                    evaluador=evaluador,
                    trabajador_evaluado=evaluado, 
                    codigo_excel=pregunta,
                    fecha_evaluacion=timezone.now().date(),
                    momento_evaluacion=timezone.now(),
                    comentario=request.POST.get('comentario', '')
                )
        
        # Redirige de vuelta al index del jefe
        return redirect(f'/?id={evaluador.id_trabajador}')

    # Carga inicial del formulario para el jefe
    preguntas = TextosEvaluacion.objects.filter(
        nivel_jerarquico=evaluado.nivel_jerarquico
    ).select_related('competencia').order_by('competencia__nombre_competencia')

    context = {
        'evaluador': evaluador,
        'evaluado': evaluado,
        'preguntas': preguntas,
    }
    return render(request, 'cuestionario/evaluacion_jefe.html', context)