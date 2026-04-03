"""
Módulo de ayuda para MoneyMap.

Uso:
    from moneymap import ayuda
    ayuda()           # ayuda general
    ayuda("convertir")  # ayuda de una función específica
"""

RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
CYAN   = "\033[36m"
GREEN  = "\033[32m"
YELLOW = "\033[33m"
WHITE  = "\033[97m"
BLUE   = "\033[34m"

_AYUDA = {
    "convertir": {
        "firma": "convertir(monto, origen, destino)",
        "desc":  "Convierte un monto de una divisa a otra con precisión decimal exacta.",
        "args": [
            ("monto",   "int | float | str | Decimal", "Valor a convertir. No puede ser negativo."),
            ("origen",  "str",                         "Código ISO de la divisa de origen (ej. 'MXN')."),
            ("destino", "str",                         "Código ISO de la divisa de destino (ej. 'USD')."),
        ],
        "retorna": "Decimal — resultado redondeado a 2 decimales.",
        "lanza": [
            ("MontoInvalidoError",     "Si el monto no es numérico o es negativo."),
            ("DivisaNoSoportadaError", "Si alguna divisa no está registrada."),
        ],
        "ejemplo": """\
from moneymap import convertir

convertir(1000, "MXN", "USD")   # → Decimal('58.65')
convertir(100,  "USD", "MXN")   # → Decimal('1705.00')
convertir(500,  "EUR", "GBP")   # → Decimal('429.35')""",
    },

    "impuesto": {
        "firma": "impuesto(monto, pais)",
        "desc":  "Calcula el monto del impuesto (IVA/VAT/GST) según el país. "
                 "Devuelve SOLO el impuesto, no el total.",
        "args": [
            ("monto", "int | float | str | Decimal", "Valor base antes de impuestos."),
            ("pais",  "str",                         "Nombre del país (ej. 'Mexico'). Usa paises_disponibles() para ver opciones."),
        ],
        "retorna": "Decimal — monto del impuesto, redondeado a 2 decimales.",
        "lanza": [
            ("MontoInvalidoError",  "Si el monto no es numérico o es negativo."),
            ("PaisNoSoportadoError","Si el país no tiene reglas fiscales registradas."),
        ],
        "ejemplo": """\
from moneymap import impuesto

impuesto(1000, "Mexico")    # → Decimal('160.00')  (IVA 16%)
impuesto(1000, "España")    # → Decimal('210.00')  (IVA 21%)
impuesto(1000, "USA")       # → Decimal('0.00')    (sin IVA federal)

total = 1000 + impuesto(1000, "Mexico")  # → 1160""",
    },

    "total_con_impuesto": {
        "firma": "total_con_impuesto(monto, pais)",
        "desc":  "Calcula el monto total (base + impuesto) para un país. "
                 "Equivale a: monto + impuesto(monto, pais).",
        "args": [
            ("monto", "int | float | str | Decimal", "Valor base antes de impuestos."),
            ("pais",  "str",                         "Nombre del país."),
        ],
        "retorna": "Decimal — total con impuesto incluido, redondeado a 2 decimales.",
        "lanza": [
            ("MontoInvalidoError",  "Si el monto no es válido."),
            ("PaisNoSoportadoError","Si el país no está registrado."),
        ],
        "ejemplo": """\
from moneymap.taxes import total_con_impuesto

total_con_impuesto(1000, "Mexico")    # → Decimal('1160.00')
total_con_impuesto(500,  "Alemania")  # → Decimal('595.00')
total_con_impuesto(1000, "USA")       # → Decimal('1000.00')""",
    },

    "tasa_fiscal": {
        "firma": "tasa_fiscal(pais)",
        "desc":  "Devuelve el porcentaje de impuesto registrado para un país.",
        "args": [
            ("pais", "str", "Nombre del país."),
        ],
        "retorna": "Decimal — porcentaje (ej. Decimal('16') representa 16%).",
        "lanza": [
            ("PaisNoSoportadoError", "Si el país no está registrado."),
        ],
        "ejemplo": """\
from moneymap.taxes import tasa_fiscal

tasa_fiscal("Mexico")       # → Decimal('16')
tasa_fiscal("Reino Unido")  # → Decimal('20')
tasa_fiscal("Suiza")        # → Decimal('7.7')""",
    },

    "registrar_tasa": {
        "firma": "registrar_tasa(divisa, referencia, tasa)",
        "desc":  "Registra o actualiza la tasa de cambio de una divisa. "
                 "Si la divisa no existe la crea; si ya existe la actualiza. "
                 "La tasa indica cuántas unidades de 'divisa' hay por 1 unidad de 'referencia'.",
        "args": [
            ("divisa",     "str",                         "Código ISO de la divisa a registrar (ej. 'VEF')."),
            ("referencia", "str",                         "Código ISO de la divisa base (debe existir, ej. 'USD')."),
            ("tasa",       "int | float | str | Decimal", "Cuántas unidades de 'divisa' equivalen a 1 'referencia'. Debe ser > 0."),
        ],
        "retorna": "None",
        "lanza": [
            ("TasaInvalidaError",      "Si la tasa no es un número o es <= 0."),
            ("DivisaNoSoportadaError", "Si la divisa de referencia no está registrada."),
        ],
        "ejemplo": """\
from moneymap import registrar_tasa, convertir

# 1 USD = 17.05 MXN
registrar_tasa("MXN", "USD", 17.05)

# Agregar divisa nueva: 1 USD = 36.50 VEF
registrar_tasa("VEF", "USD", 36.50)
convertir(100, "USD", "VEF")  # → Decimal('3650.00')""",
    },

    "divisas_disponibles": {
        "firma": "divisas_disponibles()",
        "desc":  "Devuelve la lista de códigos de divisas soportadas, ordenada alfabéticamente.",
        "args": [],
        "retorna": "list[str] — códigos ISO de las divisas registradas.",
        "lanza": [],
        "ejemplo": """\
from moneymap import divisas_disponibles

divisas_disponibles()
# → ['ARS', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY',
#     'COP', 'EUR', 'GBP', 'INR', 'JPY', 'MXN', 'PEN', 'USD']""",
    },

    "paises_disponibles": {
        "firma": "paises_disponibles()",
        "desc":  "Devuelve la lista de países con reglas fiscales registradas, ordenada alfabéticamente.",
        "args": [],
        "retorna": "list[str] — nombres de países disponibles.",
        "lanza": [],
        "ejemplo": """\
from moneymap import paises_disponibles

paises_disponibles()
# → ['Alemania', 'Argentina', 'Australia', 'Austria',
#     'Belgica', 'Bolivia', 'Brasil', 'Canada', ...]""",
    },
}


