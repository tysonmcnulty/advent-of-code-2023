from pathlib import Path


def load(data_file: Path):
    calibration_values = []
    with open(data_file) as calibration_data:
        for line in calibration_data:
            pass

    return calibration_values
