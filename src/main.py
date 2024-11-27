from pipeline import Pipeline
from error_correction_code import ErrorCorrectionCode
def main():
    image_path = "../data/input/sample1.bmp"  # Ścieżka do obrazu wejściowego
    output_path = "../data/output/output_image.bmp"  # Ścieżka do obrazu po transmisji
    pipeline = Pipeline(image_path=image_path, output_path=output_path)
    pipeline.select_type()


def test_no_errors():
    ecc = ErrorCorrectionCode(symbols=10)
    original_data = b'Test data for Reed-Solomon coding.'
    encoded_data = ecc.encode(original_data)
    decoded_data = ecc.decode(encoded_data)

    if decoded_data == original_data:
        print("Test bez błędów: Sukces")
    else:
        print("Test bez błędów: Niepowodzenie")


if __name__ == "__main__":
    main()
    # test_no_errors()




