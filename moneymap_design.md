> **El documento de diseño es tu entregable para este módulo.** Créalo como un archivo markdown en tu directorio de estudiante.

---

## Librería: MoneyMap

### Problema

Gestionar conversiones entre divisas internacionales, calcular deducciones fiscales (impuestos) y operar sobre columnas de DataFrames de pandas y Polars de forma precisa, evitando los errores de redondeo comunes al usar números de punto flotante (`float`) en aplicaciones financieras.

### Quantum

Convertir un monto entre dos divisas, calcular el impuesto según el país, u operar sobre una columna completa de un DataFrame (pandas o Polars).

### Vocabulario

| Sustantivo | En Python | Descripción |
|------------|-----------|-------------|
| Monto | `Decimal` | El valor numérico exacto, usando `decimal` de stdlib para evitar errores de punto flotante |
| Divisa | `str` | Código ISO de la moneda (ej. `"USD"`, `"MXN"`, `"EUR"`) |
| Tasa de cambio | `dict` interno | Mapa de factores de conversión referenciados a USD como moneda base |
| Jurisdicción | `str` | Nombre del país para aplicar sus reglas fiscales (ej. `"Mexico"`, `"España"`) |
| Registro fiscal | `dict` interno | Diccionario que mapea países con sus porcentajes de impuesto (IVA, VAT, GST, etc.) |
| DataFrame pandas | `pd.DataFrame` | Tabla de pandas sobre la que opera el accessor `df.moneymap` |
| DataFrame Polars | `pl.DataFrame` / `pl.LazyFrame` | Tabla de Polars sobre la que operan las funciones de `moneymap.polars` |
| Expresión Polars | `pl.Expr` | Expresión diferida de Polars para usar dentro de `.with_columns()` o `.select()` |

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
| Convertir columna (pandas) | `df.moneymap.convertir(col, origen, destino)` | Convierte una columna de montos; agrega columna `{col}_{DESTINO}` |
| Impuesto sobre columna (pandas) | `df.moneymap.impuesto(col, pais)` | Calcula el impuesto por fila; agrega columna `{col}_impuesto` |
| Total sobre columna (pandas) | `df.moneymap.total_con_impuesto(col, pais)` | Calcula base + impuesto por fila; agrega columna `{col}_total` |
| Resumen fiscal (pandas) | `df.moneymap.resumen_fiscal(col, pais)` | Agrega impuesto, total y tasa en una sola llamada |
| Convertir columna (Polars) | `mm.convertir(df, col, origen, destino)` | Igual que pandas pero con DataFrame o LazyFrame de Polars |
| Impuesto sobre columna (Polars) | `mm.impuesto(df, col, pais)` | Igual que pandas pero con DataFrame o LazyFrame de Polars |
| Total sobre columna (Polars) | `mm.total_con_impuesto(df, col, pais)` | Igual que pandas pero con DataFrame o LazyFrame de Polars |
| Resumen fiscal (Polars) | `mm.resumen_fiscal(df, col, pais)` | Igual que pandas pero con DataFrame o LazyFrame de Polars |
| Expresión convertir | `mm.expr_convertir(col, origen, destino)` | Devuelve una `pl.Expr` para usar dentro de `.with_columns()` |
| Expresión impuesto | `mm.expr_impuesto(col, pais)` | Devuelve una `pl.Expr` para usar dentro de `.with_columns()` |
| Expresión total | `mm.expr_total_con_impuesto(col, pais)` | Devuelve una `pl.Expr` para usar dentro de `.with_columns()` |

### Dream usage

```python
from moneymap import convertir, impuesto, registrar_tasa, divisas_disponibles
from moneymap import paises_disponibles, ayuda
from moneymap.taxes import total_con_impuesto, tasa_fiscal

# 1. Configurar tasas dinámicas (opcional)
registrar_tasa("MXN", "USD", 17.05)  # 1 USD = 17.05 MXN

# 2. Conversión entre divisas
pago_usd = convertir(1000, origen="MXN", destino="USD")
print(f"Total: {pago_usd} USD")  # Total: 58.65 USD

# 3. Calcular impuesto y total
iva   = impuesto(1000, pais="Mexico")           # 160.00
total = total_con_impuesto(1000, pais="Mexico") # 1160.00

# 4. Catálogos y ayuda
print(divisas_disponibles())  # ['ARS', 'AUD', 'BRL', ...]
print(paises_disponibles())   # ['Alemania', 'Argentina', ...]
ayuda()                       # índice de todas las funciones
ayuda("convertir")            # detalle con argumentos y ejemplo

# 5. Accessor de pandas
import pandas as pd
import moneymap.dataframe  # activa df.moneymap

df = pd.DataFrame({"producto": ["Laptop", "Monitor"], "precio": [25000, 8500]})

resultado = (
    df
    .moneymap.convertir(col="precio", origen="MXN", destino="USD")
    .moneymap.impuesto(col="precio_USD", pais="USA")
    .moneymap.total_con_impuesto(col="precio_USD", pais="USA")
)
df = df.moneymap.resumen_fiscal(col="precio", pais="España")
# agrega: precio_impuesto, precio_total, precio_tasa_pct

# 6. Funciones de Polars — DataFrame y LazyFrame
import polars as pl
import moneymap.polars as mm

df_pl = pl.DataFrame({"producto": ["Laptop", "Monitor"], "precio": [25000, 8500]})

# DataFrame normal
df_pl = mm.convertir(df_pl, col="precio", origen="MXN", destino="USD")
df_pl = mm.impuesto(df_pl, col="precio", pais="Mexico")
df_pl = mm.resumen_fiscal(df_pl, col="precio", pais="España")

# LazyFrame — evaluación diferida
resultado = (
    df_pl.lazy()
    .pipe(mm.convertir, col="precio", origen="MXN", destino="USD")
    .pipe(mm.impuesto,  col="precio_USD", pais="USA")
    .collect()
)

# Expresiones — múltiples columnas en una sola pasada
df_pl = df_pl.with_columns(
    mm.expr_convertir("precio", "MXN", "USD").alias("precio_USD"),
    mm.expr_convertir("precio", "MXN", "EUR").alias("precio_EUR"),
    mm.expr_impuesto("precio", "Mexico").alias("iva"),
    mm.expr_total_con_impuesto("precio", "Mexico").alias("precio_total"),
)
```
