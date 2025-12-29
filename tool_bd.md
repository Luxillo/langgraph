# 🗄️ Propuesta: Integración de Tools de Base de Datos PostgreSQL

## 📋 Resumen Ejecutivo

Esta propuesta describe la evolución del bot multiagente actual para integrar capacidades de base de datos PostgreSQL, permitiendo que el agente consulte, modifique y analice datos empresariales de forma inteligente y segura.

---

## 🎯 Objetivos

- **Ampliar funcionalidades** del agente más allá de clima e imágenes
- **Integrar datos empresariales** de forma segura y eficiente
- **Mantener la simplicidad** del patrón actual de tools
- **Escalar hacia casos de uso reales** empresariales

---

## 🏗️ Arquitectura Propuesta

### **Arquitectura Actual**
```
Usuario → Agente → [Weather Tool | Image Tool] → Respuesta
```

### **Arquitectura Futura**
```
Usuario → Agente → [Weather | Image | Database Tools] → PostgreSQL → Respuesta
```

### **Componentes Nuevos**
```
src/
├── database/
│   ├── connection.py      # Pool de conexiones PostgreSQL
│   ├── models.py         # Modelos Pydantic/SQLAlchemy
│   ├── queries.py        # Queries SQL predefinidas
│   └── security.py       # Validación y sanitización
├── tools/
│   ├── database/
│   │   ├── user_tools.py      # Tools para usuarios
│   │   ├── product_tools.py   # Tools para productos
│   │   ├── order_tools.py     # Tools para pedidos
│   │   └── report_tools.py    # Tools para reportes
│   ├── weather.py        # Existente
│   └── image.py          # Existente
```

---

## 🔧 Tools de Base de Datos Propuestas

### **1. Tools Específicas por Dominio**

#### **User Tools (`user_tools.py`)**
```python
@tool
def query_users(filters: dict = None) -> str:
    """Consulta usuarios con filtros opcionales"""

@tool  
def create_user(name: str, email: str) -> str:
    """Crea un nuevo usuario"""

@tool
def update_user(user_id: int, **kwargs) -> str:
    """Actualiza datos de usuario"""
```

#### **Product Tools (`product_tools.py`)**
```python
@tool
def search_products(query: str, category: str = None) -> str:
    """Busca productos por nombre o categoría"""

@tool
def update_inventory(product_id: int, stock: int) -> str:
    """Actualiza stock de producto"""

@tool
def get_low_stock_products(threshold: int = 10) -> str:
    """Obtiene productos con stock bajo"""
```

#### **Report Tools (`report_tools.py`)**
```python
@tool
def get_sales_report(period: str, format: str = "text") -> str:
    """Genera reporte de ventas por período"""

@tool
def get_user_activity(user_id: int = None, days: int = 30) -> str:
    """Analiza actividad de usuarios"""
```

### **2. Tool Genérica Avanzada**

```python
@tool
def execute_safe_query(operation: str, table: str, conditions: dict = None) -> str:
    """Ejecuta consultas SQL validadas y seguras"""
```

---

## 🛡️ Seguridad y Validación

### **Capas de Seguridad**

1. **SQL Injection Prevention**
   - Queries parametrizadas obligatorias
   - Sanitización de inputs
   - Whitelist de operaciones permitidas

2. **Control de Acceso**
   - Role-based permissions
   - Operaciones por usuario/contexto
   - Audit trail de todas las operaciones

3. **Validación de Queries**
   - Parser SQL para validar estructura
   - Límites de tiempo de ejecución
   - Restricciones de tablas/columnas

4. **Rate Limiting**
   - Máximo de queries por minuto/usuario
   - Throttling por complejidad de query
   - Circuit breaker para protección

### **Configuración de Seguridad**
```env
# Database Security
ENABLE_SQL_VALIDATION=true
MAX_QUERIES_PER_MINUTE=100
ALLOWED_OPERATIONS=SELECT,INSERT,UPDATE
QUERY_TIMEOUT_SECONDS=30
ALLOWED_TABLES=users,products,orders
```

