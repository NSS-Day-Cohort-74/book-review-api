import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import Reviews


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for shipping ships"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "reviews":
            if url["pk"] == 0:
                # Get all rows happen here
                reviews = Reviews()
                all_reviews_json_string = reviews.get_all()
                return self.response(all_reviews_json_string, status.HTTP_200_SUCCESS)
            else:
                # Get single row should happen here
                return self.response(None, status.HTTP_200_SUCCESS)
        else:
            return self.response("", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)

    def do_PUT(self):
        """Handle PUT requests from a client"""

        # Parse the URL and get the primary key
        url = self.parse_url(self.path)
        pk = url["pk"]

        # Get the request body JSON for the new data
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        if url["requested_resource"] == "cookies":
            if pk != 0:
                pass


    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "books":
            if pk != 0:
                removed = True
                if removed:
                    return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
                else:
                    return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
        else:
            return self.response("Not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)

    def do_POST(self):
        """Handle POST requests from a client"""

        # Get the request body JSON for the new data
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        bettys_bake_shop = BakeShop()

        url = self.parse_url(self.path)

        return self.response(None, status.HTTP_201_SUCCESS_CREATED)




#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()