from app.database import get_db_connection


def listar_cultivos_db() -> list[dict]:
    """Ejecuta sp_ListarCultivos sin ORM y devuelve la lista de cultivos."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("EXEC sp_ListarCultivos")
        rows = cursor.fetchall()
        return [
            {
                "id_cultivo": int(row[0]),
                "nombre": str(row[1]),
                "descripcion": str(row[2]) if row[2] is not None else "",
            }
            for row in rows
        ]


def listar_recomendaciones_db(id_cultivo: int | None = None) -> list[dict]:
    """Ejecuta sp_ListarRecomendaciones permitiendo filtro opcional por id_cultivo."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if id_cultivo is not None:
            cursor.execute("EXEC sp_ListarRecomendaciones @id_cultivo = ?", (id_cultivo,))
        else:
            cursor.execute("EXEC sp_ListarRecomendaciones")
        rows = cursor.fetchall()
        return [
            {
                "id_recomendacion": int(row[0]),
                "cultivo": str(row[1]),
                "condicion_climatica": str(row[2]),
                "nivel": str(row[3]),
                "mensaje": str(row[4]),
            }
            for row in rows
        ]


def listar_historial_db(id_ubicacion: int | None = None) -> list[dict]:
    """Ejecuta sp_ListarHistorial permitiendo filtro opcional por id_ubicacion."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        if id_ubicacion is not None:
            cursor.execute("EXEC sp_ListarHistorial @id_ubicacion = ?", (id_ubicacion,))
        else:
            cursor.execute("EXEC sp_ListarHistorial")
        rows = cursor.fetchall()
        return [
            {
                "id_historial": int(row[0]),
                "ubicacion": str(row[1]),
                "cultivo": str(row[2]),
                "nivel": str(row[3]),
                "mensaje": str(row[4]),
                "fecha_consulta": str(row[5]),
                "temperatura": float(row[6]),
                "probabilidad_lluvia": float(row[7]),
                "precipitacion_mm": float(row[8]),
                "humedad": float(row[9]),
                "viento_kmh": float(row[10]),
            }
            for row in rows
        ]


def registrar_historial_db(
    id_ubicacion: int,
    id_recomendacion: int,
    temperatura: float,
    probabilidad_lluvia: float,
    precipitacion_mm: float,
    humedad: float,
    viento_kmh: float,
) -> int:
    """Ejecuta sp_RegistrarHistorial e inserta un nuevo registro retornando el ID generado."""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            """
            EXEC sp_RegistrarHistorial 
                @id_ubicacion = ?,
                @id_recomendacion = ?,
                @temperatura = ?,
                @probabilidad_lluvia = ?,
                @precipitacion_mm = ?,
                @humedad = ?,
                @viento_kmh = ?
            """,
            (
                id_ubicacion,
                id_recomendacion,
                temperatura,
                probabilidad_lluvia,
                precipitacion_mm,
                humedad,
                viento_kmh,
            ),
        )
        row = cursor.fetchone()
        conn.commit()
        if row and row[0] is not None:
            return int(row[0])
        raise RuntimeError("No se pudo obtener el identificador del historial registrado.")
