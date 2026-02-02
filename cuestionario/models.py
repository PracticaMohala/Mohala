from django.db import models

# =========================
# Tabla Dimension
# =========================
class Dimension(models.Model):
    id_dimension = models.AutoField(primary_key=True)
    nombre_dimension = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dimension'

    def __str__(self):
        return self.nombre_dimension

# =========================
# Tabla Departamento
# =========================
class Departamento(models.Model):
    id_departamento = models.AutoField(primary_key=True)
    nombre_departamento = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'departamento'

    def __str__(self):
        return self.nombre_departamento

# =========================
# Tabla Nivel Jerarquico
# =========================
class NivelJerarquico(models.Model):
    id_nivel_jerarquico = models.AutoField(primary_key=True)
    nombre_nivel_jerarquico = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'nivel_jerarquico'

    def __str__(self):
        return self.nombre_nivel_jerarquico

# =========================
# Tabla Cargo
# =========================
class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=50)
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'cargo'

    def __str__(self):
        return self.nombre_cargo

# =========================
# Tabla Trabajador
# =========================
class Trabajador(models.Model):
    id_trabajador = models.AutoField(primary_key=True)
    rut = models.CharField(max_length=20, unique=True)
    id_jefe_directo = models.ForeignKey(
        'self', 
        on_delete=models.DO_NOTHING, 
        db_column='id_jefe_directo', 
        null=True, 
        blank=True, 
        related_name='subordinados'
    )
    nombre = models.CharField(max_length=40)
    apellido_paterno = models.CharField(max_length=40)
    apellido_materno = models.CharField(max_length=40)
    email = models.CharField(max_length=80)
    genero = models.CharField(max_length=10)
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )
    cargo = models.ForeignKey(
        'Cargo', 
        on_delete=models.DO_NOTHING, 
        db_column='cargo_id_cargo'
    )
    departamento = models.ForeignKey(
        'Departamento', 
        on_delete=models.DO_NOTHING, 
        db_column='departamento_id_departamento'
    )

    class Meta:
        managed = False
        db_table = 'trabajador'

    @property
    def es_jefe(self):
        return self.subordinados.exists()

    def __str__(self):
        return f"{self.nombre} {self.apellido_paterno} {self.apellido_materno} | {self.rut}"

# =========================
# Tabla Competencia
# =========================
class Competencia(models.Model):
    id_competencia = models.AutoField(primary_key=True)
    nombre_competencia = models.CharField(max_length=50)
    dimension = models.ForeignKey(
        'Dimension', 
        on_delete=models.DO_NOTHING, 
        db_column='dimension_id_dimension'
    )

    class Meta:
        managed = False
        db_table = 'competencia'

    def __str__(self):
        return self.nombre_competencia

# =========================
# Tabla Textos Evaluacion
# =========================
class TextosEvaluacion(models.Model):
    id_textos_evaluacion = models.AutoField(primary_key=True)
    codigo_excel = models.CharField(max_length=10, unique=True)
    texto = models.TextField()
    competencia = models.ForeignKey(
        'Competencia', 
        on_delete=models.DO_NOTHING, 
        db_column='competencia_id_competencia'
    )
    nivel_jerarquico = models.ForeignKey(
        'NivelJerarquico', 
        on_delete=models.DO_NOTHING, 
        db_column='nivel_jerarquico_id_nivel_jerarquico'
    )

    class Meta:
        managed = False
        db_table = 'textos_evaluacion'

    def __str__(self):
        return f"[{self.codigo_excel}] {self.competencia.nombre_competencia}"

# =========================
# Tabla Autoevaluacion
# =========================
class Autoevaluacion(models.Model):
    id_autoevaluacion = models.AutoField(primary_key=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)
    fecha_evaluacion = models.DateField()
    momento_evaluacion = models.DateTimeField()
    estado_finalizacion = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True)
    trabajador = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='trabajador_id_trabajador'
    )
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )

    class Meta:
        managed = False
        db_table = 'autoevaluacion'
        unique_together = (('trabajador', 'codigo_excel'),)

    def __str__(self):
        return f"{self.codigo_excel.codigo_excel} | {self.puntaje} | {self.trabajador.nombre} {self.trabajador.apellido_paterno} | {self.trabajador.rut}"

# =========================
# Tabla Evaluacion Jefatura
# =========================
class EvaluacionJefatura(models.Model):
    id_evaluacion_jefatura = models.AutoField(primary_key=True)
    puntaje = models.DecimalField(max_digits=5, decimal_places=2)
    evaluador = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='evaluador_id_trabajador', 
        related_name='jefe_evaluador'
    )
    fecha_evaluacion = models.DateField()
    momento_evaluacion = models.DateTimeField()
    estado_finalizacion = models.BooleanField(default=False)
    comentario = models.TextField(null=True, blank=True)
    trabajador_evaluado = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='trabajador_id_trabajador', 
        related_name='subordinado_evaluado'
    )
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )

    class Meta:
        managed = False
        db_table = 'evaluacion_jefatura'
        unique_together = (('evaluador', 'trabajador_evaluado', 'codigo_excel'),)
    
    def __str__(self):
        return f"{self.codigo_excel.codigo_excel} | {self.puntaje} | Jefe: {self.evaluador.nombre} {self.evaluador.apellido_paterno} -> Trabajador Evaluado: {self.trabajador_evaluado.nombre} {self.trabajador_evaluado.apellido_paterno}"
    
# =========================
# Tabla Resultado Consolidado
# =========================
class ResultadoConsolidado(models.Model):
    id_resultado = models.AutoField(primary_key=True)
    puntaje_autoev = models.DecimalField(max_digits=5, decimal_places=2)
    puntaje_jefe = models.DecimalField(max_digits=5, decimal_places=2)
    diferencia = models.DecimalField(max_digits=5, decimal_places=2)
    prom_competencia = models.DecimalField(max_digits=5, decimal_places=2)
    prom_dimension = models.DecimalField(max_digits=5, decimal_places=2)
    prom_general = models.DecimalField(max_digits=5, decimal_places=2)

    trabajador = models.ForeignKey(
        'Trabajador', 
        on_delete=models.DO_NOTHING, 
        db_column='trabajador_id_trabajador'
    )
    dimension = models.ForeignKey(
        'Dimension', 
        on_delete=models.DO_NOTHING, 
        db_column='dimension_id_dimension'
    )
    competencia = models.ForeignKey(
        'Competencia', 
        on_delete=models.DO_NOTHING, 
        db_column='competencia_id_competencia'
    )
    codigo_excel = models.ForeignKey(
        'TextosEvaluacion', 
        on_delete=models.DO_NOTHING, 
        to_field='codigo_excel', 
        db_column='codigo_excel'
    )
    
    # Control Temporal
    periodo = models.IntegerField()
    fecha_consolidacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        managed = False
        db_table = 'resultado_consolidado'
        unique_together = (('trabajador', 'codigo_excel', 'periodo'),)

    def __str__(self):
        return (
            f"Consolidado {self.periodo} | "
            f"{self.trabajador.nombre} {self.trabajador.apellido_paterno} {self.trabajador.apellido_materno} | "
            f"Dim: {self.dimension.nombre_dimension if self.dimension else 'N/A'} | "
            f"Comp: {self.competencia.nombre_competencia if self.competencia else 'N/A'} | "
            f"{self.codigo_excel} | "
            f"Prom. Dim: {self.prom_dimension} | "
            f"Prom. Comp: {self.prom_competencia} | "
            f"Prom. Gral: {self.prom_general} | "
            f"Dif: {self.diferencia}"
        )