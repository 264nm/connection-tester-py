# connection-tester-py

A basic script to test TCP/UDP port connecitivity, or http connectivity, when on a host without permission to install net-tools in order to debug.

Due to the nature of the use case, this is python 2.7 compatable.

## Usage

```
usage: connection-tester.py [-h] [-H HOST] [-p PORT] [-t TIMEOUT]
                            [-P {TCP,UDP}] [-e ENDPOINT] [-S] [-v]
                            {http,port}

positional arguments:
  {http,port}           Type of healthcheck to run

optional arguments:
  -h, --help            show this help message and exit
  -H HOST, --host HOST  host to check
  -p PORT, --port PORT  port to check
  -t TIMEOUT, --timeout TIMEOUT
                        set the timeout value
  -P {TCP,UDP}, --protocol {TCP,UDP}
                        PORT CHECK ONLY: protocol to check
  -e ENDPOINT, --endpoint ENDPOINT
                        HTTP CHECK ONLY: endpoint to check i.e /health
  -S, --ssl             HTTP CHECK ONLY: Flag to use HTTPS instead of HTTP
  -v, --verbose         Toggle for debug information
  ```

### Port Check

```
./connection-tester.py port -H github.com -p 443 -P TCP`
SUCCESS: Port Connection Test Succesful for github.com
```

Use the `-v` flag for more information:

```
FAILED: Port Connection Test Failed For github.com
DEBUG: Protocol: TCP
DEBUG: Host: github.com
DEBUG: Port: 443
DEBUG: Error: [Errno 8] nodename nor servname provided, or not known
```

### HTTP Check

Basic check with SSL
```
./connection-tester.py http -H github.com  -S
SUCCESS: HTTP Connection Test Passed For https://github.com/
```

Check HTTPS on port 443 with the endpoint `/264nm/connection-tester-py`

```
./connection-tester.py http -H github.com  -S --port 443 -e /264nm/connection-tester-py -v
SUCCESS: HTTP Connection Test Passed For https://github.com:443/264nm/connection-tester-py
DEBUG: Info: https://github.com:443/264nm/connection-tester-py
DEBUG: Status Code: 200
DEBUG: Error Type: None
```
# connection-tester-py
