from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


#!/usr/bin/env python

import logging
from typing import Union, List, Callable

import random
import os
import hashlib
import base64
import json
import hmac
from enum import Enum
import time
import sys
import argparse

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
fmt_interactive = logging.Formatter("%(asctime)s - %(levelname)s: %(message)s", "%H:%M:%S")
sh.setFormatter(fmt_interactive)
logger.addHandler(sh)


class Algo(Enum):
    SHA256 = "sha-256"  # These strings need to match the ones used by the altcha web client JS library.
    SHA512 = "sha-512"
    SHA384 = "sha-384"


std_encoding : str = "ascii" #"utf-8"
valid_algos : List[Algo] = [Algo.SHA256, Algo.SHA512, Algo.SHA384]

import secrets
import hashlib
import base64
import json




class Altcha:
    """
    Server backend for Altcha -- https://altcha.org/docs/website-integration/
    Note that Altcha has strong requirements, i.e., the client widget:
       * requires JavaScript enabled in the client browser AND
       * only works if the website is served via HTTPS.
    See the 'Ceveats' section on https://altcha.org/docs/website-integration/ for details.
    """

    def __init__(self, secret_key : str, min_int : int = 1, max_int : int = 10000, algorithm : Algo = Algo.SHA256):
        self.salt_len = 12
        self.min_int = min_int
        self.max_int = max_int  # must match the maxnumber passed to the altcha-widget in the HTML form source code, which defaults to 1,000,000
        self.secret_key = secret_key
        self.encoding = std_encoding
        self.algorithm = algorithm
        if not self.algorithm in valid_algos:
            raise ValueError(f"Invalid algorithm: '{self.algorithm}'. Currently the only supported algorithms are {valid_algos}.")

    @staticmethod
    def get_salt(salt_len : int = 12, use_expire : Union[int, None] = None) -> str:
        random_bytes = os.urandom(salt_len)
        salt : str = base64.b64encode(random_bytes).decode(std_encoding)
        if use_expire is not None:
            print("Using expiration")
            timestamp_now : int = int(time.time())
            timestamp_expires : int = timestamp_now + use_expire
            salt += "?expires=" + str(timestamp_expires)  # See Section 'Salt Parameters' on https://altcha.org/docs/server-integration/
        else:
            print("Not using expiration")
        return salt

    @staticmethod
    def get_algo_func(algo : str) -> Callable:
        if algo == Algo.SHA256:
            return hashlib.sha256
        elif algo == Algo.SHA512:
            return hashlib.sha512
        elif algo == Algo.SHA384:
            return hashlib.sha384
        else:
            raise ValueError(f"Invalid algo: '{algo}'. Use one of {[a.value for a in valid_algos]}.")


    def create_signature(self, data_to_sign: str, secret_key: str) -> str:
        #print(f"create_signature: using secret key '{secret_key}', encoding='{encoding}'.")
        algo = Altcha.get_algo_func(self.algorithm)
        secret_key = secret_key.encode(self.encoding) # convert to bytes
        data_to_sign = data_to_sign.encode(self.encoding) # convert to bytes
        #secret_key = base64.b64decode(secret_key) # this is still bytes # TODO: do we want this?

        hex_digest = hmac.new(secret_key, data_to_sign, digestmod=algo).hexdigest() # str
        return hex_digest

        #digest = hmac.new(secret_key, data_to_sign, digestmod=algo).digest() # still bytes
        #digest_b64 = base64.b64encode(digest) # bytes again
        #return digest_b64.decode(self.encoding) # that's now str


    def createChallenge(self, salt : Union[int, None] = None, secret_number : Union[int, None] = None, use_expire : Union[int, None] = None) -> List:
        if salt is None:
            salt : str = Altcha.get_salt(self.salt_len, use_expire=use_expire)
        if salt is not None and use_expire is not None:
            print("WARNING: Parameter 'use_expire' is ignored if a salt is passed. Set it to None to remove this warning.")

        if secret_number is None:
            secret_number = random.randint(self.min_int, self.max_int)
        secret_number_enc = base64.b64encode(bytes(bytes(salt, encoding=self.encoding) + bytes(secret_number)))

        algo = Altcha.get_algo_func(self.algorithm)

        challenge : str = algo(secret_number_enc).hexdigest()
        signature = self.create_signature(challenge, secret_key=self.secret_key)

        challenge_payload : dict = {
            "algorithm" : self.algorithm.value,
            "challenge" : challenge,
            "salt" : salt,
            "signature" : signature
        }

        # Some assertions to ensure we do not accidentally have bytes in here, because we will
        # need to encode the payload on the web in real life, when sending it to the client.
        assert isinstance(challenge_payload["algorithm"], str)
        assert isinstance(challenge_payload["challenge"], str)
        assert isinstance(challenge_payload["salt"], str)
        assert isinstance(challenge_payload["signature"], str)

        return challenge_payload

    def _get_salt_expiration_timestamp(salt : str) -> Union[int, None]:
        if "?expires=" in salt:
            try:
                expires_timestamp = int(salt.partition("?expires=")[-1])
                return expires_timestamp
            except Exception as ex:  # someone passed weird stuff over the internets. happens.
                logger.info(f"Invalid expires value in salt '{salt}'. Ignoring.")
                return False
        else:
            return False


    def isValidChallengeResponse(self, response_payload : Union[str, dict]) -> bool:
        """
        Determine whether challenge response (solution) is valid.
        @param reponse_payload: this is created from the altcha JS client library, and the (encoded) JSON object must contain the fields 'algorithm', 'challenge', 'salt', 'signature' and 'number', where number is the proof-of-work response (the result computed by the client).
        @return whether the solution is correct
        @Note If clients are simply sending a payload without server-side verification that they were assigned exactly the task solved in the payload,
        they can re-send the same response many times to circumvent the captcha, and thus only "pay" with compute *once* for many requests (replay attack). The solution
        is to invalidate a certain challenge for a while once a correct solution has been received. On a potentially multi-threaded webserver, this
        more or less requires storing these challenges in a database. This would need to be done in this function. The function would also
        need to search the database for the challenge, and only consider a new response valid if the challenge is not in the database yet.
        """
        check = self.createChallenge(response_payload['salt'], response_payload['number'])

        # if challenge_is_listed_as_used_before_in_database(response_payload):
        #     return False

        is_valid = check["algorithm"] == response_payload["algorithm"] and \
                   check["challenge"] == response_payload["challenge"] and \
                   check["signature"] == response_payload["signature"]


        # if is_valid:
        #     list_as_used_in_database(response_payload)

        return is_valid


