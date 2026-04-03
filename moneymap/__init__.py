"""
MoneyMap - Librería de conversión de divisas y cálculo de impuestos.

Maneja montos financieros con precisión decimal exacta para evitar
errores de redondeo comunes en aplicaciones financieras.
"""

from .currency import convertir, registrar_tasa, divisas_disponibles
from .taxes import impuesto, paises_disponibles
from .help import ayuda
from .exceptions import (
    MoneyMapError,
    DivisaNoSoportadaError,
    PaisNoSoportadoError,
    TasaInvalidaError,
    MontoInvalidoError,
)

__version__ = "0.1.0"
__author__ = "MoneyMap Contributors"
__license__ = "MIT"

__all__ = [
    # Funciones principales
    "ayuda",
    "convertir",
    "registrar_tasa",
    "divisas_disponibles",
    "impuesto",
    "paises_disponibles",
    # Excepciones
    "MoneyMapError",
    "DivisaNoSoportadaError",
    "PaisNoSoportadoError",
    "TasaInvalidaError",
    "MontoInvalidoError",
]
