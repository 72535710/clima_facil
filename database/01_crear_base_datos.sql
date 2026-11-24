-- =============================================
-- Clima Fácil — Script 01: Crear base de datos
-- =============================================
-- Uso: Ejecutar como administrador en SQL Server.
-- Crea la base de datos ClimaFacilDB si no existe.
-- NO modifica la base de datos original si ya existe.
-- Para una base temporal independiente, cambie ClimaFacilDB por el nombre
-- deseado en este archivo y en los scripts 02, 03 y 04 antes de ejecutar.
-- =============================================

USE master;
GO

IF NOT EXISTS (
    SELECT name FROM sys.databases WHERE name = N'ClimaFacilDB'
)
BEGIN
    CREATE DATABASE ClimaFacilDB;
    PRINT 'Base de datos ClimaFacilDB creada correctamente.';
END
ELSE
BEGIN
    PRINT 'La base de datos ClimaFacilDB ya existe. No se realiza ninguna acción.';
END
GO

USE ClimaFacilDB;
GO
