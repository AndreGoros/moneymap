"""
demo_moneymap.py — Demo interactivo de MoneyMap en la terminal.

Ejecutar:
    python demo_moneymap.py
"""

import sys
import os

from moneymap import (
    convertir,
    impuesto,
    registrar_tasa,
    divisas_disponibles,
    paises_disponibles,
    ayuda,
)
from moneymap.taxes import total_con_impuesto, tasa_fiscal
from moneymap.exceptions import (
    DivisaNoSoportadaError,
    PaisNoSoportadoError,
    MontoInvalidoError,
    TasaInvalidaError,
)

# ── Colores ANSI ────────────────────────────────────────────────────────────
RESET  = "\033[0m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
GREEN  = "\033[32m"
CYAN   = "\033[36m"
YELLOW = "\033[33m"
RED    = "\033[31m"
BLUE   = "\033[34m"
WHITE  = "\033[97m"


def header(texto: str) -> None:
    ancho = 54
    print()
    print(f"{CYAN}{'─' * ancho}{RESET}")
    print(f"{BOLD}{WHITE}  {texto}{RESET}")
    print(f"{CYAN}{'─' * ancho}{RESET}")


def ok(label: str, valor) -> None:
    print(f"  {GREEN}✓{RESET}  {DIM}{label:<28}{RESET}  {BOLD}{valor}{RESET}")


def info(texto: str) -> None:
    print(f"  {DIM}{texto}{RESET}")


def error_demo(label: str, exc: Exception) -> None:
    print(f"  {YELLOW}⚠{RESET}  {DIM}{label:<28}{RESET}  {RED}{exc}{RESET}")


def separador() -> None:
    print(f"  {DIM}{'·' * 50}{RESET}")


# ── Demo ────────────────────────────────────────────────────────────────────

def demo_conversion() -> None:
    header("1 · Conversión de divisas")

    resultado = convertir(1000, "MXN", "USD")
    ok("convertir(1000, MXN, USD)", f"{resultado} USD")

    resultado = convertir(100, "USD", "MXN")
    ok("convertir(100, USD, MXN)", f"{resultado} MXN")

    resultado = convertir(500, "EUR", "GBP")
    ok("convertir(500, EUR, GBP)", f"{resultado} GBP")

    resultado = convertir(1, "USD", "JPY")
    ok("convertir(1, USD, JPY)", f"{resultado} JPY")

    separador()
    info("acepta int, float, str y Decimal:")

    ok('convertir("250.5", MXN, USD)', f'{convertir("250.5", "MXN", "USD")} USD')
    ok("convertir(0, USD, EUR)",        f'{convertir(0, "USD", "EUR")} EUR')


def demo_tasas() -> None:
    header("2 · Registro de tasas custom")

    info("antes  → convertir(100, USD, MXN)")
    ok("resultado", f"{convertir(100, 'USD', 'MXN')} MXN")

    registrar_tasa("MXN", "USD", 20.00)
    info("después registrar_tasa('MXN', 'USD', 20.00)")
    ok("resultado", f"{convertir(100, 'USD', 'MXN')} MXN")

    # Restaurar para el resto del demo
    registrar_tasa("MXN", "USD", 17.05)

    separador()
    info("agregar divisa nueva:")
    registrar_tasa("VEF", "USD", 36.50)
    ok("registrar_tasa(VEF, USD, 36.50)", "registrada")
    ok("convertir(100, USD, VEF)", f"{convertir(100, 'USD', 'VEF')} VEF")


def demo_impuestos() -> None:
    header("3 · Cálculo de impuestos")

    paises = ["Mexico", "Argentina", "España", "USA", "Suecia", "Japon"]
    monto = 1000

    for pais in paises:
        tasa = tasa_fiscal(pais)
        imp  = impuesto(monto, pais)
        tot  = total_con_impuesto(monto, pais)
        print(
            f"  {GREEN}✓{RESET}  {DIM}{pais:<16}{RESET}"
            f"  tasa {CYAN}{str(tasa)+'%':<6}{RESET}"
            f"  impuesto {YELLOW}{str(imp):<8}{RESET}"
            f"  total {BOLD}{tot}{RESET}"
        )

    separador()
    info("total_con_impuesto(1000, Mexico) = base + IVA:")
    ok("1000 + 160.00", f"{total_con_impuesto(1000, 'Mexico')}")


def demo_catalogos() -> None:
    header("4 · Catálogos disponibles")

    divisas = divisas_disponibles()
    info(f"divisas_disponibles()  →  {len(divisas)} divisas")
    print(f"  {CYAN}{', '.join(divisas)}{RESET}")

    print()
    paises = paises_disponibles()
    info(f"paises_disponibles()   →  {len(paises)} países")
    cols = 3
    for i in range(0, len(paises), cols):
        fila = paises[i:i+cols]
        print("  " + "  ".join(f"{DIM}{p:<22}{RESET}" for p in fila))


