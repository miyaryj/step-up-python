import json
import random
import sys
from datetime import date
from abc import ABC, abstractmethod

from pydantic import BaseModel

FORTUNE_OUTPUT_TEMPLATE = """
{today} の {name} さんの運勢

ラッキーカラー: {lucky_color}
ラッキーナンバー: {lucky_number}
"""


class UserProfile(BaseModel):
    name: str
    birthday: date


class FortuneTeller(ABC):
    def tell(self, user_profile: UserProfile, today: date) -> str:
        lucky_color = self._lucky_color(user_profile, today)
        lucky_number = self._lucky_number(user_profile, today)

        return FORTUNE_OUTPUT_TEMPLATE.format(
            today=today,
            name=user_profile.name,
            lucky_color=lucky_color,
            lucky_number=lucky_number,
        )

    @abstractmethod
    def _lucky_color(self, user_profile: UserProfile, today: date) -> str:
        pass

    @abstractmethod
    def _lucky_number(self, user_profile: UserProfile, today: date) -> int:
        pass


class RandomFortuneTeller(FortuneTeller):
    def __init__(self, lucky_colors: list[str], lucky_numbers: list[int]):
        self.lucky_colors = lucky_colors
        self.lucky_numbers = lucky_numbers

    def _lucky_color(self, user_profile: UserProfile, today: date) -> str:
        return random.choice(self.lucky_colors)

    def _lucky_number(self, user_profile: UserProfile, today: date) -> int:
        return random.choice(self.lucky_numbers)


class BirthdayBasedFortuneTeller(FortuneTeller):
    def _lucky_color(self, user_profile: UserProfile, today: date) -> str:
        if user_profile.birthday.month == today.month:
            return "red"
        else:
            return "blue"

    def _lucky_number(self, user_profile: UserProfile, today: date) -> int:

        if user_profile.birthday == today:
            return 777
        else:
            return 0


def get_fortune_teller(fortune_teller_type: str) -> FortuneTeller:
    if fortune_teller_type == "random":
        lucky_colors = ["red", "green", "blue"]
        lucky_numbers = [1, 2, 3]
        return RandomFortuneTeller(lucky_colors, lucky_numbers)
    elif fortune_teller_type == "birthday":
        return BirthdayBasedFortuneTeller()
    else:
        raise ValueError(f"Unknown fortune_teller_type: {fortune_teller_type}")


def main():
    if len(sys.argv) >= 2:
        fortune_teller_type = sys.argv[1]
    else:
        fortune_teller_type = "random"

    with open("profile.json") as f:
        profile_data = json.load(f)

    user_profile = UserProfile.model_validate(profile_data)

    today = date.today()

    fortune_teller = get_fortune_teller(fortune_teller_type)

    result = fortune_teller.tell(user_profile, today)
    print(result)


if __name__ == "__main__":
    main()
