import sys
import os

# Asegurar que el directorio backend está en el path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi.testclient import TestClient
from app.main import app
from app.database import test_db_connection
from app.services.db_service import (
    listar_cultivos_db,
    listar_recomendaciones_db,
    listar_historial_db,
    registrar_historial_db,
)
from app.services.open_meteo import (
    obtener_clima_actual_open_meteo,
    obtener_pronostico_open_meteo,
)
from app.services.weather_rules import evaluar_condiciones_meteorologicas


def test_suite():
    print("==================================================")
    print(" INICIANDO PRUEBAS DEL BACKEND CLIMA FACIL")
    print("==================================================")

    # 1. Conexión a la base de datos
    print("\n[1/7] Probando conexión a SQL Server (ClimaFacilDB)...")
    assert test_db_connection() is True, "La conexión a SQL Server falló."
    print(" -> Conexión a SQL Server: EXITOSA.")

    # 2. Servicios de base de datos
    print("\n[2/7] Probando procedimientos almacenados con pyodbc...")
    cultivos = listar_cultivos_db()
    print(f" -> sp_ListarCultivos retornó {len(cultivos)} cultivos: {[c['nombre'] for c in cultivos]}")
    assert len(cultivos) >= 3, "Deberían existir al menos 3 cultivos (Papa, Maiz, Haba)."

    recs = listar_recomendaciones_db()
    print(f" -> sp_ListarRecomendaciones (sin filtro) retornó {len(recs)} recomendaciones.")
    assert len(recs) > 0

    recs_papa = listar_recomendaciones_db(id_cultivo=1)
    print(f" -> sp_ListarRecomendaciones (id_cultivo=1) retornó {len(recs_papa)} recomendaciones para Papa.")
    assert all(r["cultivo"] == "Papa" for r in recs_papa)

    historial = listar_historial_db()
    print(f" -> sp_ListarHistorial retornó {len(historial)} registros históricos.")

    # Prueba de inserción
    nuevo_id = registrar_historial_db(
        id_ubicacion=1,
        id_recomendacion=1,
        temperatura=16.5,
        probabilidad_lluvia=40.0,
        precipitacion_mm=1.5,
        humedad=65.0,
        viento_kmh=10.0,
    )
    print(f" -> sp_RegistrarHistorial insertó registro con ID: {nuevo_id}")
    assert nuevo_id > 0

    # 3. Reglas de recomendaciones
    print("\n[3/7] Probando lógica y umbrales de condiciones meteorológicas...")
    cond_frio = evaluar_condiciones_meteorologicas(temperatura=3.0, probabilidad_lluvia=10.0, precipitacion_mm=0.0)
    print(f" -> Evaluación 3°C: {cond_frio} (Esperado 'helada_probable')")
    assert "helada_probable" in cond_frio

    cond_lluvia = evaluar_condiciones_meteorologicas(temperatura=15.0, probabilidad_lluvia=80.0, precipitacion_mm=8.0)
    print(f" -> Evaluación lluvia 80%/8mm: {cond_lluvia} (Esperado 'lluvia_alta')")
    assert "lluvia_alta" in cond_lluvia

    cond_calor = evaluar_condiciones_meteorologicas(temperatura=23.5, probabilidad_lluvia=10.0, precipitacion_mm=0.0)
    print(f" -> Evaluación calor 23.5°C: {cond_calor} (Esperado 'calor_intenso')")
    assert "calor_intenso" in cond_calor

    # 4. Endpoints con TestClient
    print("\n[4/7] Probando Endpoints HTTP de FastAPI con TestClient...")
    with TestClient(app) as client:
        # GET /
        r_root = client.get("/")
        assert r_root.status_code == 200, f"GET / falló: {r_root.text}"
        print(f" -> GET /: OK (200) -> {r_root.json().get('proyecto')}")

        # GET /api/cultivos
        r_cultivos = client.get("/api/cultivos")
        assert r_cultivos.status_code == 200, f"GET /api/cultivos falló: {r_cultivos.text}"
        data_cultivos = r_cultivos.json()
        print(f" -> GET /api/cultivos: OK (200), {len(data_cultivos)} registros.")

        # GET /api/recomendaciones
        r_recs = client.get("/api/recomendaciones")
        assert r_recs.status_code == 200
        print(f" -> GET /api/recomendaciones: OK (200), {len(r_recs.json())} registros.")

        # GET /api/recomendaciones?id_cultivo=2
        r_recs_maiz = client.get("/api/recomendaciones?id_cultivo=2")
        assert r_recs_maiz.status_code == 200
        print(f" -> GET /api/recomendaciones?id_cultivo=2: OK (200), {len(r_recs_maiz.json())} registros.")

        # GET /api/historial
        r_hist = client.get("/api/historial")
        assert r_hist.status_code == 200
        print(f" -> GET /api/historial: OK (200), {len(r_hist.json())} registros.")

        # POST /api/historial
        payload = {
            "id_ubicacion": 1,
            "id_recomendacion": 2,
            "temperatura": 14.8,
            "probabilidad_lluvia": 35.0,
            "precipitacion_mm": 0.5,
            "humedad": 70.0,
            "viento_kmh": 8.5,
        }
        r_post = client.post("/api/historial", json=payload)
        assert r_post.status_code == 201, f"POST /api/historial falló: {r_post.text}"
        print(f" -> POST /api/historial: OK (201) -> {r_post.json()}")

        # GET /api/clima/actual (Open-Meteo)
        print("\n[5/7] Probando GET /api/clima/actual (llamada real a Open-Meteo)...")
        r_actual = client.get("/api/clima/actual")
        assert r_actual.status_code == 200, f"GET /api/clima/actual falló: {r_actual.text}"
        clima_data = r_actual.json()
        print(f" -> GET /api/clima/actual: OK (200)")
        print(f"    Temperatura: {clima_data['temperatura']}°C, Humedad: {clima_data['humedad']}%, "
              f"Lluvia: {clima_data['probabilidad_lluvia']}%, Viento: {clima_data['viento']} km/h, "
              f"Descripción: '{clima_data['descripcion']}'")

        # GET /api/clima/pronostico (Open-Meteo)
        print("\n[6/7] Probando GET /api/clima/pronostico (llamada real a Open-Meteo)...")
        r_pron = client.get("/api/clima/pronostico")
        assert r_pron.status_code == 200, f"GET /api/clima/pronostico falló: {r_pron.text}"
        pron_data = r_pron.json()
        print(f" -> GET /api/clima/pronostico: OK (200), {len(pron_data)} días pronosticados.")
        for d in pron_data[:3]:
            print(f"    {d['dia_semana']} ({d['fecha']}): Máx {d['temperatura_maxima']}°C, "
                  f"Mín {d['temperatura_minima']}°C, Lluvia {d['probabilidad_lluvia']}%, '{d['descripcion']}'")

        # Swagger Docs
        print("\n[7/7] Probando disponibilidad de documentación Swagger...")
        r_docs = client.get("/docs")
        assert r_docs.status_code == 200
        print(" -> Swagger UI (/docs): OK (200)")

    print("\n==================================================")
    print(" TODAS LAS PRUEBAS COMPLETADAS CON ÉXITO")
    print("==================================================")


if __name__ == "__main__":
    test_suite()