---

## 🧠 Evolución del Sistema de Prompts

### **Nuevo Contexto del Sistema**
```markdown
## Base de Datos Disponible

Tienes acceso a una base de datos PostgreSQL con estas tablas:

**users**: id, name, email, city, created_at, status
**products**: id, name, description, price, stock, category
**orders**: id, user_id, product_id, quantity, total, status, created_at

## Cuándo usar tools de BD:

- Información de usuarios/productos/pedidos
- Reportes y estadísticas  
- Crear/actualizar registros
- Análisis de datos empresariales

## Ejemplos de decisión:
- "¿Cuántos usuarios tenemos?" → query_users()
- "Productos con poco stock" → get_low_stock_products()
- "Ventas del mes pasado" → get_sales_report(period="last_month")
```

### **Clasificación de Intenciones Mejorada**
1. **Conversacional** → Respuesta directa
2. **Clima** → Weather Tool
3. **Imagen** → Image Tool
4. **Datos/Consultas** → Database Tools
5. **Reportes/Análisis** → Report Tools
6. **Mixto** → Múltiples tools en secuencia

---

## 🔄 Flujos de Trabajo Complejos

### **Ejemplo 1: Consulta Mixta**
```
Usuario: "Muéstrame usuarios de Madrid y el clima actual allí"

Flujo:
1. Agente identifica: datos + clima
2. Ejecuta: query_users(filters={"city": "Madrid"})
3. Ejecuta: get_weather("Madrid")  
4. Combina resultados en respuesta coherente
```

### **Ejemplo 2: Workflow de Negocio**
```
Usuario: "Crear usuario Juan de Barcelona y mostrar productos disponibles"

Flujo:
1. create_user(name="Juan", city="Barcelona")
2. search_products(filters={"stock > 0"})
3. get_weather("Barcelona") # Contexto adicional
4. Respuesta integrada con toda la información
```

### **Ejemplo 3: Análisis Inteligente**
```
Usuario: "¿Qué productos se están agotando?"

Flujo:
1. get_low_stock_products(threshold=5)
2. Análisis de patrones de venta
3. Recomendaciones automáticas
4. Posible alerta a administradores
```

---

## 📊 Casos de Uso Empresariales

### **Gestión de Usuarios**
- "¿Cuántos usuarios nuevos esta semana?"
- "Usuarios más activos del mes"
- "Crear usuario para el departamento de ventas"

### **Inventario y Productos**
- "¿Qué productos necesitan restock?"
- "Buscar productos de categoría electrónicos"
- "Actualizar precio del producto X"

### **Reportes y Analytics**
- "Ventas por región este trimestre"
- "Productos más vendidos"
- "Análisis de comportamiento de usuarios"

### **Operaciones Mixtas**
- "Usuarios de ciudades con buen clima hoy"
- "Generar imagen del mapa de ventas por región"
- "Crear reporte visual de inventario"

---

## 🚀 Roadmap de Implementación

### **Fase 1: Fundación (2-3 semanas)**
- [ ] Configurar conexión PostgreSQL
- [ ] Implementar 3 tools básicas (users, products, orders)
- [ ] Sistema de validación básico
- [ ] Tests unitarios

---

## ✅ Checklist de Estado (Pruebas antes de integrar)

- [x] `src/database/connection.py` creado y probado (construcción segura de `DATABASE_URL`)
- [x] `src/tools/database/product_tools.py` con funciones `search_products_by_name` y `get_low_stock_products`
- [x] `scripts/test_db.py` agregado para ejecutar checks locales
- [x] Contenedor Postgres levantado y accesible (ver `notas/docker-compose.yaml`)
- [ ] Endpoints de prueba para tools expuestos: `/tools/db/search_products` y `/tools/db/low_stock`
- [ ] Validación mínima (whitelist) implementada para queries dinámicas
- [ ] Tools envueltas como `@tool` y registradas en el agente (pendiente sólo después de pruebas)

### Cómo probar (rápido)

