import os


class UrandomPseudoRandomStringGenerator(object):
    ERROR_MESSAGE = 'Unable to generate a cryptographically secure pseudo-random string from /dev/urandom. '

    def get_pseudo_random_string(self, length):
        """
        Generate a cryptographically secure pseudorandom number
        """
        return os.urandom(length).encode('hex')
