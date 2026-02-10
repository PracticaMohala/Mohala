from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cuestionario.models import Trabajador, Autoevaluacion, EvaluacionJefatura

@login_required
def panel_seguimiento(request):
    if not request.user.is_superuser:
        return redirect('index')

    trabajadores = Trabajador.objects.all().select_related('cargo')
    total = trabajadores.count()
    
    # Contadores para el resumen
    autos_listas = 0
    jefaturas_listas = 0

    for t in trabajadores:
        # Estado Autoevaluación
        t.auto_lista = Autoevaluacion.objects.filter(trabajador=t, estado_finalizacion=True).exists()
        if t.auto_lista:
            autos_listas += 1
        
        # Estado Jefatura (si no tiene jefe, lo marcamos como N/A)
        if t.id_jefe_directo:
            t.tiene_jefe = True
            t.jefe_lista = EvaluacionJefatura.objects.filter(trabajador_evaluado=t, estado_finalizacion=True).exists()
            if t.jefe_lista:
                jefaturas_listas += 1
        else:
            t.tiene_jefe = False
            t.jefe_lista = False

    context = {
        'trabajadores': trabajadores,
        'total': total,
        'autos_listas': autos_listas,
        'jefaturas_listas': jefaturas_listas,
    }
    return render(request, 'cuestionario/seguimiento.html', context)