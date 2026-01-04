# 📊 Herramientas Analíticas - Guía Rápida

## 🚀 Inicio Rápido

### 1. Ejecutar pruebas de herramientas
```bash
python3 scripts/test_analytics.py
```
Esto prueba todas las 15+ herramientas de análisis sin iniciar el servidor.

### 2. Iniciar el servidor con las nuevas herramientas
```bash
# Activar venv (si no está activado)
source .venv/bin/activate

# Iniciar FastAPI
python -m uvicorn src.app:app --port 8000 --reload
```

### 3. Hacer consultas al agente
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuánto vendimos en enero?"}'
```

---

## 📋 Herramientas Disponibles

### Grupo 1: Ventas & Ingresos (5 herramientas)
```
✅ sales_by_date              → Ventas agrupadas por fecha
✅ sales_by_employee          → Ventas por empleado
✅ sales_by_payment_method    → Ventas por tipo de pago
✅ average_transaction_value  → Promedios de transacción
✅ top_employees_by_sales     → Top N mejores vendedores
```

### Grupo 2: Productos & Inventario (6 herramientas)
```
✅ top_products_by_quantity       → Top N productos vendidos
✅ revenue_by_product_category    → Ingresos por categoría
✅ low_stock_products            → Productos con stock bajo
✅ inventory_rotation            → Rotación rápida vs lenta
✅ total_inventory_value         → Valor total del inventario
✅ inventory_by_category         → Inventario por categoría
```

### Grupo 3: Clientes & Comportamiento (3 herramientas)
```
✅ most_frequent_customers      → Clientes más frecuentes
✅ average_customer_ticket      → Ticket promedio por cliente
✅ preferred_payment_methods    → Métodos de pago preferidos
```

### Grupo 4: Análisis Cruzados (2 herramientas)
```
✅ revenue_by_supplier                  → Ingresos por proveedor
✅ sales_vs_inventory_by_category       → Demanda vs Stock
```

---

## 💬 Ejemplos de Consultas al Chat

### Ventas
```
"¿Cuánto vendimos en enero?"
"¿Quién fue el mejor vendedor?"
"¿Cuánto ingreso por efectivo?"
"¿Cuál es el ticket promedio?"
```

### Productos e Inventario
```
"¿Cuáles son nuestros 10 productos más vendidos?"
"¿Qué categoría genera más dinero?"
"¿Qué productos necesitan reabastecimiento?"
"¿Qué producto gira más rápido?"
"¿Cuánto vale nuestro inventario?"
```

### Clientes
```
"¿Quiénes son nuestros mejores clientes?"
"¿Cuál es el gasto promedio por cliente?"
"¿Cómo pagan más los clientes?"
```

### Análisis Cruzados
```
"¿Qué proveedor genera más ingresos?"
"¿Qué categorías necesitan reabastecimiento urgente?"
```

---

## 📅 Parámetros de Fecha

Todas las herramientas soportan **fechas paramétricas**. El agente automáticamente convierte:

```
Usuario dice          → Sistema interpreta como
"en enero"           → fecha_inicio="2025-01-01", fecha_fin="2025-01-31"
"este mes"           → Rango del mes actual
"última semana"      → Últimos 7 días
"el año pasado"      → 2024-01-01 a 2024-12-31
Sin especificar      → Rango general (2025-01-01 a 2025-12-31)
```

---

## 🔧 Configuración

### Variables de entorno (.env)
```
LLM_PROVIDER=ollama              # LLM a usar
OLLAMA_MODEL=mistral:7b          # Modelo ligero (rápido)
OLLAMA_BASE_URL=http://localhost:11434

DATABASE_URL=postgresql://agente_user:agente3_84p@localhost:5432/midb
```

### Cambiar temperatura del LLM
En [src/llm.py](src/llm.py):
```python
temperature=0.1  # Más bajo = respuestas más determinísticas
temperature=0.5  # Más alto = respuestas más creativas
```

---

## 📊 Estructura de Datos

### Tablas principales
```
facturas              → Transacciones de venta
facturas_detalles     → Detalles de pago
ventas                → Información de vendedor
ventas_productos      → Productos vendidos
compras_clientes      → Registro de cliente
productos             → Catálogo
empleados             → Staff
clientes              → Base de clientes
proveedores           → Proveedores
```

---

## 🐛 Troubleshooting

### Error: "Timeout" en consultas
**Causa**: El LLM está tardando mucho
**Solución**: Cambiar a `mistral:7b` (más ligero) en .env

### Error: "Sin datos disponibles"
**Causa**: Las fechas no tienen información
**Solución**: Usar fechas más amplias o rangos con datos

### Error: Conexión a PostgreSQL fallida
**Causa**: PostgreSQL no está corriendo
**Solución**: `docker-compose -f notas/docker-compose.yaml up -d`

---

## 📈 Casos de Uso Reales

### Dashboard de Ventas
```
"Dame un resumen de ventas de enero"
→ Llama sales_by_date + sales_by_employee + average_transaction_value
```

### Análisis de Inventario
```
"¿Qué necesito reabastecer urgente?"
→ Llama low_stock_products + sales_vs_inventory_by_category
```

### Análisis de Clientes
```
"¿Quiénes son mis clientes VIP?"
→ Llama most_frequent_customers + average_customer_ticket
```

---

## 🚀 Próximos Pasos

1. ✅ Herramientas analíticas creadas
2. ✅ Integradas en el grafo LangGraph
3. ✅ Tests unitarios creados
4. ⏭️ **Ejecuta**: `python3 scripts/test_analytics.py`
5. ⏭️ **Inicia servidor**: `python -m uvicorn src.app:app --port 8000`
6. ⏭️ **Prueba en chat**: `"¿Cuánto vendimos?"`

---

## 📚 Archivos Relacionados

- [ANALYTICS_TOOLS.md](ANALYTICS_TOOLS.md) - Documentación detallada de cada herramienta
- [src/tools/database/analytics_tools.py](src/tools/database/analytics_tools.py) - Código fuente
- [scripts/test_analytics.py](scripts/test_analytics.py) - Suite de pruebas
- [src/graph.py](src/graph.py) - Integración en el grafo

---

**Última actualización**: 3 de enero de 2026
**Versión**: 1.0 - 15 herramientas analíticas con fechas paramétricas
