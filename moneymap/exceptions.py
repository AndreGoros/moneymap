"""
Excepciones personalizadas para MoneyMap.
"""


class MoneyMapError(Exception):
    """Excepción base para todos los errores de MoneyMap."""
    pass


class DivisaNoSoportadaError(MoneyMapError):
    """Se lanza cuando se usa un código de divisa no registrado."""

    def __init__(self, divisa: str):
        self.divisa = divisa
        super().__init__(
            f"La divisa '{divisa}' no está soportada. "
            f"Usa divisas_disponibles() para ver las opciones."
        )


class PaisNoSoportadoError(MoneyMapError):
    """Se lanza cuando se usa un país sin reglas fiscales registradas."""

    def __init__(self, pais: str):
        self.pais = pais
        super().__init__(
            f"El país '{pais}' no tiene reglas fiscales registradas. "
            f"Usa paises_disponibles() para ver las opciones."
        )


class TasaInvalidaError(MoneyMapError):
    """Se lanza cuando se intenta registrar una tasa de cambio inválida."""

    def __init__(self, tasa, razon: str = ""):
        self.tasa = tasa
        mensaje = f"La tasa de cambio '{tasa}' es inválida."
        if razon:
            mensaje += f" {razon}"
        super().__init__(mensaje)


class MontoInvalidoError(MoneyMapError):
    """Se lanza cuando el monto proporcionado no es válido."""

    def __init__(self, monto, razon: str = ""):
        self.monto = monto
        mensaje = f"El monto '{monto}' no es válido."
        if razon:
            mensaje += f" {razon}"
        super().__init__(mensaje)
