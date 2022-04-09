import math
from functools import cached_property, lru_cache

from .utils import load_items, load_skills, load_actions
from typing import Optional


class Database(object):
    @cached_property
    def _items(self):
        return load_items()

    @cached_property
    def _skills(self):
        return load_skills()

    @cached_property
    def _actions(self):
        return load_actions()

    @lru_cache
    def get_action_name_by_id(self, action_id: int) -> Optional[str]:
        if action_id == 0:
            return "動作停止"
        action_id = int(math.log2(action_id)) + 2
        row = self._actions[self._actions["ID"] == action_id]
        if not row.empty:
            return row.iloc[0]["_Name"]

    @lru_cache
    def get_skill_name_by_id(self, skill_id: int) -> Optional[str]:
        row = self._skills[self._skills["ID"] == skill_id]
        if not row.empty:
            return row.iloc[0]["_Name"]

    @lru_cache
    def get_item_name_by_id(self, item_id: int) -> Optional[str]:
        row = self._items[self._items["ID"] == item_id]
        if not row.empty:
            return row.iloc[0]["_Name"]


DATABASE = Database()
