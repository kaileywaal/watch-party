import unittest


def run_tests():
    loader = unittest.TestLoader()
    start_dir = "src/tests"
    suite = loader.discover(start_dir)
    runner = unittest.TextTestRunner()
    result = runner.run(suite)
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    if not success:
        exit(1)
