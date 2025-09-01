from repositories.base import BaseRepository


class IntRepo(BaseRepository[int]):
    pass


def test_add_and_get_all_order_and_trimming():
    repo = IntRepo(maxlen=3)
    repo.add(1)
    repo.add(2)
    repo.add(3)
    # Newest first
    assert repo.get_all() == [3, 2, 1]

    # Exceed maxlen trims oldest
    repo.add(4)
    assert repo.get_all() == [4, 3, 2]


def test_get_all_returns_copy():
    repo = IntRepo(maxlen=3)
    repo.add(1)
    items = repo.get_all()
    items.append(999)
    # Underlying storage should not be affected
    assert repo.get_all() == [1]
