
class SimpleMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(request.method)

        response = self.get_response(request)

        print(response)

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        print(view_func, 'VIEW', request, view_args, view_kwargs)


import time


# class TimingMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         start_time = time.time()
#
#         response = self.get_response(request)
#
#         duration = time.time() - start_time
#         print(f"Request processed in {duration:.2f} seconds")
#
#         return response
#
#     def process_view(self, request, view_func, *args, **kwargs):
#         print(f"About to execute {view_func.__name__}")
#         return None
#
#     def process_exception(self, request, exception):
#         print(f"Error occurred: {exception}")
#         return None
#

class CompleteMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before the view (and later middleware) are called.
        print("Before view processing")

        response = self.get_response(request)

        # Code to be executed for each request/response after the view is called.
        print("After view processing")

        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        # Called just before Django calls the view.
        # Return either None (continue processing) or HttpResponse (stop here)
        print("Processing view")
        return None

    def process_exception(self, request, exception):
        # Called when a view raises an exception.
        # Return either None (continue processing) or HttpResponse (stop here)
        print(f"An exception occurred: {exception}")
        return None

    def process_template_response(self, request, response):
        # Called just after the view has finished executing, if the response has a render() method
        # Must return a response object that implements a render method
        print("Processing template response")
        return response
