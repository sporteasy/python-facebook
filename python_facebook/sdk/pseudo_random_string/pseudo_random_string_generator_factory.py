from python_facebook.sdk.pseudo_random_string.\
    urandom_pseudo_random_string_generator import \
    UrandomPseudoRandomStringGenerator


class PseudoRandomStringGeneratorFactory(object):
    @classmethod
    def create_pseudo_random_string_generator(cls, generator):
        """
        Pseudo random string generator creation.
        """
        if generator:
            return generator

        return UrandomPseudoRandomStringGenerator()
