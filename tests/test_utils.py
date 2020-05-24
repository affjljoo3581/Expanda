from expanda.utils import random_filename, random_filenames


def test_generate_correct_filenames():
    # Check for single generation.
    assert len(random_filename('')) == 16
    assert random_filename('parent').startswith('parent')

    # Check for multiple generations.
    filenames = random_filenames('', n=4)
    assert len(filenames) == 4
    for name in filenames:
        assert len(name) == 16

    filenames = random_filenames('parent', n=4)
    for name in filenames:
        assert name.startswith('parent')
