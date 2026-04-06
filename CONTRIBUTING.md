# Cómo contribuir a MoneyMap

Gracias por tu interés en mejorar MoneyMap. Esta guía cubre todo lo que necesitas para hacer una contribución.

---

## Índice

- [Antes de abrir un issue](#antes-de-abrir-un-issue)
- [Reportar un bug](#reportar-un-bug)
- [Proponer una mejora](#proponer-una-mejora)
- [Configurar el entorno de desarrollo](#configurar-el-entorno-de-desarrollo)
- [Hacer cambios y enviar un PR](#hacer-cambios-y-enviar-un-pr)
- [Convenciones del proyecto](#convenciones-del-proyecto)

---

## Antes de abrir un issue

Busca primero en los [issues existentes](https://github.com/AndreGoros/moneymap/issues) para evitar duplicados. Si ya existe uno similar, puedes añadir un comentario con tu caso específico.

---

## Reportar un bug

Abre un issue usando la etiqueta `bug` e incluye:

- Versión de MoneyMap (`pip show moneymap`)
- Versión de Python
- Código mínimo que reproduce el problema
- Resultado esperado vs. resultado real
- Traza completa del error, si aplica

---

## Proponer una mejora

Abre un issue con la etiqueta `enhancement` antes de escribir código. Describir la propuesta primero permite alinear la dirección antes de invertir tiempo en la implementación.

Casos de uso habituales donde se aceptan contribuciones:

- Agregar una divisa nueva (con fuente de la tasa de referencia)
- Agregar un país con su tasa fiscal (con fuente oficial)
- Corregir una tasa fiscal desactualizada
- Mejorar mensajes de error o documentación

---

## Configurar el entorno de desarrollo

**Requiere Python 3.10 o superior.**

```bash
git clone https://github.com/AndreGoros/moneymap
cd moneymap
pip install -e ".[dev]"
```

El extra `[dev]` instala pytest, ruff y las dependencias de pandas y polars para correr la suite completa.

---

## Hacer cambios y enviar un PR

1. Crea una rama descriptiva desde `main`:

```bash
git checkout -b fix/registrar-tasa-con-referencia-no-usd
# o
git checkout -b feat/agregar-divisa-sgd
```

2. Haz tus cambios. Si modificas código fuente, agrega o actualiza los tests correspondientes en `moneymap/test_moneymap.py`.

3. Verifica que todos los tests pasen y que el linter no reporte errores:

```bash
pytest
pytest --cov=moneymap --cov-report=term-missing
ruff check moneymap/
```

4. Haz commit con un mensaje claro en presente imperativo:

```bash
git commit -m "Fix normalización de tasa cuando referencia no es USD"
git commit -m "Add divisa SGD con tasa respecto a USD"
```

5. Abre el Pull Request contra `main`. Describe qué cambia y por qué.

---

## Convenciones del proyecto

**Precisión numérica** — Toda operación monetaria usa `Decimal`. No se usan `float` en resultados internos.

**Excepciones** — Los errores deben lanzar una subclase de `MoneyMapError` definida en `moneymap/exceptions.py`. No se usan excepciones genéricas de Python como `ValueError` directamente en la API pública.

**Tests** — Cada función pública tiene tests en `moneymap/test_moneymap.py`. La cobertura debe mantenerse al 100% de las líneas del paquete.

**Estilo** — El proyecto usa `ruff` para linting. Corre `ruff check moneymap/` antes de hacer commit.

**Idioma** — El código fuente, docstrings, mensajes de error y nombres de funciones están en español para mantener consistencia con la API pública del paquete.

---

## Licencia

Al contribuir aceptas que tu código se distribuirá bajo la [licencia MIT](LICENSE) del proyecto.
