import time

import md.python.measure
import unittest
import unittest.mock


class TestTime:
    def test_measure_with_start_and_exit(self) -> None:  # white/positive
        # arrange
        with unittest.mock.patch('time.monotonic', side_effect=[0.0, 0.4815162342]):
            # act
            with md.python.measure.Time() as measure:
                # assert
                assert measure.start == 0.0
                assert measure.end is None

        # assert
        assert measure.time() == 0.4815162342

    def test_measure_with_start_and_exit_while_measure(self) -> None:  # white/positive
        # arrange
        with unittest.mock.patch('time.monotonic', side_effect=[0.0, 0.4815162342, 0.5]):
            # act
            with md.python.measure.Time() as measure:
                # assert
                assert measure.start == 0.0
                assert measure.end is None
                assert measure.time() == 0.4815162342
            assert measure.time() == 0.5

    def test_measure_without_start(self) -> None:  # white/negative
        # arrange
        with unittest.mock.patch('time.monotonic', side_effect=[0.0, 0.4815162342, 0.5]):
            # act
            measure = md.python.measure.Time()

            # assert
            assert measure.start is None
            assert measure.time() is None

    def test_measure_time_go_backwards_protection(self) -> None:  # white/negative
        # arrange
        with unittest.mock.patch('time.time', side_effect=[0.4815, 0.162342]):
            # act
            with md.python.measure.Time(now=time.time) as measure:
                pass

        # assert
        assert measure.time() == 0.0

    def test_measure_reset_start_on_reuse(self) -> None:  # white/positive
        # arrange
        with unittest.mock.patch('time.monotonic', side_effect=[0.0, 0.4815162342, 0.5, 0.16]):
            # act
            measure = md.python.measure.Time()
            with measure:
                # assert
                assert measure.start == 0.0
            assert measure.end == 0.4815162342

            with measure:
                assert measure.end is None
                assert measure.start == 0.5
            assert measure.end == 0.16
