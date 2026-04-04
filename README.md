# MoneyMap

> Conversión de divisas y cálculo de impuestos con **precisión decimal exacta**.

MoneyMap resuelve el problema de los errores de redondeo al trabajar con dinero en Python. Usa el tipo `Decimal` de la librería estándar para garantizar que nunca pierdas un centavo en tus cálculos.

```python
from moneymap import convertir, impuesto

pago = convertir(1000, origen="MXN", destino="USD")
print(f"Total: {pago} USD")  # Total: 58.65 USD

iva = impuesto(1000, pais="Mexico")
print(f"IVA: {iva}")         # IVA: 160.00
```

---

## Instalación

```bash
pip install moneymap              # solo funciones básicas
pip install moneymap[pandas]      # con soporte para pandas
pip install moneymap[polars]      # con soporte para polars
pip install moneymap[pandas,polars]  # ambos
```

**Requiere Python 3.10+**.

---

## Referencia de API

### `convertir(monto, origen, destino)`

Convierte un monto de una divisa a otra.

| Parámetro | Tipo                       | Descripción                              |
|-----------|----------------------------|------------------------------------------|
| `monto`   | `int \| float \| str \| Decimal` | El valor a convertir                 |
| `origen`  | `str`                      | Código ISO de la divisa de origen        |
| `destino` | `str`                      | Código ISO de la divisa de destino       |

**Retorna:** `Decimal` — el monto convertido, redondeado a 2 decimales.

```python
from moneymap import convertir

convertir(100, "USD", "MXN")   # Decimal('1705.00')
convertir(500, "EUR", "GBP")   # Decimal('429.35')
convertir(1,   "USD", "JPY")   # Decimal('149.50')
```

---

### `impuesto(monto, pais)`

Calcula el monto del impuesto aplicable (IVA, VAT, GST, etc.) según el país.

**Nota:** Devuelve sólo el impuesto, no el total. Para obtener el total, usa `total_con_impuesto()`.

```python
from moneymap import impuesto

impuesto(1000, "Mexico")    # Decimal('160.00')  → IVA 16%
impuesto(1000, "España")    # Decimal('210.00')  → IVA 21%
impuesto(1000, "USA")       # Decimal('0.00')    → Sin IVA federal
```

---

### `registrar_tasa(divisa, referencia, tasa)`

Registra o actualiza la tasa de cambio de una divisa.

```python
from moneymap import registrar_tasa, convertir

registrar_tasa("MXN", "USD", 17.05)   # 1 USD = 17.05 MXN
registrar_tasa("VEF", "USD", 35.50)   # divisa nueva
```

---

### Funciones adicionales (módulo `moneymap.taxes`)

```python
from moneymap.taxes import total_con_impuesto, tasa_fiscal

total_con_impuesto(1000, "Mexico")  # Decimal('1160.00')
tasa_fiscal("Mexico")               # Decimal('16')
tasa_fiscal("Suecia")               # Decimal('25')
```

---

### `divisas_disponibles()` / `paises_disponibles()`

```python
from moneymap import divisas_disponibles, paises_disponibles

divisas_disponibles()
# ['ARS', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'EUR', ...]

paises_disponibles()
# ['Alemania', 'Argentina', 'Australia', 'Austria', 'Belgica', ...]
```

---

## Integración con pandas

Activa el accessor importando el módulo una vez. Todas las operaciones son no destructivas y encadenables.

```python
import pandas as pd
import moneymap.dataframe  # activa df.moneymap

df = pd.DataFrame({
    "producto": ["Laptop", "Monitor", "Teclado"],
    "precio":   [25000,    8500,      1200],
})
```

### Métodos disponibles

```python
# Agrega columna "precio_USD"
df = df.moneymap.convertir(col="precio", origen="MXN", destino="USD")

# Agrega columna "precio_impuesto"
df = df.moneymap.impuesto(col="precio", pais="Mexico")

# Agrega columna "precio_total"
df = df.moneymap.total_con_impuesto(col="precio", pais="Mexico")

# Agrega precio_impuesto + precio_total + precio_tasa_pct en una sola llamada
df = df.moneymap.resumen_fiscal(col="precio", pais="España")
```

### Encadenado

```python
resultado = (
    df
    .moneymap.convertir(col="precio", origen="MXN", destino="USD")
    .moneymap.impuesto(col="precio_USD", pais="USA")
    .moneymap.total_con_impuesto(col="precio_USD", pais="USA")
)
```

El parámetro opcional `resultado` permite nombrar la columna de salida:

```python
df.moneymap.convertir(col="precio", origen="MXN", destino="USD", resultado="precio_dolar")
```

---

## Integración con Polars

