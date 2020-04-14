from flask import Flask, request
import requests
import jwt
import json
import os
app = Flask(__name__)

# Your CF Access Authentication domain
AUTH_DOMAIN = os.getenv("AUTH_DOMAIN")
CERTS_URL = "{}/cdn-cgi/access/certs".format(AUTH_DOMAIN)

def _get_public_keys():
    """
    Returns:
        List of RSA public keys usable by PyJWT.
    """
    r = requests.get(CERTS_URL)
    public_keys = []
    jwk_set = r.json()
    for key_dict in jwk_set['keys']:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(key_dict))
        public_keys.append(public_key)
    return public_keys

@app.route('/token/validate')
def verify_token():
    if 'aud' in request.args:
        aud = request.args['aud']
    else:
        return "missing required application audience (AUD) tag", 400

    token = ''
    if 'CF_Authorization' in request.cookies:
        token = request.cookies['CF_Authorization']
    else:
        return "missing required cf authorization token", 403
    keys = _get_public_keys()

    # Loop through the keys since we can't pass the key set to the decoder
    valid_token = False
    for key in keys:
        try:
            # decode returns the claims that has the email when needed
            jwt.decode(token, key=key, audience=aud)
            valid_token = True
            break
        except:
            pass
    if not valid_token:
        return "invalid token", 403

    return "OK", 200


if __name__ == '__main__':
    app.run()