def _imprimir_general() -> None:
    ancho = 58
    print()
    print(f"{CYAN}{'═' * ancho}{RESET}")
    print(f"{BOLD}{WHITE}  MoneyMap — Referencia de funciones{RESET}")
    print(f"{CYAN}{'═' * ancho}{RESET}")
    print(f"\n  {DIM}Uso: ayuda('nombre_funcion')  para ver detalles.{RESET}\n")

    secciones = [
        ("Divisas", ["convertir", "registrar_tasa", "divisas_disponibles"]),
        ("Impuestos", ["impuesto", "total_con_impuesto", "tasa_fiscal", "paises_disponibles"]),
    ]

    for titulo, funciones in secciones:
        print(f"  {YELLOW}{titulo}{RESET}")
        for nombre in funciones:
            info = _AYUDA[nombre]
            firma = info["firma"]
            desc  = info["desc"].split(".")[0]  # primera oración
            print(f"    {GREEN}{nombre}{RESET}{DIM}({firma.split('(')[1]}{RESET}")
            print(f"      {DIM}{desc}.{RESET}")
        print()

    print(f"  {DIM}Importar desde el paquete principal:{RESET}")
    print(f"  {CYAN}  from moneymap import convertir, impuesto, registrar_tasa{RESET}")
    print(f"  {CYAN}  from moneymap import divisas_disponibles, paises_disponibles{RESET}")
    print(f"  {CYAN}  from moneymap.taxes import total_con_impuesto, tasa_fiscal{RESET}")
    print(f"\n{CYAN}{'═' * ancho}{RESET}\n")


def _imprimir_funcion(nombre: str) -> None:
    if nombre not in _AYUDA:
        nombres = ", ".join(_AYUDA.keys())
        print(f"\n  {YELLOW}⚠{RESET}  Función '{nombre}' no encontrada.")
        print(f"  {DIM}Funciones disponibles: {nombres}{RESET}\n")
        return

    info  = _AYUDA[nombre]
    ancho = 58
    print()
    print(f"{CYAN}{'─' * ancho}{RESET}")
    print(f"  {BOLD}{WHITE}{info['firma']}{RESET}")
    print(f"{CYAN}{'─' * ancho}{RESET}")
    print(f"\n  {info['desc']}\n")

    if info["args"]:
        print(f"  {YELLOW}Argumentos{RESET}")
        for arg, tipo, desc in info["args"]:
            print(f"    {GREEN}{arg}{RESET}  {DIM}{tipo}{RESET}")
            print(f"      {desc}")
        print()

    print(f"  {YELLOW}Retorna{RESET}")
    print(f"    {info['retorna']}\n")

    if info["lanza"]:
        print(f"  {YELLOW}Lanza{RESET}")
        for exc, desc in info["lanza"]:
            print(f"    {GREEN}{exc}{RESET}  —  {DIM}{desc}{RESET}")
        print()

    print(f"  {YELLOW}Ejemplo{RESET}")
    for linea in info["ejemplo"].splitlines():
        if linea.startswith("from") or linea.startswith("import"):
            print(f"    {DIM}{linea}{RESET}")
        elif "# →" in linea:
            codigo, comentario = linea.split("# →")
            print(f"    {WHITE}{codigo}{RESET}{DIM}# → {comentario.strip()}{RESET}")
        else:
            print(f"    {WHITE}{linea}{RESET}")
    print(f"\n{CYAN}{'─' * ancho}{RESET}\n")


def ayuda(funcion: str = "") -> None:
    """
    Muestra la ayuda de MoneyMap.

    Sin argumentos muestra el resumen de todas las funciones.
    Con el nombre de una función muestra su documentación completa.

    Args:
        funcion: Nombre de la función a consultar (opcional).

    Ejemplo:
        >>> from moneymap import ayuda
        >>> ayuda()
        >>> ayuda("convertir")
        >>> ayuda("impuesto")
    """
    if funcion:
        _imprimir_funcion(funcion)
    else:
        _imprimir_general()
