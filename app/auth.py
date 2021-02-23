import os
from flask import request, abort
from functools import wraps
import json
from urllib.request import urlopen
from jose import jwt

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
ALGORITHMS = [os.getenv('AUTH0_ALGORITHMS')]
API_AUDIENCE = os.getenv('AUTH0_API_AUDIENCE')


class AuthError(Exception):
    ''' Raised whenever the @requires_auth decorator fails '''

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def get_token_auth_header():
    ''' From the request: get the authorization header, remove the "Bearer"
    prefix and return the security token.'''

    auth_header = request.headers.get('Authorization', None)

    # manage a missing authorization header
    if not auth_header:
        raise AuthError({
            'code': 'missing_auth_header',
            'description': 'Missing Authorization header.'
        }, 401)

    parts = auth_header.split()

    # manage a malformed authorization header
    if parts[0].lower() != 'bearer':
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Authorization header must start with "Bearer".'
        }, 401)
    if len(parts) != 2:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Invalid Authorization header. Must contain a token.'
        }, 401)

    token = parts[1]  # return the token stripped of the 'Bearer' prefix
    return token


def verify_decode_jwt(token):
    ''' Get the token and the public key, return the decoded payload '''

    unverified_header = jwt.get_unverified_header(token)
    # open the url and store a byte string
    json_url = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(json_url.read())  # convert to a json
    rsa_key = dict()

    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_auth_header',
            'description': 'Invalid Authorization header. Must contain a KID'
        }, 401)

    # get the public key
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e'],
            }
            break
    if rsa_key:  # verify the signature
        try:

            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer=f'https://{AUTH0_DOMAIN}/'
            )
            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired.'
                }, 401)
        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description': 'Incorrect claims. Check audience and issuer.'
                }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token.'
                }, 400)
    else:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Unable to find the appropriate key.'
            }, 400)


def check_permissions(permission, payload):
    ''' Check if the request comes with the suitable Role permissions '''
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_token',
            'description': 'Unable to find permissions.'
            }, 400)
    if permission not in payload['permissions']:
        raise AuthError({
            'code': 'forbidden',
            'description': 'User does not have required permissions.'
            }, 401)
    return True


def requires_auth(permission=''):
    ''' This is used as a DECORATOR for the endpoints.
    Get the token, decode the JWT, validate claims, check the requested
    permission.
    Return the decorator which passes the decoded payload to the decorated
    function. '''
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            try:
                payload = verify_decode_jwt(token)
            except AuthError as e:
                abort(401, e.error)
            check_permissions(permission, payload)
            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
