from dataclasses import dataclass


@dataclass
class Guest:
    day_in: int
    day_out: int
    room_preferences: int
    discount: int

    def add_discount(self, new_discount):
        self.discount = new_discount

    def room_preferences_int(self):
        return self.room_preferences