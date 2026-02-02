from django.contrib import admin
from .models import (
    Dimension,
    NivelJerarquico,
    Cargo,
    Trabajador,
    Competencia,
    TextosEvaluacion,
    Autoevaluacion,
    EvaluacionJefatura,
    ResultadoConsolidado
)

# 1. Registros que NO tienen personalización (se quedan así)
admin.site.register(Dimension)
admin.site.register(NivelJerarquico)
admin.site.register(Cargo)
admin.site.register(Trabajador)
admin.site.register(Competencia)
admin.site.register(TextosEvaluacion)

# 2. Registros con Personalización (Usan decorador, NO repetir abajo)
@admin.register(Autoevaluacion)
class AutoevaluacionAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'codigo_excel', 'puntaje', 'estado_finalizacion')
    ordering = ('codigo_excel__id_textos_evaluacion',)
    list_filter = ('trabajador', 'estado_finalizacion')

@admin.register(EvaluacionJefatura)
class EvaluacionJefaturaAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'trabajador_evaluado', 'codigo_excel', 'puntaje', 'estado_finalizacion')
    ordering = ('codigo_excel__id_textos_evaluacion',)
    list_filter = ('evaluador', 'trabajador_evaluado', 'estado_finalizacion')

@admin.register(ResultadoConsolidado)
class ResultadoConsolidadoAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'codigo_excel', 'puntaje_jefe', 'puntaje_autoev', 'diferencia', 'periodo')
    ordering = ('codigo_excel__id_textos_evaluacion',)
    list_filter = ('trabajador', 'periodo')