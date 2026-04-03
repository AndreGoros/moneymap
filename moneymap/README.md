# 💸 MoneyMap

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

## 🚀 Instalación

```bash
pip install moneymap
```

**Requiere Python 3.10+**. Sin dependencias externas — sólo usa la librería estándar de Python.

---

## 📖 Referencia de API

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

# Total con impuesto incluido
total = 1000 + impuesto(1000, "Mexico")  # 1160
```

---

### `registrar_tasa(divisa, referencia, tasa)`

Registra o actualiza la tasa de cambio de una divisa.

```python
from moneymap import registrar_tasa, convertir

# Registrar que 1 USD equivale a 17.05 MXN
registrar_tasa("MXN", "USD", 17.05)

# O agregar una divisa completamente nueva
registrar_tasa("VEF", "USD", 35.50)  # 1 USD = 35.50 VEF
```

---

### `divisas_disponibles()`

Lista todos los códigos de divisas soportados.

```python
from moneymap import divisas_disponibles

divisas_disponibles()
# ['ARS', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP', 'EUR', 'GBP',
#  'INR', 'JPY', 'MXN', 'PEN', 'USD', ...]
```

---

### `paises_disponibles()`

Lista todos los países con reglas fiscales registradas.

```python
from moneymap import paises_disponibles

paises_disponibles()
# ['Alemania', 'Argentina', 'Australia', 'Austria', 'Belgica', 'Bolivia',
#  'Brasil', 'Canada', 'Chile', 'China', 'Colombia', 'Costa Rica', ...]
```

---

### Funciones adicionales (módulo `moneymap.taxes`)

```python
from moneymap.taxes import total_con_impuesto, tasa_fiscal

# Monto base + impuesto en un solo paso
total_con_impuesto(1000, "Mexico")  # Decimal('1160.00')

# Consultar la tasa impositiva de un país
tasa_fiscal("Mexico")   # Decimal('16')
tasa_fiscal("Suecia")   # Decimal('25')
```

---

## 🌎 Divisas incluidas

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

> **Nota:** Las tasas de cambio incluidas son valores de referencia aproximados.
> Para aplicaciones de producción, se recomienda actualizar las tasas con `registrar_tasa()`
> usando datos de una API financiera en tiempo real.

---

## 🌍 Países e impuestos incluidos

Más de 35 países de América Latina, Europa y Asia, incluyendo:

- **México** (IVA 16%), **Argentina** (IVA 21%), **Colombia** (IVA 19%)
- **España** (IVA 21%), **Alemania** (19%), **Francia** (20%), **Reino Unido** (20%)
- **Japón** (10%), **China** (13%), **India** (18%), **Australia** (10%)
- Y muchos más — consulta `paises_disponibles()` para la lista completa.

---

## ⚡ ¿Por qué Decimal y no float?

```python
# ❌ Con float: error de punto flotante
0.1 + 0.2 == 0.3       # False
0.1 + 0.2              # 0.30000000000000004

# ✅ Con MoneyMap: precisión exacta
from decimal import Decimal
Decimal("0.1") + Decimal("0.2") == Decimal("0.3")  # True
```

MoneyMap convierte automáticamente todos los montos a `Decimal` internamente.

---

## 🛠️ Desarrollo

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/moneymap
cd moneymap

# Instalar en modo editable con dependencias de desarrollo
pip install -e ".[dev]"

# Ejecutar pruebas
pytest

# Ejecutar pruebas con cobertura
pytest --cov=moneymap --cov-report=term-missing

# Linting
ruff check moneymap/
```

---

## 📦 Publicar en PyPI

```bash
# Instalar herramientas de build
pip install build twine

# Construir la distribución
python -m build

# Subir a PyPI (requiere cuenta y API token)
twine upload dist/*
```

---

## 📄 Licencia

MIT — libre para uso personal y comercial.
