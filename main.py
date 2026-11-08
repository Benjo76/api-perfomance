from src import PerformanceChecker

if __name__ == "__main__":
    checker = PerformanceChecker(url=None)  # URL will be provided via command line or .env
    checker.run()
