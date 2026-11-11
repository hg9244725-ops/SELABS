
import pytest
from fuel_station import fuel_bill, pump_allowed, session_status


# ---------------- FUEL BILL TESTS ----------------

def test_within_covered_litres():
    assert fuel_bill("regular", 8, "silver") == 0


def test_unknown_fuel_grade():
    with pytest.raises(ValueError):
        fuel_bill("petrol", 20, "silver")


def test_negative_litres():
    with pytest.raises(ValueError):
        fuel_bill("regular", -5, "silver")


def test_gold_customer_extra_coverage():
    assert fuel_bill("regular", 15, "gold") == 0


def test_regular_fuel_bill():
    assert fuel_bill("regular", 20, "silver") == 1050


def test_diesel_fuel_bill():
    assert fuel_bill("diesel", 30, "silver") == 900


def test_large_extra_litres_discount():
    assert fuel_bill("regular", 50, "silver") == 3960


def test_gold_customer_large_purchase():
    assert fuel_bill("regular", 60, "gold") == 4275


def test_gold_diesel_large_purchase():
    assert fuel_bill("diesel", 60, "gold") == 3200


# ---------------- PUMP ALLOWED TESTS ----------------

def test_pump_allowed():
    assert pump_allowed(30, 1, False) is True


def test_fleet_within_limit():
    assert pump_allowed(200, 5, True) is True


def test_fleet_exceeds_limit():
    assert pump_allowed(250, 5, True) is False


def test_non_fleet_exceeds_litres():
    assert pump_allowed(70, 1, False) is False


def test_non_fleet_multiple_containers():
    assert pump_allowed(50, 2, False) is False


# ---------------- SESSION STATUS TESTS ----------------

def test_card_payment_active():
    assert session_status(60, True, False) == "active"


def test_cash_payment_active():
    assert session_status(30, False, False) == "active"


def test_night_card_payment_active():
    assert session_status(90, True, True) == "active"


def test_night_cash_payment_active():
    assert session_status(60, False, True) == "active"


def test_card_payment_warning():
    assert session_status(50, True, False) == "warning"


def test_cash_payment_warning():
    assert session_status(20, False, False) == "warning"


def test_night_payment_warning():
    assert session_status(80, True, True) == "warning"


def test_card_payment_timed_out():
    assert session_status(40, True, False) == "timed_out"


def test_cash_payment_timed_out():
    assert session_status(10, False, False) == "timed_out"


def test_night_payment_timed_out():
    assert session_status(60, True, True) == "timed_out"
