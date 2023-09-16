import json
import os
from functools import wraps
from urllib.request import urlopen

from dotenv import load_dotenv
from flask import _request_ctx_stack, abort, request
from jose import jwt

load_dotenv()

AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
ALGORITHMS = os.environ.get('ALGORITHMS')
API_AUDIENCE = os.environ.get('API_AUDIENCE')


# AuthError Exception

class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


# Auth Header
def get_token_auth_header():
    auth = request.headers.get('Authorization', None)
    # if there is no header
    if not auth:
        print('Authorization header is expected')
        raise AuthError('Authorization header is expected.', 401)

    # to check for the bearer and the token seperatly
    parts = auth.split()
    if parts[0].lower() != 'bearer':
        print('Authorization header must start with "Bearer"')
        raise AuthError('Authorization header must start with "Bearer".', 401)

    # if the lenght of the splited header is not 2 and
    # it passed the previous check then it doesn't have a token
    elif len(parts) == 1:
        print('Token not found')
        raise AuthError('Token not found.', 401)

    # checks for the format of the header
    elif len(parts) > 2:
        print('Authorization header must be Bearer<Token>.')
        raise AuthError('Authorization header must be Bearer<Token>.', 401)
    # except:
    #     abort(401)

    token = parts[1]
    # print("Token:", token)
    # print("auth", auth)
    # print("parts", parts)

    return token


def check_permissions(permission, payload):
    if 'permissions' not in payload:
        print('Permissions not included in JWT')
        raise AuthError('Permissions not included in JWT.', 400)

    if permission not in payload['permissions']:
        print('Permission not found')
        raise AuthError('Permission not found.', 403)

    return True


def verify_decode_jwt(token):
    # this is to compare with the provided token to make sure it is valid
    jsonurl = urlopen(f'https://{AUTH0_DOMAIN}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)

    # if there is no key id then it is an invalid header
    if 'kid' not in unverified_header:
        print(' Authorization malformed')
        raise AuthError('Authorization malformed.', 401)

    # does the compare to check that the key id matches the one provided
    # then it adds the values of the key(key type, key id, usage)
    rsa_key = {}
    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # if rsa_key was not found it raises AuthError
    if rsa_key:
        try:
            # print('token', token)
            # print('rsa_key', rsa_key)
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer='https://' + AUTH0_DOMAIN + '/'
            )

            return payload

        except jwt.ExpiredSignatureError:
            print(' Token expired')
            raise AuthError('Token expired.', 401)

        except jwt.JWTClaimsError:
            print('Incorrect claims. Please, check the audience and issuer')
            raise AuthError(
                'Incorrect claims. Please, check the audience and issuer.', 401)

        except Exception:
            print('Unable to parse authentication token')
            raise AuthError('Unable to parse authentication token.', 400)

    print('Unable to find the appropriate key')
    raise AuthError('Unable to find the appropriate key.', 403)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)

            return f(payload, *args, **kwargs)
        return wrapper
    return requires_auth_decorator
