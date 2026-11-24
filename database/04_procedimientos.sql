-- =============================================
-- Clima Fácil — Script 04: Procedimientos almacenados
-- =============================================
-- Prerequisito: haber ejecutado 01, 02 y 03.
-- Crea o reemplaza los cuatro procedimientos
-- almacenados del proyecto.
-- =============================================

USE ClimaFacilDB;
GO

-- =============================================
-- PROCEDIMIENTO 1: sp_ListarCultivos
-- Devuelve el catálogo de cultivos ordenado por nombre.
-- Usado por: GET /api/cultivos
-- =============================================
IF OBJECT_ID('sp_ListarCultivos', 'P') IS NOT NULL
    DROP PROCEDURE sp_ListarCultivos;
GO

CREATE PROCEDURE sp_ListarCultivos
AS
BEGIN
    SET NOCOUNT ON;

    SELECT id_cultivo, nombre, descripcion
    FROM Cultivo
    ORDER BY nombre;
END;
GO

PRINT 'Procedimiento sp_ListarCultivos creado.';
GO

-- =============================================
-- PROCEDIMIENTO 2: sp_ListarRecomendaciones
-- Devuelve recomendaciones agrícolas con join a Cultivo.
-- Permite filtrar opcionalmente por id_cultivo.
-- Usado por: GET /api/recomendaciones[?id_cultivo=N]
-- =============================================
IF OBJECT_ID('sp_ListarRecomendaciones', 'P') IS NOT NULL
    DROP PROCEDURE sp_ListarRecomendaciones;
GO

CREATE PROCEDURE sp_ListarRecomendaciones
    @id_cultivo INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        R.id_recomendacion,
        C.nombre AS cultivo,
        R.condicion_climatica,
        R.nivel,
        R.mensaje
    FROM Recomendacion R
    INNER JOIN Cultivo C
        ON R.id_cultivo = C.id_cultivo
    WHERE @id_cultivo IS NULL
       OR R.id_cultivo = @id_cultivo
    ORDER BY C.nombre;
END;
GO

PRINT 'Procedimiento sp_ListarRecomendaciones creado.';
GO

-- =============================================
-- PROCEDIMIENTO 3: sp_RegistrarHistorial
-- Inserta un registro en la tabla Historial y
-- retorna el ID generado (SCOPE_IDENTITY).
-- Usado por: POST /api/historial
-- =============================================
IF OBJECT_ID('sp_RegistrarHistorial', 'P') IS NOT NULL
    DROP PROCEDURE sp_RegistrarHistorial;
GO

CREATE PROCEDURE sp_RegistrarHistorial
    @id_ubicacion        INT,
    @id_recomendacion    INT,
    @temperatura         DECIMAL(5,2),
    @probabilidad_lluvia DECIMAL(5,2),
    @precipitacion_mm    DECIMAL(7,2),
    @humedad             DECIMAL(5,2),
    @viento_kmh          DECIMAL(6,2)
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Historial (
        id_ubicacion,
        id_recomendacion,
        temperatura,
        probabilidad_lluvia,
        precipitacion_mm,
        humedad,
        viento_kmh
    )
    VALUES (
        @id_ubicacion,
        @id_recomendacion,
        @temperatura,
        @probabilidad_lluvia,
        @precipitacion_mm,
        @humedad,
        @viento_kmh
    );

    SELECT SCOPE_IDENTITY() AS id_historial;
END;
GO

PRINT 'Procedimiento sp_RegistrarHistorial creado.';
GO

-- =============================================
-- PROCEDIMIENTO 4: sp_ListarHistorial
-- Devuelve el historial de consultas con joins
-- a Ubicacion, Recomendacion y Cultivo.
-- Permite filtrar opcionalmente por id_ubicacion.
-- Usado por: GET /api/historial[?id_ubicacion=N]
-- =============================================
IF OBJECT_ID('sp_ListarHistorial', 'P') IS NOT NULL
    DROP PROCEDURE sp_ListarHistorial;
GO

CREATE PROCEDURE sp_ListarHistorial
    @id_ubicacion INT = NULL
AS
BEGIN
    SET NOCOUNT ON;

    SELECT
        H.id_historial,
        U.nombre          AS ubicacion,
        C.nombre          AS cultivo,
        R.nivel,
        R.mensaje,
        H.fecha_consulta,
        H.temperatura,
        H.probabilidad_lluvia,
        H.precipitacion_mm,
        H.humedad,
        H.viento_kmh
    FROM Historial H
    INNER JOIN Ubicacion U
        ON H.id_ubicacion = U.id_ubicacion
    INNER JOIN Recomendacion R
        ON H.id_recomendacion = R.id_recomendacion
    INNER JOIN Cultivo C
        ON R.id_cultivo = C.id_cultivo
    WHERE @id_ubicacion IS NULL
       OR H.id_ubicacion = @id_ubicacion
    ORDER BY H.fecha_consulta DESC;
END;
GO

PRINT 'Procedimiento sp_ListarHistorial creado.';
GO

PRINT '=== Script 04 completado. Los cuatro procedimientos almacenados están listos. ===';
GO
