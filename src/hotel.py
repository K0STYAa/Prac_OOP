import typing as tp

from src.guest import Guest
from src.room import Room
from src.utils import logger, HOURS_PER_DAY

def occupation_str(occupation_dict):
    # Convert the dictionary keys to a sorted list of integers
    days = sorted(list(occupation_dict.keys()))

    # Initialize a list to store the occupied ranges
    ranges = []

    # Initialize variables to track the start and end of the current range
    range_start = None
    range_end = None

    # Iterate through the sorted list of days
    for day in days:
        # If the occupation value for the current day is True
        if occupation_dict[day]:
            # If we're not currently in a range, start a new one
            if range_start is None:
                range_start = day
            # Update the end of the current range
            range_end = day
        # If the occupation value for the current day is False
        else:
            # If we're in a range, add it to the list and reset the start and end
            if range_start is not None:
                ranges.append((range_start, range_end))
                range_start = None
                range_end = None

    # If we're still in a range at the end of the loop, add it to the list
    if range_start is not None:
        ranges.append((range_start, range_end))

    # Convert the list of ranges to the desired string format
    sequence = ""
    for r in ranges:
        if r[0] == r[1]:
            sequence += str(r[0])
        else:
            sequence += f"{r[0]}-{r[1]}"
        sequence += ", "

    # Remove the trailing ", " from the sequence
    sequence = sequence[:-2]

    return sequence

