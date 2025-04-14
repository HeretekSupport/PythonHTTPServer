import socket
import re

# Global var for HTTP headers
HTTP_METHODS: tuple = ('GET', 'POST', 'PUT', 'HEAD', 'DELETE', 'CONNECT', 'OPTIONS', 'TRACE', 'PATCH')
HTTP_VERSION: str = '1.1'
HTTP_SUCCESS_CODES: dict = {
    '200' : 'OK'
}
HTTP_ERROR_CODES: dict = {
    '400' : 'Bad Request',
    '401' : 'Unauthorized',
    '403' : 'Forbidden',
    '404' : 'Not Found',
    '500' : 'Internal Server Error',    
    }
HTTP_CRLF: str = '\r\n'

def main():

    # Create a local server socket that listens on port 4221
    server_socket = socket.create_server(("localhost", 4221))

    # The accept method returns a new socket and the address of the client
    # I capture those in vars and use the client socket to send a response    
    client_socket, client_address = server_socket.accept()
    print(f"Connection from {client_address}")


    # Receive and decode client request to string
    request = client_socket.recv(1024).decode('utf-8')
    response = ''
    print(f"Received request: {request}")
    print(f"Object type of request is {type(request)}")
    
    def validate_request_line(request_line: str) -> bool:
        """
        Validates HTTP request line using regex for
        'METHOD /path HTTP/1.x' format
        """
        pattern = r'(GET|POST|PUT|DELETE|OPTIONS|TRACE|PATCH) /[^\s]* HTTP/\d\.\d$'
        if re.match(pattern, request_line):
            return True
        else:
            return False

    def extract_request_line(request: str) -> dict:
        """
        Takes in a string formatted request, validates
        if it matches a proper HTTP request line, then parses
        and returns a dictionary with 'method', 'path', and 'version' keys.

        Splits by space for each line. 

        Zips together each element to a value in the line list.
        """
        request_elements = {'method': '', 'path': '', 'version':''}
        
        if validate_request_line(request):
            request_lines = request.split(' ')
            for k,v in zip(request_elements.keys(), request_lines):
                request_elements[k] = v

        return request_elements
    
    def validate_path(path: str) -> bool: # This is just to satisfy the simple objective or returning success if path is just root
        """
        Checks if path refers to valid file on server.

        NOTE: Mostly a stub for now checking for root path.
        """
        if path == '/':
            return True
        else:
            return False
        
    request_line = extract_request_line(request)
    if validate_path(request_line['path']):
        response = f"HTTP/{HTTP_VERSION} 200 {HTTP_SUCCESS_CODES['200']}{HTTP_CRLF}"
    else:
        response = f"HTTP/{HTTP_VERSION} 404 {HTTP_ERROR_CODES['404']}{HTTP_CRLF}"


    client_socket.send(response.encode())
    client_socket.close()
    server_socket.close()

if __name__ == '__main__':
    main()