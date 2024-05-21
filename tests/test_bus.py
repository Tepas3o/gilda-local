from gilda_opts.bus import Bus


def test_bus_1():
    b1 = Bus(name='home', uid=1)

    assert b1.name == 'home'
    assert b1.uid == 1

    b2 = Bus(uid=2, name='home2')

    assert b2.name == 'home2'
    assert b2.uid == 2


def test_bus_2():
    data = '{"name": "home", "uid": 1}'

    b1 = Bus.from_json(data)

    assert b1.name == 'home'
    assert b1.uid == 1

    d1 = b1.to_json()

    b2 = Bus.from_json(d1)

    assert b2 == b1


def test_bus_3():
    data = '[{"name": "home", "uid": 1}, {"name": "casa", "uid": 2}]'

    buses = Bus.schema().loads(data, many=True)

    b1 = buses[0]

    assert b1.name == 'home'
    assert b1.uid == 1

    b1 = buses[1]

    assert b1.name == 'casa'
    assert b1.uid == 2
