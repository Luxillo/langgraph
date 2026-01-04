# 📊 Herramientas Analíticas - Documentación

## ✅ 15 Herramientas Creadas

### 1️⃣ VENTAS & INGRESOS (5 herramientas)

#### `sales_by_date(fecha_inicio, fecha_fin)`
- **Propósito**: Total de ventas agrupadas por fecha
- **Retorna**: fecha, cantidad de transacciones, total de ingresos, promedio por venta
- **Ejemplo**: "¿Cuánto vendimos en enero?"
- **Parámetros**:
  - `fecha_inicio`: 'YYYY-MM-DD' (default: 2025-01-01)
  - `fecha_fin`: 'YYYY-MM-DD' (default: 2025-12-31)

#### `sales_by_employee(fecha_inicio, fecha_fin)`
- **Propósito**: Total de ventas por empleado
- **Retorna**: nombre, apellido, cargo, cantidad de ventas, total vendido, promedio
- **Ejemplo**: "¿Quién vendió más este mes?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `sales_by_payment_method(fecha_inicio, fecha_fin)`
- **Propósito**: Ingresos por tipo de pago (Efectivo, Tarjeta Crédito, etc.)
- **Retorna**: método de pago, cantidad de transacciones, total, porcentaje
- **Ejemplo**: "¿Cuánto ingreso por efectivo?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `average_transaction_value(fecha_inicio, fecha_fin)`
- **Propósito**: Promedio, mínimo, máximo y total de transacciones
- **Retorna**: promedio, mínimo, máximo, total de transacciones
- **Ejemplo**: "¿Cuál es el ticket promedio?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `top_employees_by_sales(top_n=5, fecha_inicio, fecha_fin)`
- **Propósito**: Top N empleados con más ingresos generados
- **Retorna**: nombre, apellido, cargo, cantidad de ventas, total vendido
- **Ejemplo**: "¿Top 10 mejores vendedores?"
- **Parámetros**:
  - `top_n`: número (default 5)
  - `fecha_inicio`, `fecha_fin`

---

### 2️⃣ PRODUCTOS & INVENTARIO (5 herramientas)

#### `top_products_by_quantity(top_n=10, fecha_inicio, fecha_fin)`
- **Propósito**: Productos más vendidos por cantidad de unidades
- **Retorna**: nombre, marca, categoría, cantidad vendida, stock, ingresos
- **Ejemplo**: "¿Qué 10 productos se venden más?"
- **Parámetros**: top_n (default 10), fecha_inicio, fecha_fin

#### `revenue_by_product_category(fecha_inicio, fecha_fin)`
- **Propósito**: Ingresos totales por categoría de productos
- **Retorna**: categoría, cantidad vendida, ingresos totales, porcentaje
- **Ejemplo**: "¿Qué categoría genera más dinero?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `low_stock_products(threshold=100)`
- **Propósito**: Productos con stock bajo
- **Retorna**: nombre, marca, categoría, stock actual, precio, valor de inventario
- **Ejemplo**: "¿Qué productos necesitan reabastecimiento?"
- **Parámetros**:
  - `threshold`: nivel mínimo (default 100)

#### `inventory_rotation(fecha_inicio, fecha_fin)`
- **Propósito**: Identificar productos con rotación rápida vs lenta
- **Retorna**: nombre, cantidad vendida, stock, categoría de rotación
- **Ejemplo**: "¿Qué productos giran rápido?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `total_inventory_value()` / `inventory_by_category()`
- **Propósito**: Valor total del inventario
- **Retorna**: valor total, cantidad de productos, valor promedio
- **Ejemplo**: "¿Cuánto vale nuestro inventario?"
- **Parámetros**: ninguno

---

### 3️⃣ CLIENTES & COMPORTAMIENTO (3 herramientas)

#### `most_frequent_customers(top_n=10, fecha_inicio, fecha_fin)`
- **Propósito**: Clientes más frecuentes
- **Retorna**: nombre, cantidad de compras, ticket promedio, total gastado
- **Ejemplo**: "¿Quiénes son nuestros mejores clientes?"
- **Parámetros**: top_n (default 10), fecha_inicio, fecha_fin

