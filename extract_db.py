"""
Script para extraer la estructura completa de ClimaFacilDB desde SQL Server.
Genera los cuatro archivos SQL de reconstrucción.
"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend'))

from app.database import get_db_connection

def q(conn, sql):
    cur = conn.cursor()
    cur.execute(sql)
    return cur.fetchall()

with get_db_connection() as conn:
    # 1. Tablas
    tablas = q(conn, "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE' AND TABLE_CATALOG='ClimaFacilDB' ORDER BY TABLE_NAME")
    print("TABLAS:", [r[0] for r in tablas])

    # 2. Columnas por tabla
    for tabla in [r[0] for r in tablas]:
        cols = q(conn, f"""
            SELECT c.COLUMN_NAME, c.DATA_TYPE, c.CHARACTER_MAXIMUM_LENGTH,
                   c.NUMERIC_PRECISION, c.NUMERIC_SCALE, c.IS_NULLABLE,
                   c.COLUMN_DEFAULT,
                   COLUMNPROPERTY(OBJECT_ID('{tabla}'), c.COLUMN_NAME, 'IsIdentity') as is_identity
            FROM INFORMATION_SCHEMA.COLUMNS c
            WHERE c.TABLE_NAME = '{tabla}'
            ORDER BY c.ORDINAL_POSITION
        """)
        print(f"\n--- {tabla} ---")
        for c in cols:
            print(f"  {c[0]} | {c[1]}({c[2] or c[3]}) | NULL={c[5]} | DEFAULT={c[6]} | IDENTITY={c[7]}")

    # 3. PKs y FKs
    print("\n=== PRIMARY KEYS ===")
    pks = q(conn, """
        SELECT kcu.TABLE_NAME, kcu.COLUMN_NAME, tc.CONSTRAINT_NAME
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
        JOIN INFORMATION_SCHEMA.KEY_COLUMN_USAGE kcu
            ON tc.CONSTRAINT_NAME = kcu.CONSTRAINT_NAME
        WHERE tc.CONSTRAINT_TYPE = 'PRIMARY KEY' AND tc.TABLE_CATALOG = 'ClimaFacilDB'
        ORDER BY kcu.TABLE_NAME
    """)
    for r in pks:
        print(f"  {r[0]}.{r[1]} ({r[2]})")

    print("\n=== FOREIGN KEYS ===")
    fks = q(conn, """
        SELECT
            fk.name AS fk_name,
            tp.name AS parent_table, cp.name AS parent_col,
            tr.name AS ref_table, cr.name AS ref_col
        FROM sys.foreign_keys fk
        JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
        JOIN sys.tables tp ON fkc.parent_object_id = tp.object_id
        JOIN sys.columns cp ON fkc.parent_object_id = cp.object_id AND fkc.parent_column_id = cp.column_id
        JOIN sys.tables tr ON fkc.referenced_object_id = tr.object_id
        JOIN sys.columns cr ON fkc.referenced_object_id = cr.object_id AND fkc.referenced_column_id = cr.column_id
        ORDER BY tp.name
    """)
    for r in fks:
        print(f"  {r[0]}: {r[1]}.{r[2]} -> {r[3]}.{r[4]}")

    # 4. Datos actuales
    print("\n=== DATOS ===")
    for tabla in [r[0] for r in tablas]:
        rows = q(conn, f"SELECT * FROM {tabla}")
        print(f"\n{tabla} ({len(rows)} filas):")
        for row in rows:
            print(f"  {list(row)}")

    # 5. Procedimientos almacenados
    print("\n=== PROCEDIMIENTOS ===")
    procs = q(conn, "SELECT name FROM sys.procedures ORDER BY name")
    print("PROCS:", [r[0] for r in procs])
    for proc in [r[0] for r in procs]:
        texto = q(conn, f"SELECT OBJECT_DEFINITION(OBJECT_ID('{proc}'))")
        print(f"\n--- {proc} ---")
        print(texto[0][0] if texto and texto[0][0] else "SIN DEFINICION")

    # 6. Constraints adicionales (CHECK, UNIQUE)
    print("\n=== CONSTRAINTS ===")
    checks = q(conn, """
        SELECT tc.TABLE_NAME, tc.CONSTRAINT_NAME, tc.CONSTRAINT_TYPE, cc.CHECK_CLAUSE
        FROM INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
        LEFT JOIN INFORMATION_SCHEMA.CHECK_CONSTRAINTS cc
            ON tc.CONSTRAINT_NAME = cc.CONSTRAINT_NAME
        WHERE tc.TABLE_CATALOG = 'ClimaFacilDB'
            AND tc.CONSTRAINT_TYPE IN ('CHECK','UNIQUE')
        ORDER BY tc.TABLE_NAME
    """)
    for r in checks:
        print(f"  {r[0]} | {r[1]} | {r[2]} | {r[3]}")
