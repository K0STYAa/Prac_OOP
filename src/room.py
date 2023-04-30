import typing as tp

from src.guest import Guest
from src.utils import logger


class Room:
    def __init__(
        self,
        price: int,
    ):
        self._price = price
        self._occupation: tp.Dict[int, bool] = {new_day: False for new_day in range(45)}
        self._guest_days_out: tp.Set[int] = set()
        
        self._total_served_guests: int = 0
        self._total_earnings: int = 0
        self._total_ticks: int = 0

    def current_occupation_in_week(self, day) -> tp.Dict[int, bool]:
        return {key: value for key, value in self._occupation.items() if day <= key <= day+7}
    
    def occupation_in_model(self, day) -> tp.Dict[int, bool]:
        return {key: value for key, value in self._occupation.items() if 0 <= key <= day}
    
    def is_occupied(self, day):
        return self._occupation[day]

    @property
    def total_served_guests(self) -> int:
        return self._total_served_guests
    
    @property
    def total_earnings(self):
        return round(self._total_earnings, 1)
    
    def receive_guest(self, new_guest: Guest) -> bool:
        """Check if the room is available"""
        is_room_busy = False
        for day in range(new_guest.day_in, new_guest.day_out+1):
            is_room_busy = is_room_busy or self._occupation[day]
        if is_room_busy:
            return False
        
        for day in range(new_guest.day_in, new_guest.day_out+1):
            self._occupation[day] = True
        self._guest_days_out.add(new_guest.day_out)
        self._total_earnings += self._price * (1 - float(new_guest.discount)/100)
        return True
    
    def tick(self, day: int):
        """
        Serve guests and write stats
        """
        count_surved_guests = 0
        for day_out in self._guest_days_out:
            if day_out <= day:
                count_surved_guests += 1
        self._total_served_guests = count_surved_guests
        self._total_ticks += 1

        logger.debug(f'Load at end of tick: {self._occupation}')