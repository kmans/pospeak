'''
tinyurl-like unique url generation for po/Speak

Includes upper and lowercase letters along with numbers.
It will try to generate a 5 character shortname, at around 1 billion, it will add a character

Fogleman's generator really is pretty fantastic.
It's fast and generates unique combinations which I can store in the DB

Based on algorithm developed by Michael Fogleman, MIT license
'''

DEFAULT_ALPHABET = 'md4eXzEnCt76WaRlJ0hkZI3V91qDQNwobPSguLxY5c2FOsB8rHjiGKMypUvTfA'
DEFAULT_BLOCK_SIZE = 30
MIN_LENGTH = 5

class _UrlEncoder(object):
    def __init__(self, alphabet=DEFAULT_ALPHABET, block_size=DEFAULT_BLOCK_SIZE):
        self.alphabet = alphabet
        self.block_size = block_size
        self.mask = (1 << block_size) - 1
        self.mapping = range(block_size)
        self.mapping.reverse()
    def encode_url(self, n, min_length=MIN_LENGTH):
        return self.enbase(self.encode(n), min_length)
    def decode_url(self, n):
        return self.decode(self.debase(n))
    def encode(self, n):
        return (n & ~self.mask) | self._encode(n & self.mask)
    def _encode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << i):
                result |= (1 << b)
        return result
    def decode(self, n):
        return (n & ~self.mask) | self._decode(n & self.mask)
    def _decode(self, n):
        result = 0
        for i, b in enumerate(self.mapping):
            if n & (1 << b):
                result |= (1 << i)
        return result
    def enbase(self, x, min_length=MIN_LENGTH):
        result = self._enbase(x)
        padding = self.alphabet[0] * (min_length - len(result))
        return '%s%s' % (padding, result)
    def _enbase(self, x):
        n = len(self.alphabet)
        if x < n:
            return self.alphabet[x]
        return self._enbase(x / n) + self.alphabet[x % n]
    def debase(self, x):
        n = len(self.alphabet)
        result = 0
        for i, c in enumerate(reversed(x)):
            result += self.alphabet.index(c) * (n ** i)
        return result

roomgen = _UrlEncoder()

def encode_url(n, min_length=MIN_LENGTH):
    return roomgen.encode_url(n, min_length)

def decode_url(n):
    return roomgen.decode_url(n)