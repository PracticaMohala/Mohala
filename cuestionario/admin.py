from django.contrib import admin
from .models import (
    Dimension, Departamento, NivelJerarquico, Cargo, Trabajador, 
    Competencia, TextosEvaluacion, Autoevaluacion, 
    EvaluacionJefatura, ResultadoConsolidado
)

# --- Configuración Estética ---
admin.site.site_header = "Administración Sistema Mohala"
admin.site.index_title = "Panel de Control Evaluación 2026"

@admin.register(Trabajador)
class TrabajadorAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'apellido_paterno', 'apellido_materno', 'rut', 'email', 'cargo', 'departamento', 'id_jefe_directo')
    list_filter = ('nivel_jerarquico', 'departamento', 'cargo')
    search_fields = ('nombre', 'apellido_paterno', 'rut', 'email')
    ordering = ('apellido_paterno', 'nombre')

@admin.register(Cargo)
class CargoAdmin(admin.ModelAdmin):
    list_display = ('nombre_cargo', 'nivel_jerarquico')
    list_filter = ('nivel_jerarquico',)

@admin.register(Competencia)
class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('nombre_competencia', 'dimension')
    list_filter = ('dimension',)

@admin.register(TextosEvaluacion)
class TextosEvaluacionAdmin(admin.ModelAdmin):
    list_display = ('codigo_excel', 'competencia', 'nivel_jerarquico', 'get_texto_corto')
    list_filter = ('nivel_jerarquico', 'competencia__dimension', 'competencia')
    search_fields = ('codigo_excel', 'texto')

    @admin.display(description='Pregunta')
    def get_texto_corto(self, obj):
        return (obj.texto[:60] + '...') if len(obj.texto) > 60 else obj.texto

@admin.register(Autoevaluacion)
class AutoevaluacionAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'codigo_excel', 'puntaje', 'estado_finalizacion', 'fecha_evaluacion')
    list_filter = ('estado_finalizacion', 'fecha_evaluacion', 'nivel_jerarquico')
    search_fields = ('trabajador__nombre', 'trabajador__apellido_paterno', 'codigo_excel__codigo_excel')

@admin.register(EvaluacionJefatura)
class EvaluacionJefaturaAdmin(admin.ModelAdmin):
    list_display = ('evaluador', 'trabajador_evaluado', 'codigo_excel', 'puntaje', 'estado_finalizacion')
    list_filter = ('estado_finalizacion', 'evaluador', 'trabajador_evaluado')

@admin.register(ResultadoConsolidado)
class ResultadoConsolidadoAdmin(admin.ModelAdmin):
    list_display = ('trabajador', 'codigo_excel', 'puntaje_autoev', 'puntaje_jefe', 'diferencia', 'periodo')
    list_filter = ('periodo', 'trabajador')
    readonly_fields = ('diferencia',)

# Registros simples
admin.site.register(Dimension)
admin.site.register(Departamento)
admin.site.register(NivelJerarquico)