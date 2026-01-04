"""Analytics tools for sales, inventory, and customer insights.

These tools use the project's DB connection helper to execute analytics queries.
All tools support optional date ranges (fecha_inicio, fecha_fin).
"""
from typing import List
from langchain_core.tools import tool
from src.database.connection import execute_query


# ============================================================================
# VENTAS & INGRESOS
# ============================================================================

@tool
def sales_by_date(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Total de ventas agrupadas por fecha.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD' (default: 2025-01-01)
      - fecha_fin: formato 'YYYY-MM-DD' (default: 2026-12-31)
    Retorna: fecha, cantidad de transacciones, total de ingresos
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def sales_by_employee(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Total de ventas por empleado (cajero/repositor).
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    Retorna: nombre del empleado, cargo, cantidad de ventas, total de ingresos
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def sales_by_payment_method(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Ingresos por tipo de pago (Efectivo, Tarjeta Crédito, Tarjeta Débito, Cheque).
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    Retorna: método de pago, cantidad de transacciones, total de ingresos
    """
    sql = """
    SELECT 
        fd.medio_de_pago,
        COUNT(f.id) as cantidad_transacciones,
        SUM(f.importe_total) as total_ingresos,
        ROUND(100.0 * SUM(f.importe_total) / (SELECT SUM(importe_total) FROM facturas WHERE fecha BETWEEN :fecha_inicio AND :fecha_fin), 2) as porcentaje
    FROM facturas f
    JOIN facturas_detalles fd ON f.id = fd.id_factura
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY fd.medio_de_pago
    ORDER BY total_ingresos DESC
    """
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def average_transaction_value(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Promedio, mínimo, máximo de valor de transacción.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def top_employees_by_sales(top_n: int = 5, fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Top N empleados con más ingresos generados.
    Parámetros:
      - top_n: número de empleados (default 5)
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "top_n": top_n})


# ============================================================================
# PRODUCTOS & INVENTARIO
# ============================================================================

@tool
def top_products_by_quantity(top_n: int = 10, fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Top N productos más vendidos (por cantidad de unidades).
    Parámetros:
      - top_n: número de productos (default 10)
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
    sql = """
    SELECT 
        p.id,
        p.nombre,
        p.marca,
        p.grupo,
        COALESCE(SUM(vp.cantidad), 0) as cantidad_vendida,
        p.stock as stock_actual,
        p.precio_unidad,
        ROUND(COALESCE(SUM(vp.cantidad), 0) * p.precio_unidad, 2) as ingresos_totales
    FROM productos p
    LEFT JOIN ventas_productos vp ON p.id = vp.id_producto
    LEFT JOIN ventas v ON vp.id_venta = v.id
    LEFT JOIN facturas f ON v.id_factura = f.id AND f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.id, p.nombre, p.marca, p.grupo, p.stock, p.precio_unidad
    ORDER BY cantidad_vendida DESC, p.nombre ASC
    LIMIT :top_n
    """
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "top_n": top_n})


@tool
def revenue_by_product_category(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Ingresos totales por categoría (grupo) de productos.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    Retorna: categoría, cantidad vendida, ingresos totales, porcentaje
    """
    sql = """
    SELECT 
        p.grupo as categoria,
        p.tipo,
        SUM(vp.cantidad) as cantidad_vendida,
        ROUND(SUM(vp.cantidad * p.precio_unidad), 2) as ingresos_totales,
        ROUND(100.0 * SUM(vp.cantidad * p.precio_unidad) / 
            (SELECT SUM(vp2.cantidad * p2.precio_unidad) 
             FROM ventas_productos vp2 
             JOIN productos p2 ON vp2.id_producto = p2.id
             JOIN ventas v2 ON vp2.id_venta = v2.id
             JOIN facturas f2 ON v2.id_factura = f2.id
             WHERE f2.fecha BETWEEN :fecha_inicio AND :fecha_fin), 2) as porcentaje
    FROM productos p
    JOIN ventas_productos vp ON p.id = vp.id_producto
    JOIN ventas v ON vp.id_venta = v.id
    JOIN facturas f ON v.id_factura = f.id
    WHERE f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY p.grupo, p.tipo
    ORDER BY ingresos_totales DESC
    """
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def low_stock_products(threshold: int = 100) -> List[dict]:
    """
    Productos con stock bajo (por debajo del umbral).
    Parámetro:
      - threshold: nivel mínimo de stock (default 100)
    Retorna: nombre, marca, categoría, stock actual, precio
    """
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
    return execute_query(sql, {"threshold": threshold})


@tool
def inventory_rotation(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Rotación de inventario: qué productos se venden rápido vs lento.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def total_inventory_value() -> List[dict]:
    """
    Valor total del inventario (stock * precio unitario).
    Retorna: valor total, cantidad total de productos, valor promedio por producto
    """
    sql = """
    SELECT 
        COUNT(id) as total_productos,
        SUM(stock) as total_unidades,
        ROUND(SUM(stock * precio_unidad), 2) as valor_inventario_total,
        ROUND(AVG(stock * precio_unidad), 2) as valor_promedio_por_producto
    FROM productos
    """
    return execute_query(sql, {})


@tool
def inventory_by_category() -> List[dict]:
    """
    Valor de inventario agrupado por categoría (grupo).
    Retorna: categoría, cantidad de productos, unidades totales, valor total
    """
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
    return execute_query(sql, {})


# ============================================================================
# CLIENTES & COMPORTAMIENTO
# ============================================================================

@tool
def most_frequent_customers(top_n: int = 10, fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Clientes más frecuentes (más compras).
    Parámetros:
      - top_n: número de clientes (default 10)
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin, "top_n": top_n})


@tool
def average_customer_ticket(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Ticket promedio por cliente.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def preferred_payment_methods(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Métodos de pago preferidos por los clientes.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


# ============================================================================
# ANÁLISIS CRUZADOS
# ============================================================================

@tool
def revenue_by_supplier(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Ingresos generados por los productos de cada proveedor.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
    sql = """
    SELECT 
        pr.id,
        pr.empresa,
        pr.tipo_producto,
        COUNT(DISTINCT p.id) as cantidad_productos,
        SUM(vp.cantidad) as cantidad_vendida,
        ROUND(SUM(vp.cantidad * p.precio_unidad), 2) as ingresos_totales,
        ROUND(100.0 * SUM(vp.cantidad * p.precio_unidad) /
            (SELECT SUM(vp2.cantidad * p2.precio_unidad)
             FROM ventas_productos vp2
             JOIN productos p2 ON vp2.id_producto = p2.id
             JOIN ventas v2 ON vp2.id_venta = v2.id
             JOIN facturas f2 ON v2.id_factura = f2.id
             WHERE f2.fecha BETWEEN :fecha_inicio AND :fecha_fin), 2) as porcentaje
    FROM proveedores pr
    LEFT JOIN productos p ON pr.id = p.id_proveedor
    LEFT JOIN ventas_productos vp ON p.id = vp.id_producto
    LEFT JOIN ventas v ON vp.id_venta = v.id
    LEFT JOIN facturas f ON v.id_factura = f.id AND f.fecha BETWEEN :fecha_inicio AND :fecha_fin
    GROUP BY pr.id, pr.empresa, pr.tipo_producto
    ORDER BY ingresos_totales DESC NULLS LAST
    """
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})


@tool
def sales_vs_inventory_by_category(fecha_inicio: str = "2025-01-01", fecha_fin: str = "2026-12-31") -> List[dict]:
    """
    Comparativo: ventas vs inventario por categoría.
    Identifica qué categorías tienen alta demanda vs poco stock.
    Parámetros:
      - fecha_inicio: formato 'YYYY-MM-DD'
      - fecha_fin: formato 'YYYY-MM-DD'
    """
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
    return execute_query(sql, {"fecha_inicio": fecha_inicio, "fecha_fin": fecha_fin})