def demo_errores() -> None:
    header("5 · Manejo de errores")

    casos = [
        ("divisa inválida",   lambda: convertir(100, "XYZ", "USD")),
        ("país no existe",    lambda: impuesto(100, "Neverland")),
        ("monto negativo",    lambda: convertir(-50, "USD", "MXN")),
        ("monto no numérico", lambda: convertir("abc", "USD", "MXN")),
        ("tasa <= 0",         lambda: registrar_tasa("TST", "USD", -5)),
    ]

    for label, fn in casos:
        try:
            fn()
        except (DivisaNoSoportadaError, PaisNoSoportadoError,
                MontoInvalidoError, TasaInvalidaError) as e:
            error_demo(label, e)


def demo_ayuda() -> None:
    header("6 · Ayuda integrada")

    info("ayuda()  →  índice general:")
    print()
    ayuda()

    separador()
    info("ayuda('convertir')  →  detalle de función:")
    print()
    ayuda("convertir")

    separador()
    info("ayuda('impuesto')  →  detalle de función:")
    print()
    ayuda("impuesto")


def demo_dataframe() -> None:
    header("7 · Integración con pandas")

    try:
        import pandas as pd
        import moneymap.dataframe  # registra el accessor df.moneymap
    except ImportError:
        info("pandas no instalado. Ejecuta: pip install moneymap[pandas]")
        return

    df = pd.DataFrame({
        "producto": ["Laptop", "Monitor", "Teclado", "Mouse"],
        "precio":   [25000,    8500,      1200,      350],
    })

    info("DataFrame original:")
    print()
    print(f"  {DIM}{df.to_string(index=False)}{RESET}")
    print()

    separador()
    info("df.moneymap.convertir(col='precio', origen='MXN', destino='USD')")
    df_conv = df.moneymap.convertir(col="precio", origen="MXN", destino="USD")
    print()
    print(f"  {DIM}{df_conv[['producto', 'precio', 'precio_USD']].to_string(index=False)}{RESET}")
    print()
    ok("columna agregada", "precio_USD")
    ok("original intacto", "precio sin modificar")

    separador()
    info("df.moneymap.impuesto(col='precio', pais='Mexico')")
    df_imp = df.moneymap.impuesto(col="precio", pais="Mexico")
    print()
    print(f"  {DIM}{df_imp[['producto', 'precio', 'precio_impuesto']].to_string(index=False)}{RESET}")
    print()
    ok("columna agregada", "precio_impuesto  (IVA 16%)")

    separador()
    info("df.moneymap.total_con_impuesto(col='precio', pais='Mexico')")
    df_tot = df.moneymap.total_con_impuesto(col="precio", pais="Mexico")
    print()
    print(f"  {DIM}{df_tot[['producto', 'precio', 'precio_total']].to_string(index=False)}{RESET}")
    print()
    ok("columna agregada", "precio_total")

    separador()
    info("df.moneymap.resumen_fiscal(col='precio', pais='España')")
    df_res = df.moneymap.resumen_fiscal(col="precio", pais="España")
    cols_res = ["producto", "precio", "precio_impuesto", "precio_total", "precio_tasa_pct"]
    print()
    print(f"  {DIM}{df_res[cols_res].to_string(index=False)}{RESET}")
    print()
    ok("columnas agregadas", "impuesto + total + tasa_pct")

    separador()
    info("encadenado: MXN→USD + impuesto USA + total USA")
    df_chain = (
        df
        .moneymap.convertir(col="precio", origen="MXN", destino="USD")
        .moneymap.impuesto(col="precio_USD", pais="USA")
        .moneymap.total_con_impuesto(col="precio_USD", pais="USA")
    )
    cols_chain = ["producto", "precio", "precio_USD", "precio_USD_impuesto", "precio_USD_total"]
    print()
    print(f"  {DIM}{df_chain[cols_chain].to_string(index=False)}{RESET}")
    print()
    ok("operaciones encadenadas", "3 columnas nuevas en una sola cadena")


def main() -> None:
    print()
    print(f"{BOLD}{CYAN}  ╔══════════════════════════════════════════╗")
    print(f"  ║          MoneyMap — Demo Python          ║")
    print(f"  ╚══════════════════════════════════════════╝{RESET}")

    demo_conversion()
    demo_tasas()
    demo_impuestos()
    demo_catalogos()
    demo_errores()
    demo_ayuda()
    demo_dataframe()

    print()
    print(f"{CYAN}{'─' * 54}{RESET}")
    print(f"  {GREEN}{BOLD}Demo completado sin errores inesperados.{RESET}")
    print()


if __name__ == "__main__":
    main()
