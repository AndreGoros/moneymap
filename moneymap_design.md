> **El documento de diseño es tu entregable para este módulo.** Créalo como un archivo markdown en tu directorio de estudiante.

---

## Librería: MoneyMap

### Problema

Gestionar conversiones entre divisas internacionales, calcular deducciones fiscales (impuestos) y operar sobre columnas de DataFrames de pandas de forma precisa, evitando los errores de redondeo comunes al usar números de punto flotante (`float`) en aplicaciones financieras.

### Quantum

Convertir un monto entre dos divisas, calcular el impuesto según el país, u operar sobre una columna completa de un DataFrame: `convertir(100, "MXN", "USD")`, `impuesto(100, "Mexico")` o `df.moneymap.convertir(col="precio", origen="MXN", destino="USD")`.

### Vocabulario

| Sustantivo | En Python | Descripción |
|------------|-----------|-------------|
| Monto | `Decimal` | El valor numérico exacto, usando `decimal` de stdlib para evitar errores de punto flotante |
| Divisa | `str` | Código ISO de la moneda (ej. `"USD"`, `"MXN"`, `"EUR"`) |
| Tasa de cambio | `dict` interno | Mapa de factores de conversión referenciados a USD como moneda base |
| Jurisdicción | `str` | Nombre del país para aplicar sus reglas fiscales (ej. `"Mexico"`, `"España"`) |
| Registro fiscal | `dict` interno | Diccionario que mapea países con sus porcentajes de impuesto (IVA, VAT, GST, etc.) |
| DataFrame | `pd.DataFrame` | Tabla de pandas sobre la que opera el accessor `moneymap` |

| Verbo | En Python | Descripción |
|-------|-----------|-------------|
| Convertir | `convertir(monto, origen, destino)` | Transforma un monto de una divisa origen a una destino |
| Calcular impuesto | `impuesto(monto, pais)` | Devuelve el monto del impuesto aplicable según el país |
| Total con impuesto | `total_con_impuesto(monto, pais)` | Devuelve la suma del monto base más su impuesto |
| Registrar tasa | `registrar_tasa(divisa, referencia, tasa)` | Añade o actualiza una paridad entre dos divisas |
| Listar divisas | `divisas_disponibles()` | Devuelve los códigos de moneda soportados |
| Listar países | `paises_disponibles()` | Muestra los países con reglas fiscales registradas |
| Consultar tasa fiscal | `tasa_fiscal(pais)` | Devuelve el porcentaje de impuesto de un país |
| Mostrar ayuda | `ayuda(funcion="")` | Imprime la referencia de todas las funciones o el detalle de una en específico |
| Convertir columna | `df.moneymap.convertir(col, origen, destino)` | Convierte una columna de montos de una divisa a otra; agrega columna `{col}_{DESTINO}` |
| Impuesto sobre columna | `df.moneymap.impuesto(col, pais)` | Calcula el impuesto de cada fila de una columna; agrega columna `{col}_impuesto` |
| Total sobre columna | `df.moneymap.total_con_impuesto(col, pais)` | Calcula el total (base + impuesto) por fila; agrega columna `{col}_total` |
| Resumen fiscal | `df.moneymap.resumen_fiscal(col, pais)` | Agrega de una vez impuesto, total y tasa aplicada como columnas nuevas |

### Dream usage

```python
from moneymap import convertir, impuesto, registrar_tasa, divisas_disponibles
from moneymap import paises_disponibles, ayuda
from moneymap.taxes import total_con_impuesto, tasa_fiscal
import pandas as pd
import moneymap.dataframe  # activa df.moneymap

# 1. Configurar tasas dinámicas (opcional)
registrar_tasa("MXN", "USD", 17.05)  # 1 USD = 17.05 MXN

# 2. Conversión entre divisas
pago_usd = convertir(1000, origen="MXN", destino="USD")
print(f"Total: {pago_usd} USD")  # Total: 58.65 USD

# 3. Conversión en sentido inverso
en_mxn = convertir(50, origen="USD", destino="MXN")
print(en_mxn)  # 852.50

# 4. Calcular solo el impuesto
iva = impuesto(1000, pais="Mexico")
print(f"IVA: {iva}")  # IVA: 160.00

# 5. Obtener el total con impuesto incluido
total = total_con_impuesto(1000, pais="Mexico")
print(total)  # 1160.00

# 6. Consultar la tasa de un país
print(tasa_fiscal("España"))  # 21

# 7. Ver catálogos disponibles
print(divisas_disponibles())   # ['ARS', 'AUD', 'BRL', 'CAD', 'EUR', 'MXN', 'USD', ...]
print(paises_disponibles())    # ['Alemania', 'Argentina', 'Chile', 'España', 'Mexico', ...]

# 8. Ayuda integrada
ayuda()              # índice de todas las funciones
ayuda("convertir")   # detalle completo con argumentos y ejemplo
ayuda("impuesto")

# 9. Accessor de pandas — operaciones sobre columnas completas
df = pd.DataFrame({
    "producto": ["Laptop", "Monitor", "Teclado"],
    "precio":   [25000,    8500,      1200],
})

# Convertir columna de precios MXN → USD
df = df.moneymap.convertir(col="precio", origen="MXN", destino="USD")

# Calcular impuesto sobre los precios en USD
df = df.moneymap.impuesto(col="precio_USD", pais="USA")

# Obtener total con impuesto
df = df.moneymap.total_con_impuesto(col="precio", pais="Mexico")

# Resumen fiscal completo en una sola llamada
df = df.moneymap.resumen_fiscal(col="precio", pais="España")
# agrega: precio_impuesto, precio_total, precio_tasa_pct

# Encadenado
resultado = (
    df
    .moneymap.convertir(col="precio", origen="MXN", destino="USD")
    .moneymap.impuesto(col="precio_USD", pais="USA")
    .moneymap.total_con_impuesto(col="precio_USD", pais="USA")
)
```
