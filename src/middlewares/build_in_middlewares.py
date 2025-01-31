from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .middleware_settings import ALLOWED_HOSTS


def register_cors_middleware(app: FastAPI):
    headers = [
        "Authorization",           # Bearer token for authentication
        "Content-Type",            # Type of the data (e.g., application/json, multipart/form-data)
        "Accept",                  # Accepted response types (e.g., application/json)
        "Accept-Encoding",         # Supported content encodings (e.g., gzip, deflate)
        "Accept-Language",         # Preferred language(s) for the response
        "User-Agent",              # Information about the client's browser
        "X-Requested-With",        # Used in AJAX requests to identify them
        "Cookie",                  # Sent cookies (e.g., session_id, cart_id)
        "Referer",                 # URL from which the request originated
        "Origin",                  # Origin of the request (used in CORS)
        "Cache-Control",           # Controls caching behavior (e.g., no-cache)
        "X-Frame-Options",         # Protects against clickjacking by controlling iframe embedding
        "X-Content-Type-Options",  # Prevents browsers from interpreting files as a different MIME type
        "Strict-Transport-Security",  # Ensures the site is accessed via HTTPS
        "Set-Cookie",              # Sent by the server to set cookies (e.g., session cookies)
        "Location",                # Used for redirection (e.g., URL for checkout)
        "X-Custom-Header",         # Custom headers for special processing or tracking
        "Content-Length",          # Length of the response body in bytes
        "ETag",                    # Entity tag for caching or identifying the resource
        "X-Powered-By",            # Information about the server technology (e.g., FastAPI)
    ]

    methods = [
        "GET",      # Retrieve data from the server (e.g., fetching products or watch details)
        "POST",     # Send data to the server (e.g., submitting a form, creating a new order)
        "PUT",      # Update data on the server (e.g., updating user information, product details)
        "PATCH",    # Partially update data on the server (e.g., updating only specific fields)
        "DELETE",   # Delete data on the server (e.g., removing a product or order)
        "OPTIONS",  # Retrieve allowed methods for a resource (usually used in CORS preflight requests)
        "HEAD",     # Similar to GET but only retrieves the headers, not the body
        "TRACE",    # Used for debugging purposes to see the request-response chain
        "CONNECT",  # Used to establish a network connection to the server (e.g., tunneling HTTP through a proxy)
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
