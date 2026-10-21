"""Convert length, mass, and temperature between common units."""

import argparse
import sys

LENGTH_TO_METERS = {
    "m": 1.0,
    "km": 1000.0,
    "cm": 0.01,
    "ft": 0.3048,
    "in": 0.0254,
    "mi": 1609.344,
}

MASS_TO_KILOGRAMS = {
    "kg": 1.0,
    "g": 0.001,
    "lb": 0.45359237,
    "oz": 0.028349523125,
}

TEMPERATURE_UNITS = ("c", "f", "k")

UNIT_ALIASES = {
    "meter": "m",
    "meters": "m",
    "metre": "m",
    "metres": "m",
    "kilometer": "km",
    "kilometers": "km",
    "kilometre": "km",
    "kilometres": "km",
    "centimeter": "cm",
    "centimeters": "cm",
    "centimetre": "cm",
    "centimetres": "cm",
    "foot": "ft",
    "feet": "ft",
    "inch": "in",
    "inches": "in",
    "mile": "mi",
    "miles": "mi",
    "kilogram": "kg",
    "kilograms": "kg",
    "gram": "g",
    "grams": "g",
    "pound": "lb",
    "pounds": "lb",
    "ounce": "oz",
    "ounces": "oz",
    "celsius": "c",
    "fahrenheit": "f",
    "kelvin": "k",
}


class UnitError(ValueError):
    """Raised when a value or unit cannot be converted."""


def _canonical(unit):
    key = unit.strip().lower()
    return UNIT_ALIASES.get(key, key)


def _convert_linear(value, from_unit, to_unit, table, kind):
    source = _canonical(from_unit)
    target = _canonical(to_unit)
    if source not in table or target not in table:
        known = ", ".join(sorted(table))
        raise UnitError(f"Unknown {kind} unit. Use one of: {known}.")
    if value < 0:
        raise UnitError(f"{kind.capitalize()} cannot be negative.")
    return value * table[source] / table[target]


def _to_celsius(value, unit):
    if unit == "c":
        return value
    if unit == "f":
        return (value - 32) * 5 / 9
    if unit == "k":
        return value - 273.15
    known = ", ".join(TEMPERATURE_UNITS)
    raise UnitError(f"Unknown temperature unit. Use one of: {known}.")


def _from_celsius(value, unit):
    if unit == "c":
        return value
    if unit == "f":
        return value * 9 / 5 + 32
    if unit == "k":
        return value + 273.15
    known = ", ".join(TEMPERATURE_UNITS)
    raise UnitError(f"Unknown temperature unit. Use one of: {known}.")


def convert_length(value, from_unit, to_unit):
    return _convert_linear(value, from_unit, to_unit, LENGTH_TO_METERS, "length")


def convert_mass(value, from_unit, to_unit):
    return _convert_linear(value, from_unit, to_unit, MASS_TO_KILOGRAMS, "mass")


def convert_temperature(value, from_unit, to_unit):
    source = _canonical(from_unit)
    target = _canonical(to_unit)
    return _from_celsius(_to_celsius(value, source), target)


def convert(value, from_unit, to_unit):
    """Convert value between two units in the same category."""
    source = _canonical(from_unit)
    target = _canonical(to_unit)
    if source in LENGTH_TO_METERS or target in LENGTH_TO_METERS:
        return convert_length(value, source, target)
    if source in MASS_TO_KILOGRAMS or target in MASS_TO_KILOGRAMS:
        return convert_mass(value, source, target)
    if source in TEMPERATURE_UNITS or target in TEMPERATURE_UNITS:
        return convert_temperature(value, source, target)
    raise UnitError(f"Unknown unit {from_unit!r} or {to_unit!r}.")


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Convert length, mass, and temperature."
    )
    parser.add_argument("value", type=float)
    parser.add_argument("from_unit")
    parser.add_argument("to_unit")
    args = parser.parse_args(argv)
    try:
        result = convert(args.value, args.from_unit, args.to_unit)
    except UnitError as exc:
        print(exc, file=sys.stderr)
        return 1
    print(format(result, ".10g"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
