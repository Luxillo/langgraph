# 📚 Documentación - Herramientas Analíticas

Bienvenido a la documentación completa del sistema de herramientas analíticas para el agente de supermercado.

## 📖 Guías Disponibles

### 🚀 [QUICK_START_ANALYTICS.md](QUICK_START_ANALYTICS.md)
**Para: Usuarios que quieren empezar rápido**
- Instrucciones de inicio en 5 pasos
- Ejemplos de consultas comunes
- Troubleshooting básico
- ~5 minutos de lectura

### 📊 [ANALYTICS_TOOLS.md](ANALYTICS_TOOLS.md)
**Para: Desarrolladores y usuarios avanzados**
- Documentación completa de las 15 herramientas
- Parámetros detallados de cada función
- Ejemplos de SQL generado
- ~15 minutos de lectura

### 🔧 [IMPLEMENTACION_HERRAMIENTAS.md](IMPLEMENTACION_HERRAMIENTAS.md)
**Para: Entender qué se implementó**
- Resumen técnico de la implementación
- Características principales
- Archivos creados y modificados
- Checklist de validación
- ~10 minutos de lectura

---

## 🎯 Acceso Rápido

### ¿Soy nuevo aquí?
→ Empieza con [QUICK_START_ANALYTICS.md](QUICK_START_ANALYTICS.md)

### ¿Quiero conocer todas las herramientas?
→ Lee [ANALYTICS_TOOLS.md](ANALYTICS_TOOLS.md)

### ¿Quiero saber qué se implementó?
→ Consulta [IMPLEMENTACION_HERRAMIENTAS.md](IMPLEMENTACION_HERRAMIENTAS.md)

---

## 📋 Herramientas por Categoría

### Ventas & Ingresos (5)
- `sales_by_date` - Ventas agrupadas por fecha
- `sales_by_employee` - Ventas por empleado
- `sales_by_payment_method` - Ventas por tipo de pago
- `average_transaction_value` - Promedios de transacción
- `top_employees_by_sales` - Top N mejores vendedores

### Productos & Inventario (6)
- `top_products_by_quantity` - Top N productos más vendidos
- `revenue_by_product_category` - Ingresos por categoría
- `low_stock_products` - Productos con stock bajo
- `inventory_rotation` - Rotación de inventario
- `total_inventory_value` - Valor total del inventario
- `inventory_by_category` - Inventario agrupado por categoría

### Clientes & Comportamiento (3)
- `most_frequent_customers` - Clientes más frecuentes
- `average_customer_ticket` - Ticket promedio por cliente
- `preferred_payment_methods` - Métodos de pago preferidos

### Análisis Cruzados (2)
- `revenue_by_supplier` - Ingresos por proveedor
- `sales_vs_inventory_by_category` - Demanda vs Stock por categoría

---

## 💬 Ejemplos de Consultas

```
Usuario: "¿Cuánto vendimos en enero?"
→ Llama: sales_by_date(fecha_inicio="2025-01-01", fecha_fin="2025-01-31")

Usuario: "¿Top 10 productos más vendidos?"
→ Llama: top_products_by_quantity(top_n=10)

Usuario: "¿Quién fue el mejor vendedor?"
→ Llama: top_employees_by_sales(top_n=1)

Usuario: "¿Qué productos necesitan reabastecimiento?"
→ Llama: low_stock_products(threshold=100)
```

---

## 🔗 Archivos Relacionados

### En el Repositorio
```
src/tools/database/analytics_tools.py     → Código de herramientas (500+ líneas)
scripts/test_analytics.py                 → Suite de pruebas (400+ líneas)
src/graph.py                              → Integración en LangGraph
src/prompts/system.md                     → Prompt del sistema
```

### En Documentación
```
docs/QUICK_START_ANALYTICS.md             → Guía rápida
docs/ANALYTICS_TOOLS.md                   → Documentación completa
docs/IMPLEMENTACION_HERRAMIENTAS.md       → Resumen técnico
docs/README.md                            → Este archivo
```

---

## 🧪 Testing

Ejecutar todas las pruebas:
```bash
python3 scripts/test_analytics.py
```

Esto prueba las 16 herramientas sin iniciar el servidor.

---

## 🚀 Inicio Rápido

```bash
# 1. Verificar instalación
python3 scripts/test_analytics.py

# 2. Iniciar PostgreSQL
docker-compose -f notas/docker-compose.yaml up -d

# 3. Iniciar servidor
python -m uvicorn src.app:app --port 8000 --reload

# 4. Probar en chat
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "¿Cuánto vendimos?"}'
```

---

## 📞 Preguntas Frecuentes

**P: ¿Todas las herramientas requieren fechas?**  
R: No. Las herramientas de inventario (stock) no las requieren.

**P: ¿Puedo personalizar el Top N?**  
R: Sí, todas las herramientas de ranking aceptan `top_n` como parámetro.

**P: ¿Los datos son reales?**  
R: 100% reales. Provienen directamente de PostgreSQL. Sin alucinaciones.

**P: ¿Cómo agrego más herramientas?**  
R: Ver sección "Extensiones" en [QUICK_START_ANALYTICS.md](QUICK_START_ANALYTICS.md)

---

## ✨ Características

- ✅ 15+ herramientas analíticas
- ✅ Fechas paramétricas automáticas
- ✅ Top N personalizable
- ✅ SQL optimizado
- ✅ Datos 100% reales
- ✅ Sin alucinaciones
- ✅ Tests incluidos
- ✅ Documentación completa

---

**Última actualización**: 3 de enero de 2026  
**Versión**: 1.0  
**Estado**: ✅ Listo para producción
