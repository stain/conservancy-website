import hashlib

from django.conf import settings
from django.template import RequestContext

# This is backwards compatibilty support for a custom function we wrote
# ourselves that is no longer necessary in modern Django.
from django.shortcuts import render as render_template_with_context

class ParameterValidator(object):
    def __init__(self, given_hash_or_params, params_hash_key=None):
        if params_hash_key is None:
            self.given_hash = given_hash_or_params
        else:
            self.given_hash = given_hash_or_params.get(params_hash_key)
        seed = getattr(settings, 'CONSERVANCY_SECRET_KEY', '')
        self.hasher = hashlib.sha256(seed)
        if isinstance(self.given_hash, basestring):
            self.hash_type = type(self.given_hash)
        else:
            self.hash_type = type(self.hasher.hexdigest())
        self.valid = None
        if not (self.given_hash and seed):
            self.fail()

    def __enter__(self):
        self.valid = self.valid and None
        return self

    def __exit__(self, exc_type, exc_value, exc_tb):
        if exc_type is None:
            self.check()
        else:
            self.fail()

    def validate(self, data):
        self.valid = self.valid and None
        self.hasher.update(data)

    def check(self):
        if self.valid or (self.valid is None):
            self.valid = self.hash_type(self.hasher.hexdigest()) == self.given_hash
        return self.valid

    def fail(self):
        self.valid = False