1. Levanta la API:

```bash
python -m uvicorn src.app:app --reload --port 8000
```

2. Probar endpoint `search_products` (ejemplo):

```bash
curl -sS -X POST http://localhost:8000/tools/db/search_products \
    -H 'Content-Type: application/json' \
    -d '{"term": "Leche", "limit": 5}' | jq
```

3. Probar endpoint `low_stock` (ejemplo):

```bash
curl -sS -X POST http://localhost:8000/tools/db/low_stock \
    -H 'Content-Type: application/json' \
    -d '{"threshold": 10}' | jq
```

4. Alternativa: script local

```bash
python3 -m scripts.test_db
```

Si los endpoints devuelven resultados, las tools funcionan y podemos integrarlas con seguridad en el agente.

### **Fase 2: Expansión (3-4 semanas)**
- [ ] Tools de reportes avanzados
- [ ] Sistema de cache
- [ ] Manejo robusto de errores
- [ ] Logging y monitoreo

### **Fase 3: Optimización (2-3 semanas)**
- [ ] Query optimization
- [ ] Connection pooling
- [ ] Rate limiting
- [ ] Performance metrics

### **Fase 4: Avanzado (4-5 semanas)**
- [ ] SQL dinámico seguro
- [ ] Workflows complejos
- [ ] Analytics en tiempo real
- [ ] Dashboard de monitoreo

---

## 📈 Beneficios Esperados

### **Para Desarrolladores**
- **Modularidad**: Fácil agregar nuevas tools
- **Reutilización**: Patrones consistentes
- **Mantenibilidad**: Código bien estructurado
- **Testabilidad**: Componentes aislados

### **Para Usuarios**
- **Inteligencia**: Decisiones automáticas de tools
- **Flexibilidad**: Desde queries simples a workflows complejos
- **Seguridad**: Múltiples capas de protección
- **Performance**: Optimizado para uso real

### **Para el Negocio**
- **Escalabilidad**: Crece con las necesidades
- **ROI**: Automatización de tareas repetitivas
- **Insights**: Análisis de datos empresariales
- **Integración**: Se conecta con sistemas existentes

---

## ⚠️ Consideraciones y Riesgos

### **Técnicos**
- **Complejidad**: Mayor superficie de ataque
- **Performance**: Queries lentas pueden afectar UX
- **Dependencias**: Más componentes = más puntos de falla

### **Seguridad**
- **Acceso a datos**: Requiere controles estrictos
- **SQL Injection**: Validación exhaustiva necesaria
- **Audit**: Trazabilidad de todas las operaciones

### **Operacionales**
- **Monitoreo**: Necesario para detectar problemas
- **Backup**: Estrategia de respaldo de BD
- **Escalamiento**: Planificar crecimiento de datos

---

## 🎯 Métricas de Éxito

### **Técnicas**
- Tiempo de respuesta < 2 segundos
- 99.9% uptime de BD
- 0 incidentes de seguridad
- Cobertura de tests > 90%

### **Funcionales**
- 80% de consultas resueltas automáticamente
- Reducción 50% en consultas manuales a BD
- Satisfacción usuario > 4.5/5
- Adopción > 70% del equipo

### **Negocio**
- ROI positivo en 6 meses
- Reducción 30% tiempo en reportes
- Incremento 25% en insights de datos
- Escalabilidad para 10x usuarios

---

## 🔗 Dependencias Técnicas

### **Nuevas Librerías**
```txt
# Database
psycopg2-binary==2.9.7
sqlalchemy==2.0.23
alembic==1.12.1

# Security  
sqlparse==0.4.4
bcrypt==4.1.2

# Performance
redis==5.0.1
celery==5.3.4
```

### **Infraestructura**
- PostgreSQL 14+
- Redis (cache)
- Monitoring (Prometheus/Grafana)
- Backup automatizado

---

Esta propuesta mantiene la simplicidad conceptual del proyecto actual mientras lo evoluciona hacia un sistema empresarial robusto y escalable.