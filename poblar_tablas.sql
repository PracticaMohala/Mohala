--- =========================
-- Poblamiento de tabla Dimension
-- =========================
INSERT INTO dimension (id_dimension, nombre_dimension)
VALUES 
(1, 'Organizacionales'),
(2, 'Funcionales');

-- =========================
-- Poblamiento de tabla Nivel Jerárquico
-- =========================
INSERT INTO nivel_jerarquico (id_nivel_jerarquico, nombre_nivel_jerarquico)
VALUES 
(1, 'Operativo'),
(2, 'Tactico'),
(3, 'Estrategico');

-- =========================
-- Poblamiento de tabla Cargo
-- =========================

-- Cargos Operativos (Nivel 1)
INSERT INTO cargo (id_cargo, nombre_cargo, nivel_jerarquico_id_nivel_jerarquico) VALUES
(1, 'Analista', 1),
(2, 'Técnico en Informática', 1),
(3, 'Asistente Administrativo', 1),
(4, 'Cajero', 1),
(5, 'Operario de Producción', 1),
(6, 'Guardia de Seguridad', 1),
(7, 'Chofer', 1),
(8, 'Secretaria', 1),
(9, 'Paramédico', 1),
(10, 'Auxiliar de Enfermería', 1),
(11, 'Vendedor', 1),
(12, 'Contador Junior', 1),
(13, 'Recepcionista', 1),
(14, 'Auxiliar de Aseo', 1),
(15, 'Digitador', 1);

-- Cargos Tácticos (Nivel 2)
INSERT INTO cargo (id_cargo, nombre_cargo, nivel_jerarquico_id_nivel_jerarquico) VALUES
(16, 'Supervisor de Ventas', 2),
(17, 'Jefe de Área', 2),
(18, 'Coordinador de Proyectos', 2),
(19, 'Ingeniero de Procesos', 2),
(20, 'Jefe de Recursos Humanos', 2),
(21, 'Encargado de Logística', 2),
(22, 'Subgerente Comercial', 2),
(23, 'Coordinador de Finanzas', 2),
(24, 'Profesor Jefe', 2),
(25, 'Médico Jefe de Servicio', 2),
(26, 'Supervisor de Producción', 2),
(27, 'Encargado de Calidad', 2),
(28, 'Coordinador de Marketing', 2),
(29, 'Jefe de Operaciones', 2),
(30, 'Coordinador Académico', 2);

-- Cargos Estratégicos (Nivel 3)
INSERT INTO cargo (id_cargo, nombre_cargo, nivel_jerarquico_id_nivel_jerarquico) VALUES
(31, 'Gerente General', 3),
(32, 'Director de Operaciones', 3),
(33, 'Director Médico', 3),
(34, 'CEO', 3),
(35, 'CFO', 3),
(36, 'COO', 3),
(37, 'Gerente de Innovación', 3),
(38, 'Gerente de Finanzas', 3),
(39, 'Gerente de Recursos Humanos', 3),
(40, 'Gerente Comercial', 3),
(41, 'Gerente de Marketing', 3),
(42, 'Director Académico', 3),
(43, 'Rector de Universidad', 3),
(44, 'Socio Fundador', 3),
(45, 'Presidente de Empresa', 3);

-- =========================
-- Poblamiento de tabla Competencia
-- =========================

-- Competencias Organizacionales (Dimension 1)
INSERT INTO competencia (id_competencia, nombre_competencia, dimension_id_dimension) VALUES
(1, 'Creatividad e Innovacion', 1),
(2, 'Enfoque de Negocio', 1),
(3, 'Identificacion Cultural', 1),
(4, 'Trabajo en Equipo', 1),
(5, 'Vision Global y Sistematica', 1);

-- Competencias Funcionales (Dimension 2)
INSERT INTO competencia (id_competencia, nombre_competencia, dimension_id_dimension) VALUES
(6, 'Analisis y Solucion de Problemas', 2),
(7, 'Aprendizaje e Innovacion', 2),
(8, 'Comunicacion', 2),
(9, 'Innovacion', 2),
(10, 'Liderazgo', 2),
(11, 'Liderazgo y Desarrollo de Equipos', 2),
(12, 'Orientacion a la Rentabilidad', 2),
(13, 'Orientacion al Logro', 2),
(14, 'Planificacion Estrategica', 2),
(15, 'Proactividad', 2);
