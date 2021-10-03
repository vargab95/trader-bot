import unittest

from exchange.interface import ExchangeInterface


class TestFloor(unittest.TestCase):
    def test_floor_zero(self):
        self.assertAlmostEqual(ExchangeInterface.floor(0.0, 0.001), 0.0)

    def test_floor_with_a_small_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(0.0000001, 0.001), 0.0)

    def test_floor_with_a_small_negative_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-0.0000001, 0.001), 0.0)

    def test_floor_above_half_precision_with_a_small_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(0.00051, 0.001), 0.0)

    def test_floor_below_half_precision_with_a_small_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(0.00049, 0.001), 0.0)

    def test_floor_above_precision_with_a_small_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(0.0010001, 0.001), 0.001)

    def test_floor_below_precision_with_a_small_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(0.0009999, 0.001), 0.0)

    def test_floor_above_half_precision_with_a_small_negative_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-0.00051, 0.001), 0.0)

    def test_floor_below_half_precision_with_a_small_negative_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-0.00049, 0.001), 0.0)

    def test_floor_above_precision_with_a_small_negative_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-0.0010001, 0.001), -0.001)

    def test_floor_below_precision_with_a_small_negative_amount(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-0.0009999, 0.001), 0.0)

    def test_floor_big_positive_value(self):
        self.assertAlmostEqual(ExchangeInterface.floor(1.234, 0.001), 1.234)

    def test_floor_big_negative_value(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-1.234, 0.001), -1.234)

    def test_floor_big_positive_value_with_below_precision_part(self):
        self.assertAlmostEqual(ExchangeInterface.floor(1.23456, 0.001), 1.234)

    def test_floor_big_negative_value_with_below_precision_part(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-1.23456, 0.001), -1.234)

    def test_floor_big_positive_value_with_below_precision_part_and_zero_before(self):
        self.assertAlmostEqual(ExchangeInterface.floor(1.230456, 0.001), 1.23)

    def test_floor_big_negative_value_with_below_precision_part_and_zero_before(self):
        self.assertAlmostEqual(ExchangeInterface.floor(-1.230456, 0.001), -1.23)


if __name__ == "__main__":
    unittest.main()
