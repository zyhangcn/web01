from functools import partial

from pandas.tests.io.test_parquet import pa


def aad(a, b, c, m=0):
    return a + b + c + m


print(aad(1, 9, 1))

add_pa0000r = partial(aad, 100, m=1000000)
add_100=partial(aad,m=102020202002020)
print(add_100(1, 2, 3))
print(add_pa0000r(89, 213))
