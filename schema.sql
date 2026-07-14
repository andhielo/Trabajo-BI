-- =========================================================================
-- BASE DE DATOS: db_salud_mental_universitaria
-- Plataforma Integral de Analítica con BI, Big Data e IA Ética
-- Lima Norte - Perú (UNI, UCH, UCV, UPN)
-- =========================================================================

CREATE DATABASE IF NOT EXISTS db_salud_mental_universitaria;
USE db_salud_mental_universitaria;

-- 1. Tabla de Universidades
CREATE TABLE IF NOT EXISTS universidades (
    id_universidad INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(150) NOT NULL,
    abreviatura VARCHAR(10) NOT NULL,
    distrito_sede VARCHAR(100) NOT NULL
);

-- 2. Tabla de Estudiantes (Datos Anonimizados con Hash Hash_ID)
CREATE TABLE IF NOT EXISTS estudiantes_anonimos (
    hash_id VARCHAR(64) PRIMARY KEY, -- Identificador único irreversible (SHA-256)
    id_universidad INT NOT NULL,
    edad INT NOT NULL,
    sexo VARCHAR(20) NOT NULL,
    distrito_residencia VARCHAR(100) NOT NULL,
    ciclo_academico INT NOT NULL,
    FOREIGN KEY (id_universidad) REFERENCES universidades(id_universidad)
);

-- 3. Tabla de Evaluaciones de Salud Mental (Indicadores BI y Big Data)
CREATE TABLE IF NOT EXISTS evaluaciones_salud_mental (
    id_evaluacion INT AUTO_INCREMENT PRIMARY KEY,
    hash_id VARCHAR(64) NOT NULL,
    fecha_evaluacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    puntuacion_ansiedad_gad7 INT NOT NULL, -- Rango 0-21
    puntuacion_depresion_phq9 INT NOT NULL, -- Rango 0-27
    nivel_estres_percibido INT NOT NULL, -- Rango 1-10
    horas_sueno_promedio DECIMAL(3,1) NOT NULL,
    tiene_apoyo_social_activo BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (hash_id) REFERENCES estudiantes_anonimos(hash_id)
);

-- 4. Tabla de Predicciones del Modelo de IA Ética
CREATE TABLE IF NOT EXISTS predicciones_ia_etica (
    id_prediccion INT AUTO_INCREMENT PRIMARY KEY,
    hash_id VARCHAR(64) NOT NULL,
    fecha_prediccion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    probabilidad_riesgo_critico DECIMAL(5,4) NOT NULL, -- 0.0000 a 1.0000
    nivel_riesgo_asignado VARCHAR(30) NOT NULL, -- 'Bajo', 'Moderado', 'Crítico'
    explicabilidad_sh_factor VARCHAR(255) NOT NULL, -- Explicación del factor principal del riesgo
    token_canalizacion_anonimo VARCHAR(64) UNIQUE, -- Token para que el psicólogo atienda sin saber quién es
    FOREIGN KEY (hash_id) REFERENCES estudiantes_anonimos(hash_id)
);

-- =========================================================================
-- INSERTANDO DATOS MOCK / SEMILLA (DATASETS DE PRUEBA)
-- =========================================================================

-- Poblado de Universidades en Lima Norte
INSERT INTO universidades (nombre, abreviatura, distrito_sede) VALUES
('Universidad Nacional de Ingeniería', 'UNI', 'Rímac'),
('Universidad de Ciencias y Humanidades', 'UCH', 'Los Olivos'),
('Universidad César Vallejo', 'UCV', 'Los Olivos'),
('Universidad Privada del Norte', 'UPN', 'Los Olivos');

-- Estudiantes Anonimizados (SHA256 simulado)
INSERT INTO estudiantes_anonimos (hash_id, id_universidad, edad, sexo, distrito_residencia, ciclo_academico) VALUES
('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 1, 20, 'Masculino', 'Independencia', 4),
('82194600122e22c9545dc65fa09163e72bc46059d4fbf1ff54c15509dfc9d64a', 2, 22, 'Femenino', 'Los Olivos', 6),
('e532a4d7948c490eba6723a4c010c2fc65fa09163e72bc46059d4fbf1ff54c155', 3, 19, 'Femenino', 'Comas', 2),
('6e0fd64f3716480e8a368770fb25e902bc46059d4fbf1ff54c15509dfc9d64a77', 4, 21, 'Masculino', 'Carabayllo', 5);

-- Evaluaciones de Salud Mental
INSERT INTO evaluaciones_salud_mental (hash_id, puntuacion_ansiedad_gad7, puntuacion_depresion_phq9, nivel_estres_percibido, horas_sueno_promedio, tiene_apoyo_social_activo) VALUES
('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 12, 14, 8, 5.0, FALSE),
('82194600122e22c9545dc65fa09163e72bc46059d4fbf1ff54c15509dfc9d64a', 4, 3, 3, 7.5, TRUE),
('e532a4d7948c490eba6723a4c010c2fc65fa09163e72bc46059d4fbf1ff54c155', 15, 18, 9, 4.5, FALSE),
('6e0fd64f3716480e8a368770fb25e902bc46059d4fbf1ff54c15509dfc9d64a77', 6, 8, 5, 6.0, TRUE);

-- Predicciones con IA Ética
INSERT INTO predicciones_ia_etica (hash_id, probabilidad_riesgo_critico, nivel_riesgo_asignado, explicabilidad_sh_factor, token_canalizacion_anonimo) VALUES
('e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855', 0.8200, 'Crítico', 'Bajas horas de sueño y falta de apoyo social activo.', 'TOKEN-A173-UNI'),
('82194600122e22c9545dc65fa09163e72bc46059d4fbf1ff54c15509dfc9d64a', 0.1100, 'Bajo', 'Sueño adecuado y fuerte soporte social.', 'TOKEN-B294-UCH'),
('e532a4d7948c490eba6723a4c010c2fc65fa09163e72bc46059d4fbf1ff54c155', 0.9400, 'Crítico', 'Puntuación GAD-7 y PHQ-9 extremadamente elevada.', 'TOKEN-C821-UCV'),
('6e0fd64f3716480e8a368770fb25e902bc46059d4fbf1ff54c15509dfc9d64a77', 0.3500, 'Moderado', 'Estrés académico moderado pero con red de apoyo activa.', 'TOKEN-D441-UPN');
