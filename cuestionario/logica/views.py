from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from cuestionario.models import Trabajador, TextosEvaluacion, Autoevaluacion, EvaluacionJefatura
from django.db import transaction

# =========================
# VISTA INDEX (DASHBOARD)
# =========================
def index(request):
    trabajador_id = request.GET.get('id', 1)
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    # Verifica si el usuario actual terminó su propia autoevaluación
    autoeval_completada = Autoevaluacion.objects.filter(
        trabajador=trabajador, 
        estado_finalizacion=True
    ).exists()
    
    equipo = trabajador.subordinados.all()
    
    # BUCLE DE PREPARACIÓN DE EQUIPO
    for sub in equipo:
        # Esto permite que el botón de jefatura se habilite/deshabilite en el HTML
        sub.autoevaluacion_terminada = Autoevaluacion.objects.filter(
            trabajador=sub, 
            estado_finalizacion=True
        ).exists()
        
        # Verifica si el jefe ya cerró la evaluación de este subordinado
        sub.ya_evaluado = EvaluacionJefatura.objects.filter(
            evaluador=trabajador, 
            trabajador_evaluado=sub,
            estado_finalizacion=True
        ).exists()

    context = {
        'trabajador': trabajador,
        'es_jefe': trabajador.subordinados.exists(),
        'equipo': equipo,
        'ya_hizo_autoevaluacion': autoeval_completada,
    }
    return render(request, 'cuestionario/index.html', context)

# =========================
# LÓGICA AUTOEVALUACIÓN
# =========================
def cuestionario_autoevaluacion(request, trabajador_id, dimension=None):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    
    if not dimension:
        respuestas = Autoevaluacion.objects.filter(trabajador=trabajador)
        ya_finalizado = respuestas.filter(estado_finalizacion=True).exists()
        
        total_preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=trabajador.nivel_jerarquico).count()
        total_respuestas = respuestas.count()
        
        listo_para_enviar = (total_respuestas >= total_preguntas) and not ya_finalizado
        
        hecho_org = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional").exists()
        hecho_fun = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional").exists()
        
        return render(request, 'cuestionario/autoevaluacion_seleccion.html', {
            'trabajador': trabajador,
            'hecho_org': hecho_org,
            'hecho_fun': hecho_fun,
            'listo_para_enviar': listo_para_enviar,
            'ya_finalizado': ya_finalizado
        })

    ya_respondido = Autoevaluacion.objects.filter(
        trabajador=trabajador,
        codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension
    ).exists()

    if ya_respondido:
        return redirect('autoevaluacion_inicio', trabajador_id=trabajador.id_trabajador)

    preguntas_qs = TextosEvaluacion.objects.filter(
        nivel_jerarquico=trabajador.nivel_jerarquico,
        competencia__dimension__nombre_dimension__icontains=dimension
    ).select_related('competencia__dimension').order_by('competencia__id_competencia')

    if request.method == 'POST':
        with transaction.atomic():
            for pregunta in preguntas_qs:
                puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
                if puntaje_valor:
                    Autoevaluacion.objects.update_or_create(
                        trabajador=trabajador,
                        codigo_excel=pregunta,
                        defaults={
                            'puntaje': puntaje_valor,
                            'fecha_evaluacion': timezone.now().date(),
                            'momento_evaluacion': timezone.now(),
                            'comentario': request.POST.get('comentario', ''),
                            'estado_finalizacion': False
                        }
                    )
        return redirect('autoevaluacion_inicio', trabajador_id=trabajador.id_trabajador)

    context = {'trabajador': trabajador, 'preguntas': preguntas_qs, 'dimension': dimension}
    return render(request, 'cuestionario/autoevaluacion.html', context)

def finalizar_autoevaluacion(request, trabajador_id):
    if request.method == "POST":
        Autoevaluacion.objects.filter(trabajador_id=trabajador_id).update(estado_finalizacion=True)
    return redirect('autoevaluacion_inicio', trabajador_id=trabajador_id)

