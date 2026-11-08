""" 
Class to check the performance of an API route by sending multiple requests and measuring the response time.
"""

import requests
import time
import argparse
import statistics
import sys
import os
from dotenv import load_dotenv


class PerformanceChecker():

    def __init__(self, url, count=5, api_key=None):
        self.url = url
        self.count = count
        self.api_key = api_key

    def run(self):
        """ Run the performance check """
        parser = argparse.ArgumentParser(description="Check the performance of an API route.")
        parser.add_argument("url", nargs="?", help="The URL of the API route to check.")
        parser.add_argument("-c", "--count", type=int, default=5, help="Number of requests (default: 5).")
            
        args = parser.parse_args()
        load_dotenv()
        url = args.url or os.getenv("BASE_URL")
        api_key = os.getenv("API_KEY")
        
        if not url:
            parser.error("provide a URL argument or set BASE_URL in .env")
    
        if not url.startswith("http"):
            print("Error: The URL must start with http:// or https://.")
            sys.exit(1)

        if not api_key:
            print("INFO: You might be unathorized without an API key. Consider setting the API_KEY in your .env file.")
            
        self.check_performance()

    def check_performance(self):
        """ Check the performance of an API route by sending multiple requests """
        print("Checking performance for: %s" % self.url)
        print("Number of requests: %d" % self.count)
        print("-" * 40)

        latencies = []
        headers = {"X-API-Key": self.api_key} if self.api_key else {}
        
        for i in range(self.count):
            try:
                start_time = time.perf_counter()
                response = requests.get(self.url, headers=headers, timeout=10)
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