Polars no tiene sistema de accessors, por lo que la integración usa funciones que reciben el DataFrame como primer argumento. Soporta `DataFrame`, `LazyFrame` y expresiones (`pl.Expr`).

```python
import polars as pl
import moneymap.polars as mm
```

### DataFrame y LazyFrame

El mismo API funciona para ambos tipos — si pasas un `LazyFrame`, recibes un `LazyFrame`:

```python
df_pl = pl.DataFrame({
    "producto": ["Laptop", "Monitor", "Teclado"],
    "precio":   [25000,    8500,      1200],
})

# DataFrame normal
df_pl = mm.convertir(df_pl, col="precio", origen="MXN", destino="USD")
df_pl = mm.impuesto(df_pl, col="precio", pais="Mexico")
df_pl = mm.total_con_impuesto(df_pl, col="precio", pais="Mexico")
df_pl = mm.resumen_fiscal(df_pl, col="precio", pais="España")

# LazyFrame — evaluación diferida, todo se ejecuta en .collect()
resultado = (
    df_pl.lazy()
    .pipe(mm.convertir, col="precio", origen="MXN", destino="USD")
    .pipe(mm.impuesto,  col="precio_USD", pais="USA")
    .pipe(mm.total_con_impuesto, col="precio_USD", pais="USA")
    .collect()
)
```

### Expresiones

Las funciones `expr_*` devuelven una `pl.Expr` para usar dentro de `.with_columns()` o `.select()`, permitiendo calcular múltiples columnas en una sola pasada:

```python
df_pl = df_pl.with_columns(
    mm.expr_convertir("precio", "MXN", "USD").alias("precio_USD"),
    mm.expr_convertir("precio", "MXN", "EUR").alias("precio_EUR"),
    mm.expr_impuesto("precio", "Mexico").alias("iva"),
    mm.expr_total_con_impuesto("precio", "Mexico").alias("precio_total"),
)
```

| Función | Retorna | Uso |
|---------|---------|-----|
| `mm.convertir(df, col, origen, destino)` | `DataFrame` / `LazyFrame` | Agrega columna `{col}_{DESTINO}` |
| `mm.impuesto(df, col, pais)` | `DataFrame` / `LazyFrame` | Agrega columna `{col}_impuesto` |
| `mm.total_con_impuesto(df, col, pais)` | `DataFrame` / `LazyFrame` | Agrega columna `{col}_total` |
| `mm.resumen_fiscal(df, col, pais)` | `DataFrame` / `LazyFrame` | Agrega impuesto + total + tasa_pct |
| `mm.expr_convertir(col, origen, destino)` | `pl.Expr` | Para usar en `.with_columns()` |
| `mm.expr_impuesto(col, pais)` | `pl.Expr` | Para usar en `.with_columns()` |
| `mm.expr_total_con_impuesto(col, pais)` | `pl.Expr` | Para usar en `.with_columns()` |

---

## Ayuda integrada

```python
from moneymap import ayuda

ayuda()                        # índice de todas las funciones
ayuda("convertir")             # detalle con argumentos, retorno y ejemplo
ayuda("impuesto")
ayuda("registrar_tasa")
ayuda("total_con_impuesto")
ayuda("tasa_fiscal")
ayuda("divisas_disponibles")
ayuda("paises_disponibles")
```

---

## Divisas incluidas

| Código | Divisa              | Código | Divisa          |
|--------|---------------------|--------|-----------------|
| USD    | Dólar estadounidense | MXN   | Peso mexicano   |
| EUR    | Euro                | CAD    | Dólar canadiense|
| GBP    | Libra esterlina     | JPY    | Yen japonés     |
| BRL    | Real brasileño      | ARS    | Peso argentino  |
| COP    | Peso colombiano     | CLP    | Peso chileno    |
| PEN    | Sol peruano         | CHF    | Franco suizo    |
| CNY    | Yuan chino          | INR    | Rupia india     |
| AUD    | Dólar australiano   | ...    | y más           |


---

## Países e impuestos incluidos

Más de 35 países de América Latina, Europa y Asia, incluyendo:

- **México** (IVA 16%), **Argentina** (IVA 21%), **Colombia** (IVA 19%)
- **España** (IVA 21%), **Alemania** (19%), **Francia** (20%), **Reino Unido** (20%)
- **Japón** (10%), **China** (13%), **India** (18%), **Australia** (10%)
- Y muchos más — consulta `paises_disponibles()` para la lista completa.

---

## ¿Por qué Decimal y no float?

```python
# ❌ Con float: error de punto flotante
0.1 + 0.2 == 0.3       # False
0.1 + 0.2              # 0.30000000000000004

# ✅ Con MoneyMap: precisión exacta
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True
```

---

## Licencia

MIT — libre para uso personal y comercial.
