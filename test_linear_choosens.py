
from linear_choosens import choice_linear


def test_taking_all():
    for n in range(1, 20):
        print('N =', n)
        assert set(range(n)) == choice_linear(n, range(n))

def test_taking_some():
    for _ in range(10):  # do that many times
        for n in range(1, 20):
            print('N =', n)
            found = choice_linear(n, range(20))
            assert len(found) == n
            assert found <= set(range(20))

def test_gen_behavior():
    for _ in range(10):  # do that many times
        for n in range(1, 20):
            print('N =', n)
            stream = iter(range(20))
            found = choice_linear(n, stream, it_size=n)
            print(found)
            assert set(range(n)) == found
            assert set(stream) == set(range(n, 20))
