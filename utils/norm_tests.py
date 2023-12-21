import pytest
from normalization import LowUpScaller, TimeNormalization
from datetime import datetime


@pytest.fixture
def normalization_obj():
    return LowUpScaller(lower_limit=-80, upper_limit=80)


def test_normalize(normalization_obj):
    original_values = [-60, -40, 0, 20, 40, 60]
    normalized_values = normalization_obj.normalize(original_values)

    assert all(0 <= val <= 1 for val in normalized_values)


def test_denormalize(normalization_obj):
    normalized_values = [0.1, 0.3, 0.5, 0.7, 0.9]
    denormalized_values = normalization_obj.denormalize(normalized_values)

    assert all(-80 <= val <= 80 for val in denormalized_values)


def test_info(capsys, normalization_obj):
    normalization_obj.info()
    captured = capsys.readouterr()
    assert "Normalization range: [-80, 80]" in captured.out


# Запуск тестов
if __name__ == "__main__":
    pytest.main()
