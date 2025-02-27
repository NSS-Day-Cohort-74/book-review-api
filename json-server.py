import json
from http.server import HTTPServer
from nss_handler import HandleRequests, status


# Add your imports below this line
from views import Reviews, Books, Categories


class JSONServer(HandleRequests):
    """Server class to handle incoming HTTP requests for Jane's Reviews"""

    def do_GET(self):
        """Handle GET requests from a client"""

        response_body = ""
        url = self.parse_url(self.path)

        if url["requested_resource"] == "reviews":
            reviews = Reviews()
            if url["pk"] == 0:
                # Get all reviews
                response_body = reviews.get_all()
                return self.response(response_body, status.HTTP_200_SUCCESS)
            else:
                # Get single review
                response_body = reviews.get_single(url["pk"])
                if response_body is not None:
                    return self.response(response_body, status.HTTP_200_SUCCESS)
                else:
                    return self.response("Review not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
        elif url["requested_resource"] == "books":
            books = Books()
            if url["pk"] == 0:
                # Get all books
                response_body = books.get_all()
                return self.response(response_body, status.HTTP_200_SUCCESS)
            else:
                # Get single book
                response_body = books.get_single(url["pk"])
                if response_body is not None:
                    return self.response(response_body, status.HTTP_200_SUCCESS)
                else:
                    return self.response("Book not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
        elif url["requested_resource"] == "categories":
            categories = Categories()
            if url["pk"] == 0:
                # Get all categories
                response_body = categories.get_all()
                return self.response(response_body, status.HTTP_200_SUCCESS)
            else:
                return self.response("Individual category retrieval not implemented", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
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

        if url["requested_resource"] == "books":
            if pk != 0:
                books = Books()
                updated = books.update(pk, request_body)
                if updated:
                    return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
                else:
                    return self.response("Book not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
        else:
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)


    def do_DELETE(self):
        """Handle DELETE requests from a client"""

        url = self.parse_url(self.path)
        pk = url["pk"]

        if url["requested_resource"] == "reviews":
            if pk != 0:
                reviews = Reviews()
                removed = reviews.delete(pk)
                if removed:
                    return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
                else:
                    return self.response("Review not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)

        elif url["requested_resource"] == "books":
            if pk != 0:
                books = Books()
                removed = books.delete(pk)
                if removed:
                    return self.response(None, status.HTTP_204_SUCCESS_NO_RESPONSE_BODY)
                else:
                    return self.response("Book not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)
        else:
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)

    def do_POST(self):
        """Handle POST requests from a client"""

        # Get the request body JSON for the new data
        content_len = int(self.headers.get('content-length', 0))
        request_body = self.rfile.read(content_len)
        request_body = json.loads(request_body)

        url = self.parse_url(self.path)

        if url["requested_resource"] == "reviews":
            reviews = Reviews()
            new_review = reviews.create(request_body)
            return self.response(new_review, status.HTTP_201_SUCCESS_CREATED)
        elif url["requested_resource"] == "books":
            books = Books()
            new_book = books.create(request_body)
            return self.response(new_book, status.HTTP_201_SUCCESS_CREATED)
        elif url["requested_resource"] == "categories":
            categories = Categories()
            new_category = categories.create(request_body)
            return self.response(new_category, status.HTTP_201_SUCCESS_CREATED)
        else:
            return self.response("Resource not found", status.HTTP_404_CLIENT_ERROR_RESOURCE_NOT_FOUND)




#
# THE CODE BELOW THIS LINE IS NOT IMPORTANT FOR REACHING YOUR LEARNING OBJECTIVES
#
def main():
    host = ''
    port = 8000
    HTTPServer((host, port), JSONServer).serve_forever()

if __name__ == "__main__":
    main()