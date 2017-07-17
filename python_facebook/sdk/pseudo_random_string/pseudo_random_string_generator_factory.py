from python_facebook.sdk.pseudo_random_string.urandom_pseudo_random_string_generator import \
    UrandomPseudoRandomStringGenerator


class PseudoRandomStringGeneratorFactory(object):

    @classmethod
    def create_pseudo_random_string_generator(cls, generator_name):
        """
        Pseudo random string generator creation.
        """
        return UrandomPseudoRandomStringGenerator()
