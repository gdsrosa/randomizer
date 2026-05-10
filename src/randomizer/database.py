from typing import Protocol

from .schemas import ItemRequest, UserInDB


class ItemRepository(Protocol):
    def get_all(self) -> list[ItemRequest]: ...

    def add(self, item: ItemRequest) -> None: ...

    def get_by_id(self, item_id: str) -> ItemRequest | None: ...

    def get_by_name(self, name: str) -> ItemRequest | None: ...

    def update(self, item_id: str, new_name: str) -> ItemRequest | None: ...

    def delete(self, item_id: str) -> ItemRequest | None: ...


class UserRepository(Protocol):
    def get_by_username(self, username: str) -> UserInDB | None: ...

    def add(self, user: UserInDB) -> None: ...


class InMemoryItemRepository:
    def __init__(self) -> None:
        self._items: list[ItemRequest] = []

    def get_all(self) -> list[ItemRequest]:
        return self._items.copy()

    def add(self, item: ItemRequest) -> None:
        self._items.append(item)

    def get_by_id(self, item_id: str) -> ItemRequest | None:
        return next((item for item in self._items if str(item.id) == item_id), None)

    def get_by_name(self, name: str) -> ItemRequest | None:
        return next((item for item in self._items if item.name == name), None)

    def update(self, item_id: str, new_name: str) -> ItemRequest | None:
        item = self.get_by_id(item_id)
        if item is None:
            return None
        index = self._items.index(item)
        updated_item = ItemRequest(id=item.id, name=new_name)
        self._items[index] = updated_item
        return updated_item

    def delete(self, item_id: str) -> ItemRequest | None:
        item = self.get_by_id(item_id)
        if item is None:
            return None
        self._items.remove(item)
        return item


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: list[UserInDB] = []

    def get_by_username(self, username: str) -> UserInDB | None:
        return next((user for user in self._users if user.username == username), None)

    def add(self, user: UserInDB) -> None:
        self._users.append(user)


items_db: InMemoryItemRepository = InMemoryItemRepository()
users_db: InMemoryUserRepository = InMemoryUserRepository()
