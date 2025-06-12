import functools
import json

import jwt
import requests
from jwt.algorithms import RSAAlgorithm
from rest_framework.response import Response

AUTH0_DOMAIN = "your-tenant.auth0.com"
API_IDENTIFIER = "https://project-api.local"

def get_jwks():
    jwks_url = f"https://{AUTH0_DOMAIN}/.well-known/jwks.json"
    return requests.get(jwks_url).json()

def validate_jwt(token):
    jwks = get_jwks()
    unverified_header = jwt.get_unverified_header(token)
    key = None
    for jwk in jwks['keys']:
        if jwk['kid'] == unverified_header['kid']:
            key = RSAAlgorithm.from_jwk(json.dumps(jwk))
            break

    if not key:
        raise Exception("Key not found")

    payload = jwt.decode(
        token,
        key=key,
        algorithms=["RS256"],
        audience=API_IDENTIFIER,
        issuer=f"https://{AUTH0_DOMAIN}/"
    )
    return payload

def auth_required(view_func):
    @functools.wraps(view_func)
    def wrapper(self, request, *args, **kwargs):
        auth = request.META.get("HTTP_AUTHORIZATION", "")
        if not auth.startswith("Bearer "):
            return Response({"error": "Unauthorized"}, status=401)
        token = auth.split(" ")[1]
        try:
            payload = validate_jwt(token)
            request.user_payload = payload
        except Exception as e:
            return Response({"error": str(e)}, status=401)
        return view_func(self, request, *args, **kwargs)
    return wrapper
