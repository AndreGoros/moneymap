"""
Módulo de cálculo de impuestos para MoneyMap.

Contiene un registro de tasas fiscales (IVA, VAT, GST, etc.) por país/región.
Usa Decimal para precisión exacta en todos los cálculos.
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union

from .exceptions import PaisNoSoportadoError, MontoInvalidoError

# ---------------------------------------------------------------------------
# Registro de impuestos por país
# Formato: "NombrePais": Decimal("porcentaje")
# El porcentaje representa la tasa impositiva (ej. 16 = 16%)
# ---------------------------------------------------------------------------
_IMPUESTOS: dict[str, Decimal] = {
    # América Latina
    "Mexico":       Decimal("16"),    # IVA
    "Argentina":    Decimal("21"),    # IVA
    "Colombia":     Decimal("19"),    # IVA
    "Chile":        Decimal("19"),    # IVA
    "Peru":         Decimal("18"),    # IGV
    "Brasil":       Decimal("12"),    # ICMS (promedio estatal)
    "Ecuador":      Decimal("15"),    # IVA
    "Uruguay":      Decimal("22"),    # IVA
    "Paraguay":     Decimal("10"),    # IVA
    "Bolivia":      Decimal("13"),    # IVA
    "Venezuela":    Decimal("16"),    # IVA
    "Costa Rica":   Decimal("13"),    # IVA
    "Panama":       Decimal("7"),     # ITBMS
    "Guatemala":    Decimal("12"),    # IVA
    "Honduras":     Decimal("15"),    # ISV
    "El Salvador":  Decimal("13"),    # IVA
    "Nicaragua":    Decimal("15"),    # IVA
    "Cuba":         Decimal("10"),    # Impuesto de ventas
    "Republica Dominicana": Decimal("18"),  # ITBIS
    # América del Norte
    "USA":          Decimal("0"),     # Sin IVA federal (varía por estado)
    "Canada":       Decimal("5"),     # GST federal
    # Europa
    "España":       Decimal("21"),    # IVA
    "Alemania":     Decimal("19"),    # MwSt
    "Francia":      Decimal("20"),    # TVA
    "Italia":       Decimal("22"),    # IVA
    "Reino Unido":  Decimal("20"),    # VAT
    "Portugal":     Decimal("23"),    # IVA
    "Paises Bajos": Decimal("21"),    # BTW
    "Belgica":      Decimal("21"),    # TVA/BTW
    "Suecia":       Decimal("25"),    # Moms
    "Noruega":      Decimal("25"),    # MVA
    "Dinamarca":    Decimal("25"),    # Moms
    "Finlandia":    Decimal("24"),    # ALV
    "Polonia":      Decimal("23"),    # PTU
    "Suiza":        Decimal("7.7"),   # MWST
    "Austria":      Decimal("20"),    # USt
    "Grecia":       Decimal("24"),    # ΦΠΑ
    # Asia
    "Japon":        Decimal("10"),    # 消費税
    "China":        Decimal("13"),    # 增值税
    "India":        Decimal("18"),    # GST estándar
    "Corea del Sur": Decimal("10"),   # 부가가치세
    "Singapur":     Decimal("9"),     # GST
    "Australia":    Decimal("10"),    # GST
    "Nueva Zelanda": Decimal("15"),   # GST
}

_PRECISION = Decimal("0.01")


def _normalizar_monto(monto: Union[int, float, str, Decimal]) -> Decimal:
    """
    Convierte el monto al tipo Decimal de forma segura.

    Raises:
        MontoInvalidoError: Si el monto no puede convertirse o es negativo.
    """
    try:
        valor = Decimal(str(monto))
    except InvalidOperation:
        raise MontoInvalidoError(monto, "No es un número válido.")

    if valor < 0:
        raise MontoInvalidoError(monto, "El monto no puede ser negativo.")

    return valor


def impuesto(
    monto: Union[int, float, str, Decimal],
    pais: str,
) -> Decimal:
    """
    Calcula el monto del impuesto aplicable a un valor según el país indicado.

    Devuelve únicamente el monto del impuesto (no el total con impuesto).
    Para obtener el total, súmalo al monto original.

    Args:
        monto: El valor base sobre el cual calcular el impuesto.
        pais:  Nombre del país tal como aparece en el registro fiscal.
               Consulta paises_disponibles() para ver los nombres exactos.

    Returns:
        El monto del impuesto como Decimal, redondeado a 2 decimales.

    Raises:
        MontoInvalidoError:    Si el monto no es un número válido o es negativo.
        PaisNoSoportadoError:  Si el país no tiene reglas fiscales registradas.

    Example:
        >>> from moneymap import impuesto
        >>> impuesto(1000, "Mexico")
        Decimal('160.00')
        >>> total = 1000 + impuesto(1000, "Mexico")
        >>> print(total)
        1160.00
    """
    valor = _normalizar_monto(monto)

    if pais not in _IMPUESTOS:
        raise PaisNoSoportadoError(pais)

    tasa = _IMPUESTOS[pais] / Decimal("100")
    resultado = valor * tasa

    return resultado.quantize(_PRECISION, rounding=ROUND_HALF_UP)


def total_con_impuesto(
    monto: Union[int, float, str, Decimal],
    pais: str,
) -> Decimal:
    """
    Calcula el monto total (base + impuesto) para un país determinado.

    Args:
        monto: El valor base antes de impuestos.
        pais:  Nombre del país tal como aparece en el registro fiscal.

    Returns:
        El total (monto + impuesto) como Decimal, redondeado a 2 decimales.

    Raises:
        MontoInvalidoError:    Si el monto no es válido.
        PaisNoSoportadoError:  Si el país no está registrado.

    Example:
        >>> from moneymap import total_con_impuesto
        >>> total_con_impuesto(1000, "Mexico")
        Decimal('1160.00')
    """
    valor = _normalizar_monto(monto)
    impuesto_calculado = impuesto(valor, pais)
    return (valor + impuesto_calculado).quantize(_PRECISION, rounding=ROUND_HALF_UP)


def tasa_fiscal(pais: str) -> Decimal:
    """
    Devuelve la tasa de impuesto registrada para un país en porcentaje.

    Args:
        pais: Nombre del país tal como aparece en el registro fiscal.

    Returns:
        La tasa impositiva como Decimal (ej. Decimal('16') para 16%).

    Raises:
        PaisNoSoportadoError: Si el país no está registrado.

    Example:
        >>> from moneymap import tasa_fiscal
        >>> tasa_fiscal("Mexico")
        Decimal('16')
    """
    if pais not in _IMPUESTOS:
        raise PaisNoSoportadoError(pais)
    return _IMPUESTOS[pais]


def paises_disponibles() -> list[str]:
    """
    Devuelve la lista de países con reglas fiscales registradas.

    Returns:
        Lista de strings con los nombres de países disponibles,
        ordenada alfabéticamente.

    Example:
        >>> from moneymap import paises_disponibles
        >>> paises_disponibles()
        ['Alemania', 'Argentina', 'Australia', ...]
    """
    return sorted(_IMPUESTOS.keys())
