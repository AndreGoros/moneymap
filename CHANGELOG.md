# Changelog

All notable changes to MoneyMap are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
MoneyMap uses [Semantic Versioning](https://semver.org/).

---

## [0.1.6] — 2026-04-06

### Fixed
- Corrección en el módulo de integración con Polars (`moneymap.dataframepl`): ajuste en el comportamiento de las funciones `expr_*` al usarse dentro de `.with_columns()`.

---

## [0.1.5] — 2026-04-06

### Added
- `Dockerfile` para ejecutar MoneyMap sin instalación local.
- Soporte para `docker run --rm moneymap` (demo) y `docker run --rm moneymap pytest` (tests).
- Badges de CI y PyPI en el README.

---

## [0.1.4] — 2026-04-05

### Fixed
- Bug en `registrar_tasa()`: la normalización de tasas referenciadas a una divisa distinta de USD producía valores incorrectos. Se corrige la fórmula de conversión interna.

---

## [0.1.3] — 2026-04-04

### Added
- Integración completa con **Polars** (`moneymap.dataframepl`):
  - `convertir()`, `impuesto()`, `total_con_impuesto()`, `resumen_fiscal()` para `DataFrame` y `LazyFrame`.
  - Funciones de expresión `expr_convertir()`, `expr_impuesto()`, `expr_total_con_impuesto()` para usar en `.with_columns()`.

---

## [0.1.2] — 2026-04-04

### Added
- Método `resumen_fiscal(col, pais)` en el accessor de pandas: agrega `{col}_impuesto`, `{col}_total` y `{col}_tasa_pct` en una sola llamada.
- Parámetro opcional `resultado` en `df.moneymap.convertir()` para nombrar la columna de salida.

### Fixed
- Corrección de errores menores en el módulo de pandas (`moneymap.dataframepd`).

---

## [0.1.1] — 2026-04-03

### Added
- Integración con **pandas** (`moneymap.dataframepd`):
  - Accessor `df.moneymap` con métodos `convertir()`, `impuesto()` y `total_con_impuesto()`.
  - Todas las operaciones son no destructivas y encadenables.

---

## [0.1.0] — 2026-04-03

### Added
- Lanzamiento inicial de MoneyMap.
- `convertir(monto, origen, destino)` — conversión entre divisas con precisión `Decimal`.
- `impuesto(monto, pais)` — cálculo de IVA/VAT/GST para más de 35 países.
- `total_con_impuesto(monto, pais)` y `tasa_fiscal(pais)` en `moneymap.taxes`.
- `registrar_tasa(divisa, referencia, tasa)` — registro y actualización de tasas custom.
- `divisas_disponibles()` y `paises_disponibles()` — catálogos de divisas y jurisdicciones.
- `ayuda()` — sistema de ayuda integrada por función.
- Jerarquía de excepciones propias: `MoneyMapError`, `DivisaNoSoportadaError`, `PaisNoSoportadoError`, `MontoInvalidoError`, `TasaInvalidaError`.
- Suite de tests con 41 casos (`moneymap/test_moneymap.py`).
- Publicación en PyPI con extras opcionales `[pandas]`, `[polars]` y `[pandas,polars]`.

[0.1.6]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.6
[0.1.5]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.5
[0.1.4]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.4
[0.1.3]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.3
[0.1.2]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.2
[0.1.1]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.1
[0.1.0]: https://github.com/AndreGoros/moneymap/releases/tag/v0.1.0
