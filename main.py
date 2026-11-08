import requests
import time
import argparse
import statistics
import sys

def check_performance(url, count):
    print("Checking performance for: %s" % url)
    print("Number of requests: %d" % count)
    print("-" * 40)

    latencies = []
    
    for i in range(count):
        try:
            start_time = time.perf_counter()
            response = requests.get(url, timeout=10)
            end_time = time.perf_counter()
            
            latency = (end_time - start_time) * 1000  # in milliseconds
            latencies.append(latency)
            
            print("Request %d: Status %d, Time: %.2f ms" % (i + 1, response.status_code, latency))
        except requests.exceptions.RequestException as e:
            print("Request %d: Error - %s" % (i + 1, e))

    if not latencies:
        print("No successful requests performed.")
        return

    print("-" * 40)
    print("Results:")
    print("Average:   %.2f ms" % statistics.mean(latencies))
    print("Minimum:   %.2f ms" % min(latencies))
    print("Maximum:   %.2f ms" % max(latencies))
    if len(latencies) > 1:
        print("Std Dev:   %.2f ms" % statistics.stdev(latencies))

def main():
    parser = argparse.ArgumentParser(description="Check the performance of an API route.")
    parser.add_argument("url", help="The URL of the API route to check.")
    parser.add_argument("-c", "--count", type=int, default=5, help="Number of requests (default: 5).")
    
    args = parser.parse_args()
    
    if not args.url.startswith("http"):
        print("Error: The URL must start with http:// or https://.")
        sys.exit(1)
        
    check_performance(args.url, args.count)

if __name__ == "__main__":
    main()
