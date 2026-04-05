"""
Módulo de conversión de divisas para MoneyMap.

Todas las tasas de cambio están referenciadas al USD como moneda base.
Se usa el tipo `Decimal` para garantizar precisión numérica exacta.
"""

from decimal import Decimal, ROUND_HALF_UP, InvalidOperation
from typing import Union

from .exceptions import DivisaNoSoportadaError, TasaInvalidaError, MontoInvalidoError

# ---------------------------------------------------------------------------
# Tasas de cambio base (referenciadas a 1 USD)
# Fuente de referencia: valores aproximados para uso en desarrollo/pruebas.
# En producción, se recomienda actualizar con una API en tiempo real.
# ---------------------------------------------------------------------------
_TASAS_BASE: dict[str, Decimal] = {
    "USD": Decimal("1.0"),
    "MXN": Decimal("17.05"),
    "EUR": Decimal("0.92"),
    "GBP": Decimal("0.79"),
    "CAD": Decimal("1.36"),
    "JPY": Decimal("149.50"),
    "BRL": Decimal("4.97"),
    "ARS": Decimal("876.00"),
    "COP": Decimal("3925.00"),
    "CLP": Decimal("945.00"),
    "PEN": Decimal("3.72"),
    "CHF": Decimal("0.89"),
    "CNY": Decimal("7.24"),
    "INR": Decimal("83.12"),
    "AUD": Decimal("1.53"),
}

# Precisión decimal para los resultados de conversión
_PRECISION = Decimal("0.01")


def _normalizar_monto(monto: Union[int, float, str, Decimal]) -> Decimal:
    """
    Convierte el monto al tipo Decimal de forma segura.

    Args:
        monto: El valor a convertir. Acepta int, float, str o Decimal.

    Returns:
        El monto como Decimal.

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


def convertir(
    monto: Union[int, float, str, Decimal],
    origen: str,
    destino: str,
) -> Decimal:
    """
    Convierte un monto de una divisa origen a una divisa destino.

    Usa precisión Decimal para evitar errores de punto flotante.

    Args:
        monto:   El valor a convertir (int, float, str o Decimal).
        origen:  Código ISO de la divisa de origen (ej. "MXN").
        destino: Código ISO de la divisa de destino (ej. "USD").

    Returns:
        El monto convertido como Decimal, redondeado a 2 decimales.

    Raises:
        MontoInvalidoError:       Si el monto no es un número válido o es negativo.
        DivisaNoSoportadaError:   Si alguna de las divisas no está registrada.

    Example:
        >>> from moneymap import convertir
        >>> convertir(1000, "MXN", "USD")
        Decimal('58.65')
    """
    valor = _normalizar_monto(monto)

    origen = origen.upper()
    destino = destino.upper()

    if origen not in _TASAS_BASE:
        raise DivisaNoSoportadaError(origen)
    if destino not in _TASAS_BASE:
        raise DivisaNoSoportadaError(destino)

    # Convertir a USD primero, luego a la divisa destino
    en_usd = valor / _TASAS_BASE[origen]
    resultado = en_usd * _TASAS_BASE[destino]

    return resultado.quantize(_PRECISION, rounding=ROUND_HALF_UP)


def registrar_tasa(
    divisa: str,
    referencia: str,
    tasa: Union[int, float, str, Decimal],
) -> None:
    """
    Registra o actualiza la tasa de cambio de una divisa respecto a otra.

    La librería convierte internamente la tasa a la referencia USD.
    Si la divisa no existe, la crea; si ya existe, la actualiza.

    Args:
        divisa:     Código ISO de la divisa a registrar/actualizar (ej. "MXN").
        referencia: Código ISO de la divisa de referencia (ej. "USD").
        tasa:       Cuántas unidades de `divisa` equivalen a 1 unidad de `referencia`.

    Raises:
        TasaInvalidaError:      Si la tasa no es un número positivo válido.
        DivisaNoSoportadaError: Si la divisa de referencia no está registrada.

    Example:
        >>> from moneymap import registrar_tasa
        >>> registrar_tasa("USD", "MXN", 17.05)  # 1 MXN = 17.05 USD... er, al revés
        >>> # Registra que 1 USD = 17.05 MXN
        >>> registrar_tasa("MXN", "USD", 17.05)
    """
    divisa = divisa.upper()
    referencia = referencia.upper()

    if referencia not in _TASAS_BASE:
        raise DivisaNoSoportadaError(referencia)

    try:
        valor_tasa = Decimal(str(tasa))
    except InvalidOperation:
        raise TasaInvalidaError(tasa, "No es un número válido.")

    if valor_tasa <= 0:
        raise TasaInvalidaError(tasa, "La tasa debe ser mayor que cero.")

    # Normalizar a equivalencia en USD.
    # tasa         = cuántas `divisa`     hay por 1 `referencia`
    # tasa_usd_ref = cuántas `referencia`  hay por 1 USD
    # => cuántas `divisa` hay por 1 USD = tasa * tasa_usd_ref
    #
    # Ejemplo: registrar_tasa("MXN", "JPY", 0.10)
    #   tasa         = 0.10   (1 JPY = 0.10 MXN)
    #   tasa_usd_ref = 149.50 (1 USD = 149.50 JPY)
    #   resultado    = 0.10 * 149.50 = 14.95 MXN por USD  correcto
    tasa_usd_referencia = _TASAS_BASE[referencia]
    if referencia == "USD":
        _TASAS_BASE[divisa] = valor_tasa
    else:
        _TASAS_BASE[divisa] = valor_tasa * tasa_usd_referencia


def divisas_disponibles() -> list[str]:
    """
    Devuelve la lista de códigos de divisas soportadas por el sistema.

    Returns:
        Lista de strings con los códigos ISO de las divisas disponibles,
        ordenada alfabéticamente.

    Example:
        >>> from moneymap import divisas_disponibles
        >>> divisas_disponibles()
        ['ARS', 'AUD', 'BRL', 'CAD', 'CHF', ...]
    """
    return sorted(_TASAS_BASE.keys())
