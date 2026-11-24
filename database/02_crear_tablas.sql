-- =============================================
-- Clima Fácil — Script 02: Crear tablas
-- =============================================
-- Prerequisito: haber ejecutado 01_crear_base_datos.sql
-- Crea las cuatro tablas con sus relaciones, restricciones
-- y constraints exactamente como existen en ClimaFacilDB.
-- Idempotente: no falla si las tablas ya existen.
-- =============================================

USE ClimaFacilDB;
GO

-- =============================================
-- TABLA 1: Ubicacion
-- Almacena las zonas geográficas de consulta.
-- (Actualmente solo Huancayo, Valle del Mantaro)
-- =============================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Ubicacion')
BEGIN
    CREATE TABLE Ubicacion (
        id_ubicacion INT          IDENTITY(1,1) NOT NULL,
        nombre       NVARCHAR(100) NOT NULL,
        latitud      DECIMAL(9,6)  NOT NULL,
        longitud     DECIMAL(9,6)  NOT NULL,

        CONSTRAINT PK_Ubicacion PRIMARY KEY (id_ubicacion),
        CONSTRAINT UQ_Ubicacion_Nombre UNIQUE (nombre),
        CONSTRAINT CK_Ubicacion_Latitud  CHECK (latitud  >= -90  AND latitud  <= 90),
        CONSTRAINT CK_Ubicacion_Longitud CHECK (longitud >= -180 AND longitud <= 180)
    );
    PRINT 'Tabla Ubicacion creada.';
END
ELSE
    PRINT 'Tabla Ubicacion ya existe.';
GO

-- =============================================
-- TABLA 2: Cultivo
-- Catálogo de cultivos del Valle del Mantaro.
-- =============================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Cultivo')
BEGIN
    CREATE TABLE Cultivo (
        id_cultivo  INT           IDENTITY(1,1) NOT NULL,
        nombre      NVARCHAR(80)  NOT NULL,
        descripcion NVARCHAR(300) NOT NULL,

        CONSTRAINT PK_Cultivo PRIMARY KEY (id_cultivo),
        CONSTRAINT UQ_Cultivo_Nombre UNIQUE (nombre)
    );
    PRINT 'Tabla Cultivo creada.';
END
ELSE
    PRINT 'Tabla Cultivo ya existe.';
GO

-- =============================================
-- TABLA 3: Recomendacion
-- Consejos agrícolas según condición climática.
-- Referencia a Cultivo mediante FK.
-- =============================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Recomendacion')
BEGIN
    CREATE TABLE Recomendacion (
        id_recomendacion    INT           IDENTITY(1,1) NOT NULL,
        id_cultivo          INT           NOT NULL,
        condicion_climatica NVARCHAR(50)  NOT NULL,
        nivel               NVARCHAR(20)  NOT NULL,
        mensaje             NVARCHAR(500) NOT NULL,

        CONSTRAINT PK_Recomendacion PRIMARY KEY (id_recomendacion),
        CONSTRAINT FK_Recomendacion_Cultivo FOREIGN KEY (id_cultivo)
            REFERENCES Cultivo (id_cultivo),
        CONSTRAINT UQ_Recomendacion UNIQUE (id_cultivo, condicion_climatica, nivel),
        CONSTRAINT CK_Recomendacion_Nivel CHECK (
            nivel = 'Precaucion' OR nivel = 'Importante' OR nivel = 'Informativo'
        )
    );
    PRINT 'Tabla Recomendacion creada.';
END
ELSE
    PRINT 'Tabla Recomendacion ya existe.';
GO

-- =============================================
-- TABLA 4: Historial
-- Registro de consultas realizadas por los
-- agricultores, con métricas climáticas reales.
-- Referencia a Ubicacion y Recomendacion.
-- =============================================
IF NOT EXISTS (SELECT 1 FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = 'Historial')
BEGIN
    CREATE TABLE Historial (
        id_historial        INT           IDENTITY(1,1) NOT NULL,
        id_ubicacion        INT           NOT NULL,
        id_recomendacion    INT           NOT NULL,
        fecha_consulta      DATETIME2     NOT NULL CONSTRAINT DF_Historial_Fecha DEFAULT (sysdatetime()),
        temperatura         DECIMAL(5,2)  NOT NULL,
        probabilidad_lluvia DECIMAL(5,2)  NOT NULL,
        precipitacion_mm    DECIMAL(7,2)  NOT NULL,
        humedad             DECIMAL(5,2)  NOT NULL,
        viento_kmh          DECIMAL(6,2)  NOT NULL,

        CONSTRAINT PK_Historial PRIMARY KEY (id_historial),
        CONSTRAINT FK_Historial_Ubicacion     FOREIGN KEY (id_ubicacion)
            REFERENCES Ubicacion (id_ubicacion),
        CONSTRAINT FK_Historial_Recomendacion FOREIGN KEY (id_recomendacion)
            REFERENCES Recomendacion (id_recomendacion),
        CONSTRAINT CK_Historial_Temperatura   CHECK (temperatura         >= -80  AND temperatura         <= 60),
        CONSTRAINT CK_Historial_Lluvia        CHECK (probabilidad_lluvia >= 0    AND probabilidad_lluvia <= 100),
        CONSTRAINT CK_Historial_Humedad       CHECK (humedad             >= 0    AND humedad             <= 100),
        CONSTRAINT CK_Historial_Precipitacion CHECK (precipitacion_mm    >= 0),
        CONSTRAINT CK_Historial_Viento        CHECK (viento_kmh          >= 0)
    );
    PRINT 'Tabla Historial creada.';
END
ELSE
    PRINT 'Tabla Historial ya existe.';
GO
