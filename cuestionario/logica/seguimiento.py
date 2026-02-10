from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cuestionario.models import Trabajador, Autoevaluacion, EvaluacionJefatura

@login_required
def panel_seguimiento(request):
    # SEGURIDAD: Si no es admin, lo mandamos de vuelta al index sin explicaciones
    if not request.user.is_superuser:
        return redirect('index')

    trabajadores = Trabajador.objects.all()
    total = trabajadores.count()
    completados = 0

    for t in trabajadores:
        # Lógica de completitud
        t.auto_lista = Autoevaluacion.objects.filter(trabajador=t, estado_finalizacion=True).exists()
        
        if t.id_jefe_directo:
            t.jefe_lista = EvaluacionJefatura.objects.filter(trabajador_evaluado=t, estado_finalizacion=True).exists()
            t.finalizado = t.auto_lista and t.jefe_lista
        else:
            t.finalizado = t.auto_lista
        
        if t.finalizado:
            completados += 1

    context = {
        'trabajadores': trabajadores,
        'total': total,
        'completados': completados,
        'faltan': total - completados
    }
    return render(request, 'cuestionario/seguimiento.html', context)