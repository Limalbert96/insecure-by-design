import requests
import time
import concurrent.futures
from datetime import datetime

def make_request(session):
    try:
        start_time = time.time()
        response = session.get('http://<MONGO_VM_IP>')
        end_time = time.time()
        return response.status_code, end_time - start_time
    except Exception as e:
        return str(e), 0

def main():
    duration = 5  # seconds to run the test
    start_time = time.time()
    end_time = start_time + duration
    
    success_count = 0
    error_count = 0
    total_requests = 0
    results = []
    
    print(f"Starting load test at {datetime.now()}")
    print(f"Will run for {duration} seconds...\n")
    
    # Use a single session to maintain the same TCP connection
    session = requests.Session()
    
    while time.time() < end_time:
        # Make concurrent requests
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(make_request, session) for _ in range(20)]
            batch_results = [f.result() for f in futures]
            results.extend(batch_results)
            
            # Process batch results
            for status, req_time in batch_results:
                total_requests += 1
                if isinstance(status, int) and 200 <= status < 300:
                    success_count += 1
                else:
                    error_count += 1
                    print(f"Error response: Status={status}, Time={req_time:.2f}s")
            
            # Small delay to ensure requests aren't coalesced
            time.sleep(0.1)
    
    total_time = time.time() - start_time
    
    print(f"\nTest completed at {datetime.now()}")
    print(f"Summary:")
    print(f"Total Time: {total_time:.2f}s")
    print(f"Total Requests: {total_requests}")
    print(f"Success: {success_count}")
    print(f"Errors: {error_count}")
    print(f"Requests/sec: {total_requests/total_time:.2f}")
    
    # Calculate error rate
    error_rate = (error_count / total_requests) * 100 if total_requests > 0 else 0
    print(f"Error Rate: {error_rate:.2f}%")

if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
