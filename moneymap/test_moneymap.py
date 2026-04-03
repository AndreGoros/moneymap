"""
Suite de pruebas para MoneyMap.

Cubre: conversiones de divisas, cálculo de impuestos,
registro de tasas, y manejo de errores.
"""

import pytest
from decimal import Decimal

from moneymap import (
    convertir,
    registrar_tasa,
    divisas_disponibles,
    impuesto,
    paises_disponibles,
)
from moneymap.taxes import total_con_impuesto, tasa_fiscal
from moneymap.exceptions import (
    DivisaNoSoportadaError,
    PaisNoSoportadoError,
    MontoInvalidoError,
    TasaInvalidaError,
)
from moneymap.currency import _TASAS_BASE  # sólo para tests de estado interno


# ===========================================================================
# Tests de conversión de divisas
# ===========================================================================

class TestConvertir:

    def test_misma_divisa_retorna_mismo_monto(self):
        resultado = convertir(100, "USD", "USD")
        assert resultado == Decimal("100.00")

    def test_conversion_mxn_a_usd(self):
        # 1000 MXN / 17.05 MXN/USD = ~58.65 USD
        resultado = convertir(1000, "MXN", "USD")
        assert resultado == Decimal("58.65")

    def test_conversion_usd_a_mxn(self):
        # 100 USD * 17.05 = 1705.00 MXN
        resultado = convertir(100, "USD", "MXN")
        assert resultado == Decimal("1705.00")

    def test_conversion_acepta_int(self):
        resultado = convertir(100, "USD", "EUR")
        assert isinstance(resultado, Decimal)

    def test_conversion_acepta_float(self):
        resultado = convertir(100.50, "USD", "EUR")
        assert isinstance(resultado, Decimal)

    def test_conversion_acepta_string(self):
        resultado = convertir("100", "USD", "EUR")
        assert isinstance(resultado, Decimal)

    def test_conversion_acepta_decimal(self):
        resultado = convertir(Decimal("100"), "USD", "EUR")
        assert isinstance(resultado, Decimal)

    def test_conversion_mayusculas_minusculas(self):
        resultado_upper = convertir(100, "USD", "MXN")
        resultado_lower = convertir(100, "usd", "mxn")
        assert resultado_upper == resultado_lower

    def test_conversion_monto_cero(self):
        resultado = convertir(0, "USD", "MXN")
        assert resultado == Decimal("0.00")

    def test_conversion_divisa_origen_invalida(self):
        with pytest.raises(DivisaNoSoportadaError) as exc_info:
            convertir(100, "XYZ", "USD")
        assert "XYZ" in str(exc_info.value)

    def test_conversion_divisa_destino_invalida(self):
        with pytest.raises(DivisaNoSoportadaError) as exc_info:
            convertir(100, "USD", "ABC")
        assert "ABC" in str(exc_info.value)

    def test_conversion_monto_negativo(self):
        with pytest.raises(MontoInvalidoError):
            convertir(-100, "USD", "MXN")

    def test_conversion_monto_string_invalido(self):
        with pytest.raises(MontoInvalidoError):
            convertir("no_es_numero", "USD", "MXN")

    def test_resultado_tiene_dos_decimales(self):
        resultado = convertir(1, "USD", "JPY")
        # El resultado debe estar cuantizado a 2 decimales
        assert resultado == resultado.quantize(Decimal("0.01"))


# ===========================================================================
# Tests de divisas disponibles
# ===========================================================================

class TestDivisasDisponibles:

    def test_retorna_lista(self):
        resultado = divisas_disponibles()
        assert isinstance(resultado, list)

    def test_incluye_divisas_base(self):
        disponibles = divisas_disponibles()
        for divisa in ["USD", "MXN", "EUR", "GBP", "CAD"]:
            assert divisa in disponibles

    def test_esta_ordenada(self):
        disponibles = divisas_disponibles()
        assert disponibles == sorted(disponibles)


# ===========================================================================
# Tests de registro de tasas
# ===========================================================================

