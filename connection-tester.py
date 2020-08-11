#!/usr/bin/env python
"""CLI util for performing connectivity checks."""
import argparse
import urllib2
from urllib2 import URLError, HTTPError
import socket


class PortChecker:
    """
    Class to check if a port is open on a given host.

    Attributes:
        host (str): Hostname or IP address
        port (int): Port to check
        proto (str): TCP or UDP protocol to check
        verbose (bool): Trigger debug output
    """

    def __init__(self, host, port, proto='TCP', verbose=False):
        self.host = host
        self.port = port
        self.proto = proto
        self.verbose = verbose

    @staticmethod
    def _create_socket(protocol):
        """
        Initialise the socket based on protocol.

        Args:
            protocol (str): TCP or UDP protocol

        Returns:
            socket object
        """
        if protocol.upper() == 'TCP':
            return socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        elif protocol.upper() == 'UDP':
            return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def _check_connection(self):
        """
        Connect to the remote host.

        Returns:
            Dict[str, Any]
            Results and error if failed

        >>> { 'success': False, 'error': socket.aierror }
        >>> { 'success': True. 'error': None }
        """
        s = self._create_socket(self.proto)
        try:
            s.connect((self.host, self.port))
            return {'success': True, 'error': None}
        except (socket.error, socket.gaierror, socket.herror) as e:
            return {'success': False, 'error': e}

    def check(self):
        """Public method to class. Returns human readable output."""
        result = self._check_connection()
        if result['success']:
            print('SUCCESS: Port Connection Test Succesful for ' + self.host)
        else:
            print('FAILED: Port Connection Test Failed For ' + self.host)

        if self.verbose:
            print 'DEBUG: Protocol: ' + self.proto
            print 'DEBUG: Host: ' + self.host
            print 'DEBUG: Port: ' + str(self.port)
            print 'DEBUG: Error: ' + str(result['error'])


class HTTPChecker(object):
    """
    Perform a HTTP Check.

    Attributes:
        host (str): hostname or IP address
        endpoint (str): endpoint i.e /health
        port (Optional[int]): port the server runs on if not 443/80
        ssl (bool): Whether to check SSL
        verbose (bool): Toggle debug output
    """

    def __init__(self, host, endpoint, port=None, ssl=False, verbose=False):
        self.host = host
        self.port = port
        self.ssl = ssl
        self.endpoint = endpoint
        self.verbose = verbose
        self.url = self._build_url()

    def _is_ssl(self):
        """
        Convert ssl boolean to http or https and default to http.

        Returns:
            (str) http or https
        """
        return 'https' if self.ssl else 'http'

    def _build_url(self):
        """
        Build the URL to perform the check against.

        Returns:
            (str) the full URL
        >>> https://github.com:443/someendpoint
        """
        proto = self._is_ssl()
        endpoint = self.endpoint if self.endpoint else ''
        if self.port:
            return proto + '://' + self.host + ':' + str(self.port) + endpoint
        else:
            return proto + '://' + self.host + endpoint

    @staticmethod
    def _open_url(url):
        """
        Performs the HTTP request.

        Args:
            url (str) - URL to check

        Returns:
            Response or Error Object
        """
        try:
            req = urllib2.Request(url)
            res = urllib2.urlopen(req)
        except (HTTPError, URLError) as e:
            return e
        return res

    def _check_connection(self):
        """
        Wrapper for the URL opener to return a results dictionary.

        Returns:
            (Dict[str, Any])
            Dictionary contain status as a bool, debug message,
            HTTP status code or error code, and Error type optional.
        """
        res = self._open_url(self.url)
        result = {}
        if isinstance(res, HTTPError):
            result = {'success': False, 'debug': res.msg,
                      'status': res.code, 'error_type': res}
        elif isinstance(res, URLError):
            result = {'success': False, 'debug': res.reason,
                      'status': res.code, 'error_type': res}
        else:
            result = {'success': True, 'debug': res.geturl(
            ), 'status': res.getcode(), 'error_type': None}

        return result

    def check(self):
        """
        Public method for class. Prints human readable output.
        """
        result = self._check_connection()
        if result['success']:
            print('SUCCESS: HTTP Connection Test Passed For ' + self.url)
        else:
            print('FAILED: HTTP Connection Test Failed for ' + self.url)

        if self.verbose:
            print 'DEBUG: Info: ' + result['debug']
            print 'DEBUG: Status Code: ' + str(result['status'])
            print 'DEBUG: Error Type: ' + str(result['error_type'])


def get_args():
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'check', choices=['http', 'port'], help='Type of healthcheck to run')
    parser.add_argument('-H', '--host', type=str, help='host to check')
    parser.add_argument('-p', '--port', type=int, help='port to check')
    parser.add_argument('-t', '--timeout', type=int,
                        help='set the timeout value', default=3)
    parser.add_argument('-P', '--protocol', type=str,
                        help='PORT CHECK ONLY: protocol to check', choices=['TCP', 'UDP'], default='TCP')
    parser.add_argument('-e', '--endpoint', type=str,
                        help='HTTP CHECK ONLY: endpoint to check i.e /health', default='/')
    parser.add_argument('-S', '--ssl', action='store_true',
                        help='HTTP CHECK ONLY: Flag to use HTTPS instead of HTTP')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='Toggle for debug information')
    return parser.parse_args()


def main():
    """Main function/entrypoint."""
    args = get_args()
    socket.setdefaulttimeout(args.timeout)
    if args.check == 'http':
        checker = HTTPChecker(args.host, args.endpoint,
                              args.port, args.ssl, args.verbose)
    if args.check == 'port':
        checker = PortChecker(args.host, args.port,
                              args.protocol, args.verbose)

    checker.check()


if __name__ == '__main__':
    main()