class Hotel:
    def __init__(
        self,
        number_of_luxury_rooms: int,
        cost_of_luxury_rooms: int,
        number_of_junior_suites: int,
        cost_of_junior_suites: int,
        number_of_double_rooms: int,
        cost_of_double_rooms: int,
        number_of_single_rooms: int,
        cost_of_single_rooms: int,
        discount_percent: int,
    ):
        
        self._luxury_rooms: tp.List[Room] = [
            Room(price=cost_of_luxury_rooms)
            for _ in range(number_of_luxury_rooms)
        ]
        self._junior_suites: tp.List[Room] = [
            Room(price=cost_of_junior_suites)
            for _ in range(number_of_junior_suites)
        ]
        self._double_rooms: tp.List[Room] = [
            Room(price=cost_of_double_rooms)
            for _ in range(number_of_double_rooms)
        ]
        self._single_rooms: tp.List[Room] = [
            Room(price=cost_of_single_rooms)
            for _ in range(number_of_single_rooms)
        ]

        self._discount_percent = discount_percent
        self._total_lost_clients = 0
        self._current_day_hours = 0 # hours from start. day = _current_day_hours / HOURS_PER_DAY

        logger.debug(f'Created Hotel with '
                     f'{number_of_luxury_rooms} luxury rooms(cost={cost_of_luxury_rooms}), '
                     f'{number_of_junior_suites} junior suites(cost={cost_of_junior_suites}), '
                     f'{number_of_double_rooms} double rooms(cost={cost_of_double_rooms}), '
                     f'{number_of_single_rooms} single rooms(cost={cost_of_single_rooms}), '
                     f'dicount percent = {discount_percent}')
        
    def recieve_guests(self, guests: tp.List[Guest]):
        """Book for guest some room or add to lost clients"""
        for guest in guests:
            guest_room_id = -1
            if guest.room_preferences == 0:
                for room_id in range(len(self._single_rooms)):
                    if self._single_rooms[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the single room {guest_room_id}')
                        break
            elif guest.room_preferences == 1:
                for room_id in range(len(self._double_rooms)):
                    if self._double_rooms[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the double room {guest_room_id}')
                        break
            if guest.room_preferences == 2:
                for room_id in range(len(self._junior_suites)):
                    if self._junior_suites[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the junior suites {guest_room_id}')
                        break
            elif guest.room_preferences == 3:
                for room_id in range(len(self._luxury_rooms)):
                    if self._luxury_rooms[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the luxury room {guest_room_id}')
                        break
            
            if guest_room_id == -1 and (guest.room_preferences == 0 or guest.room_preferences == 1):
                guest.add_discount(self._discount_percent)

                for room_id in range(len(self._double_rooms)):
                    if self._double_rooms[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the double room {guest_room_id} with discount {self._discount_percent}')
                        break
                for room_id in range(len(self._junior_suites)):
                    if self._junior_suites[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into junior suites {guest_room_id} with discount {self._discount_percent}')
                        break
                for room_id in range(len(self._luxury_rooms)):
                    if self._luxury_rooms[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the luxury room {guest_room_id} with discount {self._discount_percent}')
                        break
            elif guest_room_id == -1 and guest.room_preferences == 2:
                guest.add_discount(self._discount_percent)
                for room_id in range(len(self._luxury_rooms)):
                    if self._luxury_rooms[room_id].receive_guest(guest):
                        guest_room_id = room_id
                        logger.debug(f'the client {guest} checked into the luxury room {guest_room_id} with discount {self._discount_percent}')
                        break

            if guest_room_id == -1:
                    self._total_lost_clients += 1
                    logger.debug(f'lost a client with room preferences {guest.room_preferences}')
        
    def tick(self, tick_hours: int):
        logger.debug('Hotel tick')
        self._current_day_hours = self._current_day_hours + tick_hours
        for room_number in range(len(self._single_rooms)):
            logger.debug(f"Tick in single room #{room_number}")
            self._single_rooms[room_number].tick(self._current_day_hours // HOURS_PER_DAY)
        for room_number in range(len(self._double_rooms)):
            logger.debug(f"Tick in double room #{room_number}")
            self._double_rooms[room_number].tick(self._current_day_hours // HOURS_PER_DAY)
        for room_number in range(len(self._junior_suites)):
            logger.debug(f"Tick in junior room #{room_number}")
            self._junior_suites[room_number].tick(self._current_day_hours // HOURS_PER_DAY)
        for room_number in range(len(self._luxury_rooms)):
            logger.debug(f"Tick in luxury room #{room_number}")
            self._luxury_rooms[room_number].tick(self._current_day_hours // HOURS_PER_DAY)
            
    
    @property
    def current_luxury_occupancy_str(self) -> tp.List[str]:
        return [occupation_str(room.current_occupation_in_week(self._current_day_hours // HOURS_PER_DAY)) for room in self._luxury_rooms]
    
    @property
    def current_junior_occupancy_str(self) -> tp.List[str]:
        return [occupation_str(room.current_occupation_in_week(self._current_day_hours // HOURS_PER_DAY)) for room in self._luxury_rooms]
    
    @property
    def current_double_occupancy_str(self) -> tp.List[str]:
        return [occupation_str(room.current_occupation_in_week(self._current_day_hours // HOURS_PER_DAY)) for room in self._luxury_rooms]
    
    @property
    def current_single_occupancy_str(self) -> tp.List[str]:
        return [occupation_str(room.current_occupation_in_week(self._current_day_hours // HOURS_PER_DAY)) for room in self._luxury_rooms]
    

    @property
    def current_luxury_occupancy_today(self) -> tp.List[bool]:
        return [room.is_occupied(self._current_day_hours // HOURS_PER_DAY) for room in self._luxury_rooms]
    
    @property
    def current_junior_occupancy_today(self) -> tp.List[bool]:
        return [room.is_occupied(self._current_day_hours // HOURS_PER_DAY) for room in self._junior_suites]
    
    @property
    def current_double_occupancy_today(self) -> tp.List[bool]:
        return [room.is_occupied(self._current_day_hours // HOURS_PER_DAY) for room in self._double_rooms]
    
    @property
    def current_single_occupancy_today(self) -> tp.List[bool]:
        return [room.is_occupied(self._current_day_hours // HOURS_PER_DAY) for room in self._single_rooms]
    
    
    @property
    def per_week_luxury_occupation_percent(self) -> int:
        avg_occupation = 0
        for room in self._luxury_rooms:
            day=self._current_day_hours // HOURS_PER_DAY
            occupation = room.current_occupation_in_week(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._luxury_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    @property
    def per_week_junior_occupation_percent(self) -> int:
        avg_occupation = 0
        for room in self._junior_suites:
            day=self._current_day_hours // HOURS_PER_DAY
            occupation = room.current_occupation_in_week(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._junior_suites)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    @property
    def per_week_double_occupation_percent(self) -> int:
        avg_occupation = 0
        for room in self._double_rooms:
            day=self._current_day_hours // HOURS_PER_DAY
            occupation = room.current_occupation_in_week(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._double_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    @property
    def per_week_single_occupation_percent(self) -> int:
        avg_occupation = 0
        for room in self._single_rooms:
            day=self._current_day_hours // HOURS_PER_DAY
            occupation = room.current_occupation_in_week(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._single_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    @property
    def per_week_hotel_occupation_percent(self) -> int:
        avg_occupation = 0
        all_rooms = self._single_rooms + self._double_rooms + self._junior_suites + self._luxury_rooms
        for room in all_rooms:
            day=self._current_day_hours // HOURS_PER_DAY
            occupation = room.current_occupation_in_week(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(all_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    
    def total_luxury_occupation_percent(self, day) -> int:
        avg_occupation = 0
        for room in self._luxury_rooms:
            occupation = room.occupation_in_model(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._luxury_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    def total_junior_occupation_percent(self, day) -> int:
        avg_occupation = 0
        for room in self._junior_suites:
            occupation = room.occupation_in_model(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._junior_suites)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    def total_double_occupation_percent(self, day) -> int:
        avg_occupation = 0
        for room in self._double_rooms:
            occupation = room.occupation_in_model(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._double_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    def total_single_occupation_percent(self, day) -> int:
        avg_occupation = 0
        for room in self._single_rooms:
            occupation = room.occupation_in_model(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(self._single_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation
    
    def total_hotel_occupation_percent(self, day) -> int:
        avg_occupation = 0
        all_rooms = self._single_rooms + self._double_rooms + self._junior_suites + self._luxury_rooms
        for room in all_rooms:
            occupation = room.occupation_in_model(day)
            occup_days = sum(occupation.values())
            avg_occupation += float(occup_days) / 8
        avg_occupation /= len(all_rooms)
        avg_occupation = int(avg_occupation*100)
        return avg_occupation


    @property
    def current_luxury_total_earnings(self):
        return sum((room.total_earnings for room in self._luxury_rooms))

    @property
    def current_junior_total_earnings(self):
        return sum((room.total_earnings for room in self._junior_suites))
    
    @property
    def current_double_total_earnings(self):
        return sum((room.total_earnings for room in self._double_rooms))
    
    @property
    def current_single_total_earnings(self):
        return sum((room.total_earnings for room in self._single_rooms))
    
    @property
    def current_hotel_total_earnings(self):
        all_rooms = self._luxury_rooms + self._junior_suites + self._double_rooms + self._single_rooms
        return sum((room.total_earnings for room in all_rooms))
    

    @property
    def luxury_served_guests(self):
        return int(sum((room.total_served_guests for room in self._luxury_rooms)))
    
    @property
    def junior_served_guests(self):
        return int(sum((room.total_served_guests for room in self._junior_suites)))
    
    @property
    def double_served_guests(self):
        return int(sum((room.total_served_guests for room in self._double_rooms)))
    
    @property
    def single_served_guests(self):
        return int(sum((room.total_earnings for room in self._single_rooms)))
    
    @property
    def hotel_served_guests(self):
        all_rooms = self._luxury_rooms + self._junior_suites + self._double_rooms + self._single_rooms
        return int(sum((room.total_served_guests for room in all_rooms)))


    @property
    def total_lost_clients(self):
        return self._total_lost_clients
    

    @property
    def percent_of_surved_clients(self):
        all_rooms = self._luxury_rooms + self._junior_suites + self._double_rooms + self._single_rooms
        surved_clients = float(sum((room.total_served_guests for room in all_rooms)))
        lost_clients = self._total_lost_clients 
        all_clients = surved_clients + lost_clients
        if all_clients == 0:
            return 0
        return int(surved_clients/all_clients*100)
