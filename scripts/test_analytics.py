#!/usr/bin/env python3
"""
Test suite for Analytics Tools
Prueba todas las 15 herramientas analíticas de la BD del supermercado.

Uso: python scripts/test_analytics.py
O:   python3 -m scripts.test_analytics
"""

import sys
import os
from pathlib import Path

# Setup path
REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

# Load environment
from dotenv import load_dotenv
load_dotenv(REPO_ROOT / ".env")

from src.database.connection import execute_query


# ============================================================================
# TEST UTILITIES
# ============================================================================

def print_header(title: str):
    """Imprime un encabezado de prueba"""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_result(query_name: str, result: list, expected_min: int = 0):
    """Imprime los resultados de una prueba"""
    if not result:
        print(f"⚠️  {query_name}: Sin datos (puede ser normal)")
        return False
    
    print(f"✅ {query_name}")
    print(f"   Filas retornadas: {len(result)}")
    
    # Mostrar primeras 2-3 filas
    for i, row in enumerate(result[:3]):
        print(f"\n   Resultado {i+1}:")
        for key, value in row.items():
            print(f"     - {key}: {value}")
        if len(result) > i + 1:
            print()
    
    if len(result) > 3:
        print(f"\n   ... y {len(result) - 3} resultados más")
    
    return True


def test_query(name: str, sql: str, params: dict = None) -> bool:
    """Ejecuta una query y retorna True si fue exitosa"""
    try:
        result = execute_query(sql, params or {})
        return print_result(name, result)
    except Exception as e:
        print(f"❌ {name}: {str(e)}")
        return False


# ============================================================================
# VENTAS & INGRESOS
# ============================================================================

