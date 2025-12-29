#!/usr/bin/env python3
"""Script de ayuda para probar la conexión a la BD y ejecutar la query de ejemplo.

Ejecutar desde la raíz del repo (usa `python3`):
  python3 scripts/test_db.py

El script imprimirá el resultado o el traceback completo para depuración.
Si quieres que imprima las credenciales para debug, exporta:
  export DEBUG_DB_CREDENTIALS=1
"""
import traceback
from dotenv import load_dotenv
import os

load_dotenv()

def main():
    try:
        # Si se habilita debug, imprimir credenciales (solo para debugging local)
        # Import y ejecución de la función de prueba
        from src.tools.database.product_tools import search_products_by_name
        rows = search_products_by_name('Leche', limit=5)
        print('OK - filas retornadas:', len(rows))
        for r in rows:
            print(r)
    except Exception:
        print('ERROR al ejecutar la prueba:')
        traceback.print_exc()


if __name__ == '__main__':
    main()
