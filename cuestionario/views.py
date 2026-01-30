from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Trabajador, TextosEvaluacion, Autoevaluacion, EvaluacionJefatura
from django.db import transaction

def index(request):
    trabajador_id = request.GET.get('id', 1)
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    hecho_org = Autoevaluacion.objects.filter(
        trabajador=trabajador, 
        codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional"
    ).exists()
    hecho_fun = Autoevaluacion.objects.filter(
        trabajador=trabajador, 
        codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional"
    ).exists()
    
    equipo = trabajador.subordinados.all()
    for sub in equipo:
        sub_org = EvaluacionJefatura.objects.filter(
            evaluador=trabajador, 
            trabajador_evaluado=sub,
            codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional"
        ).exists()
        sub_fun = EvaluacionJefatura.objects.filter(
            evaluador=trabajador, 
            trabajador_evaluado=sub,
            codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional"
        ).exists()
        sub.ya_evaluado = sub_org and sub_fun

    context = {
        'trabajador': trabajador,
        'es_jefe': trabajador.subordinados.exists(),
        'equipo': equipo,
        'ya_hizo_autoevaluacion': hecho_org and hecho_fun,
    }
    return render(request, 'cuestionario/index.html', context)

def cuestionario_autoevaluacion(request, trabajador_id, dimension=None):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    if not dimension:
        hecho_org = Autoevaluacion.objects.filter(
            trabajador=trabajador, 
            codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional"
        ).exists()
        hecho_fun = Autoevaluacion.objects.filter(
            trabajador=trabajador, 
            codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional"
        ).exists()
        
        return render(request, 'cuestionario/autoevaluacion_seleccion.html', {
            'trabajador': trabajador,
            'hecho_org': hecho_org,
            'hecho_fun': hecho_fun
        })

    preguntas_qs = TextosEvaluacion.objects.filter(
        nivel_jerarquico=trabajador.nivel_jerarquico,
        competencia__dimension__nombre_dimension__icontains=dimension
    ).select_related('competencia__dimension').order_by('competencia__id_competencia')

    if request.method == 'POST':
        with transaction.atomic():
            for pregunta in preguntas_qs:
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
        return redirect('autoevaluacion_inicio', trabajador_id=trabajador.id_trabajador)

    context = {
        'trabajador': trabajador,
        'preguntas': preguntas_qs,
        'dimension': dimension,
    }
    return render(request, 'cuestionario/autoevaluacion.html', context)

def cuestionario_jefatura(request, evaluador_id, evaluado_id, dimension=None):
    evaluador = get_object_or_404(Trabajador, id_trabajador=evaluador_id)
    evaluado = get_object_or_404(Trabajador, id_trabajador=evaluado_id)
    
    if not dimension:
        hecho_org = EvaluacionJefatura.objects.filter(
            evaluador=evaluador, 
            trabajador_evaluado=evaluado, 
            codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional"
        ).exists()
        hecho_fun = EvaluacionJefatura.objects.filter(
            evaluador=evaluador, 
            trabajador_evaluado=evaluado, 
            codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional"
        ).exists()
        
        return render(request, 'cuestionario/evaluacion_jefe_seleccion.html', {
            'evaluador': evaluador,
            'evaluado': evaluado,
            'hecho_org': hecho_org,
            'hecho_fun': hecho_fun
        })

    preguntas_qs = TextosEvaluacion.objects.filter(
        nivel_jerarquico=evaluado.nivel_jerarquico,
        competencia__dimension__nombre_dimension__icontains=dimension
    ).select_related('competencia__dimension').order_by('competencia__id_competencia')

    if request.method == 'POST':
        with transaction.atomic():
            for pregunta in preguntas_qs:
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

        return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador.id_trabajador, evaluado_id=evaluado.id_trabajador)

    context = {
        'evaluador': evaluador,
        'evaluado': evaluado,
        'preguntas': preguntas_qs,
        'dimension': dimension,
    }
    return render(request, 'cuestionario/evaluacion_jefe.html', context)