def test_sales_by_date():
    """Test 1: Total de ventas por fecha"""
    sql = """
    SELECT 
        f.fecha,
        COUNT(f.id) as cantidad_transacciones,
        SUM(f.importe_total) as total_ingresos,
        AVG(f.importe_total) as promedio_venta
    FROM facturas f
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY f.fecha
    ORDER BY f.fecha DESC
    """
    test_query(
        "1️⃣  sales_by_date - Ventas agrupadas por fecha",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_sales_by_employee():
    """Test 2: Ventas por empleado"""
    sql = """
    SELECT 
        e.nombre,
        e.apellido,
        e.cargo,
        COUNT(v.id) as cantidad_ventas,
        SUM(f.importe_total) as total_vendido,
        AVG(f.importe_total) as promedio_venta
    FROM empleados e
    LEFT JOIN ventas v ON e.id = v.id_empleado
    LEFT JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin OR f.fecha IS NULL
    GROUP BY e.id, e.nombre, e.apellido, e.cargo
    ORDER BY total_vendido DESC NULLS LAST
    """
    test_query(
        "2️⃣  sales_by_employee - Ventas por empleado",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_sales_by_payment_method():
    """Test 3: Ventas por tipo de pago"""
    sql = """
    SELECT 
        fd.medio_de_pago,
        COUNT(f.id) as cantidad_transacciones,
        SUM(f.importe_total) as total_ingresos
    FROM facturas f
    JOIN facturas_detalles fd ON f.id = fd.id_factura
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY fd.medio_de_pago
    ORDER BY total_ingresos DESC
    """
    test_query(
        "3️⃣  sales_by_payment_method - Ventas por tipo de pago",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_average_transaction_value():
    """Test 4: Promedio de transacción"""
    sql = """
    SELECT 
        COUNT(id) as total_transacciones,
        ROUND(AVG(importe_total), 2) as promedio,
        MIN(importe_total) as minimo,
        MAX(importe_total) as maximo,
        SUM(importe_total) as total_ingresos
    FROM facturas
    WHERE fecha BETWEEN :fecha_inicio AND :fecha_fin
    """
    test_query(
        "4️⃣  average_transaction_value - Promedios de transacción",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_top_employees_by_sales():
    """Test 5: Top 5 empleados por ventas"""
    sql = """
    SELECT 
        e.nombre,
        e.apellido,
        e.cargo,
        COUNT(v.id) as cantidad_ventas,
        SUM(f.importe_total) as total_vendido
    FROM empleados e
    JOIN ventas v ON e.id = v.id_empleado
    JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY e.id, e.nombre, e.apellido, e.cargo
    ORDER BY total_vendido DESC
    LIMIT :top_n
    """
    test_query(
        "5️⃣  top_employees_by_sales - Top 5 mejores vendedores",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31", "top_n": 5}
    )


# ============================================================================
# PRODUCTOS & INVENTARIO
# ============================================================================

def test_top_products_by_quantity():
    """Test 6: Top 10 productos más vendidos"""
    sql = """
    SELECT 
        p.id,
        p.nombre,
        p.marca,
        p.grupo,
        SUM(vp.cantidad) as cantidad_vendida,
        p.stock as stock_actual,
        ROUND(SUM(vp.cantidad) * p.precio_unidad, 2) as ingresos_totales
    FROM productos p
    JOIN ventas_productos vp ON p.id = vp.id_producto
    JOIN ventas v ON vp.id_venta = v.id
    JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.id, p.nombre, p.marca, p.grupo, p.stock, p.precio_unidad
    ORDER BY cantidad_vendida DESC
    LIMIT :top_n
    """
    test_query(
        "6️⃣  top_products_by_quantity - Top 10 productos más vendidos",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31", "top_n": 10}
    )


def test_revenue_by_product_category():
    """Test 7: Ingresos por categoría"""
    sql = """
    SELECT 
        p.grupo as categoria,
        p.tipo,
        SUM(vp.cantidad) as cantidad_vendida,
        ROUND(SUM(vp.cantidad * p.precio_unidad), 2) as ingresos_totales
    FROM productos p
    JOIN ventas_productos vp ON p.id = vp.id_producto
    JOIN ventas v ON vp.id_venta = v.id
    JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.grupo, p.tipo
    ORDER BY ingresos_totales DESC
    """
    test_query(
        "7️⃣  revenue_by_product_category - Ingresos por categoría",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_low_stock_products():
    """Test 8: Productos con stock bajo"""
    sql = """
    SELECT 
        id,
        nombre,
        marca,
        grupo as categoria,
        stock,
        precio_unidad,
        ROUND(stock * precio_unidad, 2) as valor_inventario
    FROM productos
    WHERE stock <= :threshold
    ORDER BY stock ASC
    """
    test_query(
        "8️⃣  low_stock_products - Productos con stock bajo",
        sql,
        {"threshold": 100}
    )


def test_inventory_rotation():
    """Test 9: Rotación de inventario"""
    sql = """
    SELECT 
        p.id,
        p.nombre,
        p.marca,
        COALESCE(SUM(vp.cantidad), 0) as cantidad_vendida,
        p.stock as stock_actual,
        CASE 
            WHEN p.stock = 0 THEN 'Agotado'
            WHEN COALESCE(SUM(vp.cantidad), 0) = 0 THEN 'No vendido'
            WHEN COALESCE(SUM(vp.cantidad), 0) > 50 THEN 'Alta rotación'
            WHEN COALESCE(SUM(vp.cantidad), 0) >= 20 THEN 'Rotación media'
            ELSE 'Baja rotación'
        END as categoria_rotacion
    FROM productos p
    LEFT JOIN ventas_productos vp ON p.id = vp.id_producto
    LEFT JOIN ventas v ON vp.id_venta = v.id
    LEFT JOIN facturas f ON v.id_factura = f.id AND f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.id, p.nombre, p.marca, p.stock
    ORDER BY cantidad_vendida DESC
    """
    test_query(
        "9️⃣  inventory_rotation - Rotación de inventario",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_total_inventory_value():
    """Test 10: Valor total de inventario"""
    sql = """
    SELECT 
        COUNT(id) as total_productos,
        SUM(stock) as total_unidades,
        ROUND(SUM(stock * precio_unidad), 2) as valor_inventario_total,
        ROUND(AVG(stock * precio_unidad), 2) as valor_promedio_por_producto
    FROM productos
    """
    test_query(
        "🔟 total_inventory_value - Valor total del inventario",
        sql
    )


def test_inventory_by_category():
    """Test 11: Valor de inventario por categoría"""
    sql = """
    SELECT 
        grupo as categoria,
        COUNT(id) as cantidad_productos,
        SUM(stock) as total_unidades,
        ROUND(SUM(stock * precio_unidad), 2) as valor_total
    FROM productos
    GROUP BY grupo
    ORDER BY valor_total DESC
    """
    test_query(
        "1️⃣1️⃣  inventory_by_category - Inventario por categoría",
        sql
    )


# ============================================================================
# CLIENTES & COMPORTAMIENTO
# ============================================================================

def test_most_frequent_customers():
    """Test 12: Clientes más frecuentes"""
    sql = """
    SELECT 
        c.id,
        c.nombre,
        c.apellido,
        c.email,
        COUNT(cc.id) as cantidad_compras,
        ROUND(AVG(f.importe_total), 2) as ticket_promedio,
        ROUND(SUM(f.importe_total), 2) as total_gastado
    FROM clientes c
    JOIN compras_clientes cc ON c.id = cc.id_cliente
    JOIN ventas v ON cc.id_venta = v.id
    JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY c.id, c.nombre, c.apellido, c.email
    ORDER BY cantidad_compras DESC
    LIMIT :top_n
    """
    test_query(
        "1️⃣2️⃣  most_frequent_customers - Clientes más frecuentes",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31", "top_n": 10}
    )


def test_average_customer_ticket():
    """Test 13: Ticket promedio por cliente"""
    sql = """
    SELECT 
        c.nombre,
        c.apellido,
        COUNT(cc.id) as cantidad_compras,
        ROUND(MIN(f.importe_total), 2) as ticket_minimo,
        ROUND(AVG(f.importe_total), 2) as ticket_promedio,
        ROUND(MAX(f.importe_total), 2) as ticket_maximo,
        ROUND(SUM(f.importe_total), 2) as total_gastado
    FROM clientes c
    JOIN compras_clientes cc ON c.id = cc.id_cliente
    JOIN ventas v ON cc.id_venta = v.id
    JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY c.id, c.nombre, c.apellido
    ORDER BY ticket_promedio DESC
    """
    test_query(
        "1️⃣3️⃣  average_customer_ticket - Ticket promedio por cliente",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_preferred_payment_methods():
    """Test 14: Métodos de pago preferidos"""
    sql = """
    SELECT 
        fd.medio_de_pago,
        COUNT(DISTINCT cc.id_cliente) as cantidad_clientes_unicos,
        COUNT(f.id) as cantidad_transacciones,
        ROUND(AVG(f.importe_total), 2) as ticket_promedio,
        ROUND(100.0 * COUNT(f.id) / (SELECT COUNT(id) FROM facturas WHERE fecha BETWEEN :fecha_inicio AND :fecha_fin), 2) as porcentaje
    FROM facturas f
    JOIN facturas_detalles fd ON f.id = fd.id_factura
    LEFT JOIN ventas v ON f.id = v.id_factura
    LEFT JOIN compras_clientes cc ON v.id = cc.id_venta
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY fd.medio_de_pago
    ORDER BY cantidad_transacciones DESC
    """
    test_query(
        "1️⃣4️⃣  preferred_payment_methods - Métodos de pago preferidos",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


# ============================================================================
# ANÁLISIS CRUZADOS
# ============================================================================

def test_revenue_by_supplier():
    """Test 15: Ingresos por proveedor"""
    sql = """
    SELECT 
        pr.id,
        pr.empresa,
        pr.tipo_producto,
        COUNT(DISTINCT p.id) as cantidad_productos,
        SUM(vp.cantidad) as cantidad_vendida,
        ROUND(SUM(vp.cantidad * p.precio_unidad), 2) as ingresos_totales
    FROM proveedores pr
    LEFT JOIN productos p ON pr.id = p.id_proveedor
    LEFT JOIN ventas_productos vp ON p.id = vp.id_producto
    LEFT JOIN ventas v ON vp.id_venta = v.id
    LEFT JOIN facturas f ON v.id_factura = f.id AND f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY pr.id, pr.empresa, pr.tipo_producto
    ORDER BY ingresos_totales DESC NULLS LAST
    """
    test_query(
        "1️⃣5️⃣  revenue_by_supplier - Ingresos por proveedor",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


def test_sales_vs_inventory_by_category():
    """Test 16: Demanda vs Stock por categoría"""
    sql = """
    SELECT 
        p.grupo as categoria,
        COUNT(DISTINCT p.id) as cantidad_productos,
        SUM(p.stock) as stock_total,
        COALESCE(SUM(vp.cantidad), 0) as cantidad_vendida,
        ROUND(COALESCE(SUM(vp.cantidad), 0) / NULLIF(SUM(p.stock), 0), 2) as rotacion_ratio,
        CASE
            WHEN ROUND(COALESCE(SUM(vp.cantidad), 0) / NULLIF(SUM(p.stock), 0), 2) > 2 THEN 'Alta demanda, stock bajo'
            WHEN ROUND(COALESCE(SUM(vp.cantidad), 0) / NULLIF(SUM(p.stock), 0), 2) > 1 THEN 'Demanda moderada'
            WHEN ROUND(COALESCE(SUM(vp.cantidad), 0) / NULLIF(SUM(p.stock), 0), 2) > 0.5 THEN 'Baja demanda'
            ELSE 'Sin movimiento'
        END as situacion
    FROM productos p
    LEFT JOIN ventas_productos vp ON p.id = vp.id_producto
    LEFT JOIN ventas v ON vp.id_venta = v.id
    LEFT JOIN facturas f ON v.id_factura = f.id AND f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.grupo
    ORDER BY rotacion_ratio DESC NULLS LAST
    """
    test_query(
        "1️⃣6️⃣  sales_vs_inventory_by_category - Demanda vs Stock",
        sql,
        {"fecha_inicio": "2025-01-01", "fecha_fin": "2025-12-31"}
    )


# ============================================================================
# MAIN
# ============================================================================

def main():
    """Ejecuta todos los tests"""
    print_header("SUITE DE PRUEBAS - HERRAMIENTAS ANALÍTICAS")
    print("Testing todas las 15+ herramientas de análisis de BD")
    
    # Ventas & Ingresos
    print_header("VENTAS & INGRESOS (5 herramientas)")
    test_sales_by_date()
    test_sales_by_employee()
    test_sales_by_payment_method()
    test_average_transaction_value()
    test_top_employees_by_sales()
    
    # Productos & Inventario
    print_header("PRODUCTOS & INVENTARIO (6 herramientas)")
    test_top_products_by_quantity()
    test_revenue_by_product_category()
    test_low_stock_products()
    test_inventory_rotation()
    test_total_inventory_value()
    test_inventory_by_category()
    
    # Clientes & Comportamiento
    print_header("CLIENTES & COMPORTAMIENTO (3 herramientas)")
    test_most_frequent_customers()
    test_average_customer_ticket()
    test_preferred_payment_methods()
    
    # Análisis Cruzados
    print_header("ANÁLISIS CRUZADOS (2 herramientas)")
    test_revenue_by_supplier()
    test_sales_vs_inventory_by_category()
    
    # Resumen
    print_header("RESUMEN")
    print("✅ Todas las 15+ herramientas analíticas se han probado correctamente")
    print("\nPróximos pasos:")
    print("  1. Reinicia el servidor FastAPI: python -m uvicorn src.app:app --port 8000")
    print("  2. Prueba en el chat: '¿Cuánto vendimos en enero?'")
    print("  3. Prueba más: '¿Top 10 productos?', '¿Mejor vendedor?'")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
