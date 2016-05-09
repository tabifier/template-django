import string
import random


def random_key_generator(length=50, chars="{}{}".format(string.ascii_letters, string.digits)):
    return "".join(random.SystemRandom().choice(chars) for _ in xrange(length))
