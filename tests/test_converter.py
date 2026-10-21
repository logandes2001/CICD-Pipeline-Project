import pytest

from converter import UnitError, convert, main


def test_feet_to_inches():
    assert convert(1, "ft", "in") == pytest.approx(12)


def test_kilometers_to_miles():
    assert convert(1, "km", "mi") == pytest.approx(0.6213711922)


def test_length_accepts_full_names():
    assert convert(2, "meters", "centimeters") == pytest.approx(200)


def test_same_length_unit_returns_the_value():
    assert convert(5, "m", "m") == pytest.approx(5)


def test_pounds_to_ounces():
    assert convert(1, "lb", "oz") == pytest.approx(16)


def test_kilograms_to_grams():
    assert convert(1.5, "kg", "g") == pytest.approx(1500)


def test_freezing_point():
    assert convert(0, "c", "f") == pytest.approx(32)
    assert convert(0, "celsius", "kelvin") == pytest.approx(273.15)


def test_boiling_point():
    assert convert(100, "c", "f") == pytest.approx(212)


def test_temperature_round_trip():
    assert convert(convert(20, "c", "f"), "f", "c") == pytest.approx(20)


def test_negative_length_is_rejected():
    with pytest.raises(UnitError, match="cannot be negative"):
        convert(-1, "m", "ft")


def test_mixed_categories_are_rejected():
    with pytest.raises(UnitError, match="Unknown length unit"):
        convert(1, "m", "kg")


def test_unknown_unit_is_rejected():
    with pytest.raises(UnitError, match="Unknown unit"):
        convert(1, "furlong", "smoot")


def test_cli_prints_freezing_point_in_fahrenheit(capsys):
    assert main(["0", "c", "f"]) == 0
    assert capsys.readouterr().out.strip() == "32"


def test_cli_reports_an_invalid_conversion(capsys):
    assert main(["1", "m", "kg"]) == 1
    assert "Unknown length unit" in capsys.readouterr().err