def simulate_client_solving(challenge_payload : dict, response_computed : int) -> dict:
    """
    This simulates sending the challenge to the client over the web, the client solving it, and sending back a response.
    The real work done by the client is to compute 'response_computed', which needs to be passed for this simulation.
    @return the challenge response with the added 'number' field, containing the result. In this simuation, the result is simply set to the value of the parameter 'response_computed'.
    """
    response_payload = challenge_payload.copy()
    response_payload["number"] = response_computed
    return response_payload


altcha = Altcha(secret_key="bananeinderbirne")

@app.route('/')
def form():
    return render_template('form.html')

@app.route('/altcha_challenge', methods=['GET'])
def altcha_challenge():
    challenge = altcha.createChallenge()

    hardcoded_challenge =  { "algorithm" :	"SHA-256",
"challenge" :	"26f05a070bb77c99eb150a989d2a86a96aa7223fe5f253e8713dd87ebcfc4855",
"salt" :	"6b5cabdfb473dc7fa1468f21",
"signature" :	"f54640bd99a34f7acff52f19769c72124e22f93abe5a728e9e2a5306835b97c0" }


    #challenge = generator.create_challenge()
    return jsonify(hardcoded_challenge)


def test_altcha_creation():
    num_asserts_okay = 0
    altcha = Altcha(secret_key="bananeinderbirne")
    salt = "6b5cabdfb473dc7fa1468f21"
    secret_number = 17
    challenge = altcha.createChallenge(salt=salt, secret_number=secret_number)

    assert challenge["salt"] == salt, "Invalid salt."
    num_asserts_okay += 1

    assert challenge["algorithm"] == "sha-256", f"Invalid algo {challenge['algorithm']}, expected sha-256."
    num_asserts_okay += 1

    print(f"Tests okay, {num_asserts_okay} asserts passed.")


@app.route('/submit_form', methods=['POST'])
def submit_form():
    form_data = request.form.to_dict()
    altcha_response_raw = form_data.pop('altcha', None) # the name can be set in the widget, default is 'altcha'
    altcha_response = json.loads(base64.b64decode(altcha_response_raw))

    # Verify AltCHA response here
    if not altcha_response or not altcha.isValidChallengeResponse(altcha_response):
        return "Invalid AltCHA response", 400

    print("Received form data:", form_data)
    return "Form submitted successfully!"


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Altcha demo app with Python')
    parser.add_argument('--test', action='store_true', help='Run unit test.')
    args = parser.parse_args()
    if args.test:
        print(f"Running test...")
        test_altcha_creation()
    else:
        print(f"Running flask web app...")
        app.run(host='0.0.0.0', port=5000, ssl_context=('cert.pem', 'key.pem'))

