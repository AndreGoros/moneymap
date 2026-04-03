> **El documento de diseño es tu entregable para este módulo.** Créalo como un archivo markdown en tu directorio de estudiante.

---

## Librería: MoneyMap

### Problema

Gestionar conversiones entre divisas internacionales y calcular deducciones fiscales (impuestos) de forma precisa, evitando los errores de redondeo comunes al usar números de punto flotante (`float`) en aplicaciones financieras.

### Quantum

Convertir un monto entre dos divisas basado en una tasa de cambio, o calcular el impuesto aplicable a un monto según el país: `convertir(100, "MXN", "USD")` o `impuesto(100, "Mexico")`.

### Vocabulario

| Sustantivo | En Python | Descripción |
|------------|-----------|-------------|
| Monto | `Decimal` | El valor numérico exacto, usando `decimal` de stdlib para evitar errores de punto flotante |
| Divisa | `str` | Código ISO de la moneda (ej. `"USD"`, `"MXN"`, `"EUR"`) |
| Tasa de cambio | `dict` interno | Mapa de factores de conversión referenciados a USD como moneda base |
| Jurisdicción | `str` | Nombre del país para aplicar sus reglas fiscales (ej. `"Mexico"`, `"España"`) |
| Registro fiscal | `dict` interno | Diccionario que mapea países con sus porcentajes de impuesto (IVA, VAT, GST, etc.) |

| Verbo | En Python | Descripción |
|-------|-----------|-------------|
| Convertir | `convertir(monto, origen, destino)` | Transforma un monto de una divisa origen a una destino |
| Calcular impuesto | `impuesto(monto, pais)` | Devuelve el monto del impuesto aplicable según el país |
| Total con impuesto | `total_con_impuesto(monto, pais)` | Devuelve la suma del monto base más su impuesto |
| Registrar tasa | `registrar_tasa(divisa, referencia, tasa)` | Añade o actualiza una paridad entre dos divisas |
| Listar divisas | `divisas_disponibles()` | Devuelve los códigos de moneda soportados |
| Listar países | `paises_disponibles()` | Muestra los países con reglas fiscales registradas |
| Consultar tasa fiscal | `tasa_fiscal(pais)` | Devuelve el porcentaje de impuesto de un país |
| Mostrar ayuda | `ayuda(funcion="")` | Imprime la referencia de todas las funciones o el detalle de una en específico. |


### Dream usage

```python
from moneymap import convertir, impuesto, registrar_tasa, divisas_disponibles
from moneymap.taxes import total_con_impuesto, tasa_fiscal

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
ayuda()                      # resumen de todas las funciones
ayuda("convertir")           # detalle completo con argumentos y ejemplo
ayuda("impuesto")            # ídem para impuesto
```