#### `average_customer_ticket(fecha_inicio, fecha_fin)`
- **Propósito**: Análisis de ticket promedio por cliente
- **Retorna**: nombre, cantidad de compras, min/avg/max ticket, total gastado
- **Ejemplo**: "¿Cuál es el gasto promedio de cada cliente?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `preferred_payment_methods(fecha_inicio, fecha_fin)`
- **Propósito**: Métodos de pago preferidos
- **Retorna**: método de pago, clientes únicos, transacciones, ticket promedio
- **Ejemplo**: "¿Cómo pagan más los clientes?"
- **Parámetros**: fecha_inicio, fecha_fin

---

### 4️⃣ ANÁLISIS CRUZADOS (2 herramientas)

#### `revenue_by_supplier(fecha_inicio, fecha_fin)`
- **Propósito**: Ingresos generados por productos de cada proveedor
- **Retorna**: empresa, tipo, cantidad de productos, cantidad vendida, ingresos, porcentaje
- **Ejemplo**: "¿Qué proveedor genera más ingresos?"
- **Parámetros**: fecha_inicio, fecha_fin

#### `sales_vs_inventory_by_category(fecha_inicio, fecha_fin)`
- **Propósito**: Comparativa demanda vs stock por categoría
- **Retorna**: categoría, stock total, cantidad vendida, ratio de rotación, situación
- **Ejemplo**: "¿Qué categorías necesitan reabastecimiento urgente?"
- **Parámetros**: fecha_inicio, fecha_fin

---

## 🔄 Flujo de Uso

```
Usuario: "¿Cuánto vendimos en enero?"
  ↓
Agente: Identifica que es una consulta de ventas por fecha
  ↓
Agente: Llama sales_by_date("2025-01-01", "2025-01-31")
  ↓
Herramienta: Ejecuta SQL y retorna:
  - 15 transacciones
  - $45,000 en ingresos
  - $3,000 promedio por venta
  ↓
Agente: Formatea la respuesta en español
  ↓
Usuario: Recibe la respuesta con datos reales
```

---

## 📅 Parámetros de Fecha

Todas las herramientas soportan fechas paramétricas. Ejemplos:

| Usuario dice | Parámetros generados |
|---|---|
| "En enero" | fecha_inicio="2025-01-01", fecha_fin="2025-01-31" |
| "Este mes" | fecha_inicio="2025-01-01", fecha_fin="2025-01-31" (mes actual) |
| "Última semana" | fecha_inicio="2025-01-24", fecha_fin="2025-01-31" |
| "El año pasado" | fecha_inicio="2024-01-01", fecha_fin="2024-12-31" |
| Sin especificar | fecha_inicio="2025-01-01", fecha_fin="2025-12-31" (rango general) |

---

## 🎯 Ejemplos de Consultas

### "¿Cuáles fueron nuestras ventas en diciembre?"
```
sales_by_date(fecha_inicio="2024-12-01", fecha_fin="2024-12-31")
```

### "¿Top 5 mejores empleados de este mes?"
```
top_employees_by_sales(top_n=5, fecha_inicio="2025-01-01", fecha_fin="2025-01-31")
```

### "¿Qué productos necesitan reabastecimiento?"
```
low_stock_products(threshold=100)
```

### "¿Cuál es nuestro mejor cliente?"
```
most_frequent_customers(top_n=1, fecha_inicio="2025-01-01", fecha_fin="2025-01-31")
```

### "¿Qué categoría genera más ingresos?"
```
revenue_by_product_category(fecha_inicio="2025-01-01", fecha_fin="2025-01-31")
```

### "¿Cuánto vale nuestro inventario?"
```
total_inventory_value()
```

---

## ✨ Beneficios

✅ **Consultas precisas**: Datos reales de la BD, no alucinaciones
✅ **Fechas flexibles**: El usuario dice "enero" y el sistema lo convierte
✅ **Análisis cruzados**: Compara ventas, inventario, clientes en un solo query
✅ **Formateo automático**: Resultados legibles en español
✅ **Sin límites**: Puedes hacer consultas complejas combinando múltiples herramientas

---

## 🚀 Próximos pasos

1. Reinicia el servidor FastAPI
2. Prueba con: `"¿Cuánto vendimos en enero?"`
3. Luego: `"¿Top 10 productos más vendidos?"`
4. Finalmente: `"¿Qué clientes compraron más este mes?"`

¡Disfruta del análisis automático! 📈