# =========================
# LÓGICA EVALUACIÓN JEFATURA
# =========================
def cuestionario_jefatura(request, evaluador_id, evaluado_id, dimension=None):
    evaluador = get_object_or_404(Trabajador, id_trabajador=evaluador_id)
    evaluado = get_object_or_404(Trabajador, id_trabajador=evaluado_id)
    
    # Solo permite entrar si el evaluado YA FINALIZÓ su autoevaluación
    autoeval_lista = Autoevaluacion.objects.filter(
        trabajador=evaluado, 
        estado_finalizacion=True
    ).exists()

    if not autoeval_lista:
        # Si no ha terminado, lo regresamos al index con su ID de jefe
        return redirect(f"/?id={evaluador_id}")
    # ---------------------------------

    if not dimension:
        respuestas = EvaluacionJefatura.objects.filter(evaluador=evaluador, trabajador_evaluado=evaluado)
        ya_finalizado = respuestas.filter(estado_finalizacion=True).exists()
        
        total_preguntas = TextosEvaluacion.objects.filter(nivel_jerarquico=evaluado.nivel_jerarquico).count()
        total_respuestas = respuestas.count()
        
        listo_para_enviar = (total_respuestas >= total_preguntas) and not ya_finalizado
        
        hecho_org = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Organizacional").exists()
        hecho_fun = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains="Funcional").exists()
        
        return render(request, 'cuestionario/evaluacion_jefe_seleccion.html', {
            'evaluador': evaluador,
            'evaluado': evaluado,
            'hecho_org': hecho_org,
            'hecho_fun': hecho_fun,
            'listo_para_enviar': listo_para_enviar,
            'ya_finalizado': ya_finalizado
        })

    ya_respondido = EvaluacionJefatura.objects.filter(
        evaluador=evaluador,
        trabajador_evaluado=evaluado,
        codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension
    ).exists()

    if ya_respondido:
        return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador.id_trabajador, evaluado_id=evaluado.id_trabajador)

    preguntas_qs = TextosEvaluacion.objects.filter(
        nivel_jerarquico=evaluado.nivel_jerarquico,
        competencia__dimension__nombre_dimension__icontains=dimension
    ).select_related('competencia__dimension').order_by('competencia__id_competencia')

    if request.method == 'POST':
        with transaction.atomic():
            for pregunta in preguntas_qs:
                puntaje_valor = request.POST.get(f'puntaje_{pregunta.id_textos_evaluacion}')
                if puntaje_valor:
                    EvaluacionJefatura.objects.update_or_create(
                        evaluador=evaluador,
                        trabajador_evaluado=evaluado,
                        codigo_excel=pregunta,
                        defaults={
                            'puntaje': puntaje_valor,
                            'fecha_evaluacion': timezone.now().date(),
                            'momento_evaluacion': timezone.now(),
                            'comentario': request.POST.get('comentario', ''),
                            'estado_finalizacion': False
                        }
                    )
        return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador.id_trabajador, evaluado_id=evaluado.id_trabajador)

    context = {'evaluador': evaluador, 'evaluado': evaluado, 'preguntas': preguntas_qs, 'dimension': dimension}
    return render(request, 'cuestionario/evaluacion_jefe.html', context)

def finalizar_evaluacion_jefe(request, evaluador_id, evaluado_id):
    if request.method == "POST":
        EvaluacionJefatura.objects.filter(
            evaluador_id=evaluador_id, 
            trabajador_evaluado_id=evaluado_id
        ).update(estado_finalizacion=True)
    return redirect('evaluacion_jefe_inicio', evaluador_id=evaluador_id, evaluado_id=evaluado_id)

# =========================
# VISTA DE RESULTADOS
# =========================
def ver_resultados(request, trabajador_id, tipo_evaluacion):
    trabajador = get_object_or_404(Trabajador, id_trabajador=trabajador_id)
    dimension_filtro = request.GET.get('dimension')

    if tipo_evaluacion == 'auto':
        respuestas = Autoevaluacion.objects.filter(trabajador=trabajador)
        visor_id = trabajador.id_trabajador
    else:
        evaluador_id = request.GET.get('evaluador_id')
        respuestas = EvaluacionJefatura.objects.filter(trabajador_evaluado=trabajador, evaluador_id=evaluador_id)
        visor_id = evaluador_id

    respuestas = respuestas.select_related('codigo_excel__competencia__dimension')

    if dimension_filtro:
        respuestas = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension__icontains=dimension_filtro)

    dimensiones_data = {}
    dimensiones_nombres = respuestas.values_list('codigo_excel__competencia__dimension__nombre_dimension', flat=True).distinct()
    
    for dim in dimensiones_nombres:
        dimensiones_data[dim] = respuestas.filter(codigo_excel__competencia__dimension__nombre_dimension=dim)

    context = {
        'trabajador': trabajador,
        'dimensiones': dimensiones_data,
        'comentario_final': respuestas.first().comentario if respuestas.exists() else "",
        'fecha_cierre': respuestas.first().momento_evaluacion if respuestas.exists() else None,
        'visor_id': visor_id,
        'tipo_evaluacion': tipo_evaluacion
    }
    return render(request, 'cuestionario/ver_resultados.html', context)