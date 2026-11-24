-- =============================================
-- Clima Fácil — Script 03: Insertar datos iniciales
-- =============================================
-- Prerequisito: haber ejecutado 01 y 02.
-- Inserta los datos base del proyecto usando
-- MERGE para ser idempotente (no duplica).
-- =============================================

USE ClimaFacilDB;
GO

-- =============================================
-- Ubicacion: Huancayo, Valle del Mantaro
-- =============================================
SET IDENTITY_INSERT Ubicacion ON;

MERGE INTO Ubicacion AS target
USING (VALUES
    (1, N'Huancayo', -12.065100, -75.204900)
) AS src (id_ubicacion, nombre, latitud, longitud)
ON target.id_ubicacion = src.id_ubicacion
WHEN NOT MATCHED THEN
    INSERT (id_ubicacion, nombre, latitud, longitud)
    VALUES (src.id_ubicacion, src.nombre, src.latitud, src.longitud);

SET IDENTITY_INSERT Ubicacion OFF;
GO

PRINT 'Ubicacion: datos insertados (1 registro — Huancayo).';
GO

-- =============================================
-- Cultivo: Papa, Maíz, Haba
-- =============================================
SET IDENTITY_INSERT Cultivo ON;

MERGE INTO Cultivo AS target
USING (VALUES
    (1, N'Papa', N'Cultivo alimenticio que requiere un manejo adecuado del agua y del suelo.'),
    (2, N'Maiz', N'Cultivo que necesita condiciones adecuadas de temperatura y humedad.'),
    (3, N'Haba', N'Leguminosa cultivada para consumo alimenticio.')
) AS src (id_cultivo, nombre, descripcion)
ON target.id_cultivo = src.id_cultivo
WHEN NOT MATCHED THEN
    INSERT (id_cultivo, nombre, descripcion)
    VALUES (src.id_cultivo, src.nombre, src.descripcion);

SET IDENTITY_INSERT Cultivo OFF;
GO

PRINT 'Cultivo: datos insertados (3 registros — Papa, Maiz, Haba).';
GO

-- =============================================
-- Recomendacion: 5 recomendaciones agrícolas
-- =============================================
SET IDENTITY_INSERT Recomendacion ON;

MERGE INTO Recomendacion AS target
USING (VALUES
    (1, 1, N'lluvia_alta',    N'Precaucion',  N'Revisa que el terreno tenga buen drenaje y evita trabajar en suelo saturado.'),
    (2, 1, N'helada_probable',N'Importante',  N'Revisa las condiciones de tu cultivo y considera medidas de protección frente a las heladas.'),
    (3, 2, N'lluvia_alta',    N'Precaucion',  N'Evita labores agrícolas en terrenos con exceso de agua y revisa el drenaje.'),
    (4, 2, N'calor_intenso',  N'Precaucion',  N'Vigila la humedad del suelo y revisa si el cultivo necesita riego.'),
    (5, 3, N'helada_probable',N'Importante',  N'Presta atención a las alertas de heladas y evalúa medidas de protección.')
) AS src (id_recomendacion, id_cultivo, condicion_climatica, nivel, mensaje)
ON target.id_recomendacion = src.id_recomendacion
WHEN NOT MATCHED THEN
    INSERT (id_recomendacion, id_cultivo, condicion_climatica, nivel, mensaje)
    VALUES (src.id_recomendacion, src.id_cultivo, src.condicion_climatica, src.nivel, src.mensaje);

SET IDENTITY_INSERT Recomendacion OFF;
GO

PRINT 'Recomendacion: datos insertados (5 registros).';
GO

-- =============================================
-- Nota: La tabla Historial no tiene datos de
-- semilla — se llena en tiempo de ejecución
-- mediante sp_RegistrarHistorial.
-- =============================================
PRINT 'Script 03 completado. Base de datos lista con datos iniciales.';
GO