class TestRegistrarTasa:

    def test_registrar_nueva_divisa(self):
        registrar_tasa("VEF", "USD", 35.50)
        assert "VEF" in divisas_disponibles()

    def test_actualizar_divisa_existente(self):
        registrar_tasa("MXN", "USD", 20.00)
        resultado = convertir(100, "USD", "MXN")
        assert resultado == Decimal("2000.00")
        # Restaurar valor original para no afectar otros tests
        registrar_tasa("MXN", "USD", 17.05)

    def test_tasa_negativa_lanza_error(self):
        with pytest.raises(TasaInvalidaError):
            registrar_tasa("TST", "USD", -5)

    def test_tasa_cero_lanza_error(self):
        with pytest.raises(TasaInvalidaError):
            registrar_tasa("TST", "USD", 0)

    def test_tasa_string_invalido_lanza_error(self):
        with pytest.raises(TasaInvalidaError):
            registrar_tasa("TST", "USD", "no_es_numero")

    def test_referencia_no_soportada_lanza_error(self):
        with pytest.raises(DivisaNoSoportadaError):
            registrar_tasa("TST", "XYZ", 10)


# ===========================================================================
# Tests de impuestos
# ===========================================================================

class TestImpuesto:

    def test_impuesto_mexico(self):
        # IVA México = 16%
        resultado = impuesto(1000, "Mexico")
        assert resultado == Decimal("160.00")

    def test_impuesto_cero(self):
        resultado = impuesto(0, "Mexico")
        assert resultado == Decimal("0.00")

    def test_impuesto_acepta_int(self):
        resultado = impuesto(100, "Mexico")
        assert isinstance(resultado, Decimal)

    def test_impuesto_acepta_float(self):
        resultado = impuesto(100.50, "Mexico")
        assert isinstance(resultado, Decimal)

    def test_impuesto_acepta_string(self):
        resultado = impuesto("100", "Mexico")
        assert isinstance(resultado, Decimal)

    def test_impuesto_pais_invalido(self):
        with pytest.raises(PaisNoSoportadoError) as exc_info:
            impuesto(1000, "PaisFantasia")
        assert "PaisFantasia" in str(exc_info.value)

    def test_impuesto_monto_negativo(self):
        with pytest.raises(MontoInvalidoError):
            impuesto(-500, "Mexico")

    def test_impuesto_monto_string_invalido(self):
        with pytest.raises(MontoInvalidoError):
            impuesto("abc", "Mexico")

    def test_resultado_tiene_dos_decimales(self):
        resultado = impuesto(333, "Mexico")
        assert resultado == resultado.quantize(Decimal("0.01"))

    def test_multiples_paises(self):
        """Verifica que cada país use su propia tasa."""
        monto = Decimal("1000")
        paises_tasas = {
            "Mexico": Decimal("160.00"),   # 16%
            "Argentina": Decimal("210.00"), # 21%
            "USA": Decimal("0.00"),         # 0%
            "Suecia": Decimal("250.00"),    # 25%
        }
        for pais, esperado in paises_tasas.items():
            assert impuesto(monto, pais) == esperado


# ===========================================================================
# Tests de total con impuesto
# ===========================================================================

class TestTotalConImpuesto:

    def test_total_mexico(self):
        # 1000 + 16% = 1160
        resultado = total_con_impuesto(1000, "Mexico")
        assert resultado == Decimal("1160.00")

    def test_total_usa_sin_iva(self):
        # USA no tiene IVA federal (0%)
        resultado = total_con_impuesto(1000, "USA")
        assert resultado == Decimal("1000.00")

    def test_total_igual_monto_mas_impuesto(self):
        monto = 500
        pais = "España"
        assert total_con_impuesto(monto, pais) == Decimal(str(monto)) + impuesto(monto, pais)


# ===========================================================================
# Tests de tasa fiscal
# ===========================================================================

class TestTasaFiscal:

    def test_tasa_mexico(self):
        assert tasa_fiscal("Mexico") == Decimal("16")

    def test_tasa_pais_invalido(self):
        with pytest.raises(PaisNoSoportadoError):
            tasa_fiscal("PaisInventado")


# ===========================================================================
# Tests de países disponibles
# ===========================================================================

class TestPaisesDisponibles:

    def test_retorna_lista(self):
        resultado = paises_disponibles()
        assert isinstance(resultado, list)

    def test_incluye_paises_base(self):
        disponibles = paises_disponibles()
        for pais in ["Mexico", "Argentina", "España", "USA"]:
            assert pais in disponibles

    def test_esta_ordenada(self):
        disponibles = paises_disponibles()
        assert disponibles == sorted(disponibles)
