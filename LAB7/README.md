# Lab 7 – Fuel Station

## Lab: Fuzz Testing

### About

A Python module that parses fuel purchases, calculates average pump volumes, and computes payable bills after discounts.

### Files

| File | Description |
|---|---|
| `fuel_station.py` | Application code with input validation |
| `test_fuel_station.py` | Hypothesis-based fuzz tests |
| `README.md` | Lab documentation |

### Testing

The project uses **pytest** and **Hypothesis** to generate different inputs and test the application functions.

The tests cover:
- `parse_purchase()`
- `volume_average()`
- `payable_bill()`

All three fuzz tests pass after input validation was added.