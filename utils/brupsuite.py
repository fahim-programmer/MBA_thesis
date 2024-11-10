from urllib.parse import urlparse, parse_qs
import requests

class BurpRequest:
    def __init__(self, request_body:str):
        self.request = request_body
        payload_ =  self.__internal_parser(self.request)
        self.url = "https://" + payload_["headers"]["Host"] + payload_["url"]
        self.headers = payload_["headers"]
        self.params = payload_["params"]

    def __internal_parser(self, request):
        lines = request.strip().splitlines()
        # First line should contain method, path, and HTTP version
        method_line = lines[0].split()
        method = method_line[0]
        full_path = method_line[1]
        # Parse URL and query parameters
        url_parts = urlparse(full_path)
        endpoint = url_parts.path
        params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(url_parts.query).items()}
        # Parse headers
        headers = {}
        for line in lines[1:]:
            if line == "":  # Empty line indicates end of headers
                break
            key, value = line.split(": ", 1)
            headers[key] = value
        # If it's a POST request, extract body as params if content-type is application/x-www-form-urlencoded
        body = ""
        if method == "POST":
            # Find the index of the empty line separating headers from body
            empty_line_index = lines.index("")
            body = "\n".join(lines[empty_line_index + 1:])
            if headers.get("Content-Type") == "application/x-www-form-urlencoded":
                post_params = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(body).items()}
                params.update(post_params)
        # Build the result dictionary
        parsed_request = {
            "url": endpoint,
            "params": params,
            "headers": headers
        }
        return parsed_request