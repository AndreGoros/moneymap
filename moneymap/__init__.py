"""
MoneyMap - Librería de conversión de divisas y cálculo de impuestos.

Maneja montos financieros con precisión decimal exacta para evitar
errores de redondeo comunes en aplicaciones financieras.

Uso básico:
    from moneymap import convertir, impuesto
    convertir(1000, "MXN", "USD")   # Decimal('58.65')
    impuesto(1000, "Mexico")        # Decimal('160.00')

Integración con pandas y/o con polars (requiere: pip install moneymap[pandas], pip install moneymap[polars], pip install moneymap[pandas,polars]):
    import moneymap.dataframepd  # activa df.moneymap para pandas
    import moneymap.dataframepl
    df.moneymap.convertir(col="precio", origen="MXN", destino="USD")

Ayuda:
    from moneymap import ayuda
    ayuda()              # índice de todas las funciones
    ayuda("convertir")   # detalle de una función específica
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

__version__ = "0.1.5"
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
    # Módulos opcionales (no se importan aquí para no forzar dependencias)
    # "dataframepd"  →  import moneymap.dataframepd  (requiere pandas)
    # "dataframepl" →  import moneymap.dataframepl  (requiere polars)
]
