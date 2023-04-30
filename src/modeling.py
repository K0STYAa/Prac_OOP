import random
import sys
import typing as tp

from src.guest import Guest
from src.hotel import Hotel
from src.utils import (
    logger,
    HOURS_PER_DAY,
)

def _generate_customers(modeling_days: int, new_application_hours: tp.Tuple[int, int]) -> tp.List[tp.Union[Guest, int]]:
    """
    Generate customers with given random parameters.
    """
    MIN_LIFE_EXPECTANCY = 1 # срок жизни в номере
    MAX_LIFE_EXPECTANCY = 7
    MIN_FURTHEST_BOOKING_DAY = 0 # не дальше какого дня бронь
    MAX_FURTHEST_BOOKING_DAY = 6
    current_hour = 0
    generated_customers = []
    while current_hour < modeling_days * HOURS_PER_DAY:
        if random.randint(0,1) == 1: # заселение в моменте
            day_in = current_hour // HOURS_PER_DAY
        else: # бронь с предоплатой
            day_in = random.randint(MIN_FURTHEST_BOOKING_DAY, MAX_FURTHEST_BOOKING_DAY)
        day_out = day_in + random.randint(MIN_LIFE_EXPECTANCY, MAX_LIFE_EXPECTANCY)
        
        generated_customers.append(
            (
                Guest(
                    day_in=day_in,
                    day_out=day_out,
                    room_preferences = random.randint(0, 3), 
                    discount=0), 
                current_hour
            )
        )
        current_hour += random.randint(*new_application_hours)
    return generated_customers

class HotelModel:
    
    def __init__(
        self,
        modeling_days: int,
        model_number_of_luxury_rooms: int,
        model_cost_of_luxury_rooms: int,
        model_number_of_junior_suites: int,
        model_cost_of_junior_suites: int,
        model_number_of_double_rooms: int,
        model_cost_of_double_rooms: int,
        model_number_of_single_rooms: int,
        model_cost_of_single_rooms: int,
        new_application_hours: tp.Tuple[int, int],
        discount_percent: int,
        tick_hours: int,
    ):
        self._hotel = Hotel(
            number_of_luxury_rooms=model_number_of_luxury_rooms,
            cost_of_luxury_rooms=model_cost_of_luxury_rooms,
            number_of_junior_suites=model_number_of_junior_suites,
            cost_of_junior_suites=model_cost_of_junior_suites,
            number_of_double_rooms=model_number_of_double_rooms,
            cost_of_double_rooms=model_cost_of_double_rooms,
            number_of_single_rooms=model_number_of_single_rooms,
            cost_of_single_rooms=model_cost_of_single_rooms,
            discount_percent=discount_percent
        )
        self._modeling_days = modeling_days
        self._tick_hours = tick_hours
        self._current_tick = 0
        self._guests_flow = _generate_customers(modeling_days, new_application_hours)
        logger.debug(f"Model with parameters: tick_time={self._tick_hours}")

    def tick(self):
        """
        Grab statistics about rooms,
        get new guests from generated.
        Then makes hotel tick.
        """
        new_customers = []
        while self._guests_flow and (self._current_tick+1) * self._tick_hours >= self._guests_flow[0][1]:
            new_guest = self._guests_flow.pop(0)
            new_customers.append(new_guest[0])

        logger.debug(f'TICK# {self._current_tick + 1}: generated_customers = {new_customers}')
        self._hotel.recieve_guests(new_customers)
        self._hotel.tick(self._tick_hours)
        self._current_tick += 1
    

    @property
    def current_luxury_occupancy_str(self) -> tp.List[str]:
        return self._hotel.current_luxury_occupancy_str
    
    @property
    def current_junior_occupancy_str(self) -> tp.List[str]:
        return self._hotel.current_junior_occupancy_str
    
    @property
    def current_double_occupancy_str(self) -> tp.List[str]:
        return self._hotel.current_double_occupancy_str
    
    @property
    def current_single_occupancy_str(self) -> tp.List[str]:
        return self._hotel.current_single_occupancy_str
    

    @property
    def current_luxury_occupancy_today(self) -> tp.List[str]:
        return self._hotel.current_luxury_occupancy_today
    
    @property
    def current_junior_occupancy_today(self) -> tp.List[str]:
        return self._hotel.current_junior_occupancy_today
    
    @property
    def current_double_occupancy_today(self) -> tp.List[str]:
        return self._hotel.current_double_occupancy_today
    
    @property
    def current_single_occupancy_today(self) -> tp.List[str]:
        return self._hotel.current_single_occupancy_today
    
    
    @property
    def per_week_luxury_occupation_percent(self):
        return self._hotel.per_week_luxury_occupation_percent
    
    @property
    def per_week_junior_occupation_percent(self):
        return self._hotel.per_week_junior_occupation_percent
    
    @property
    def per_week_double_occupation_percent(self):
        return self._hotel.per_week_double_occupation_percent
    
    @property
    def per_week_single_occupation_percent(self):
        return self._hotel.per_week_single_occupation_percent
    
    @property
    def per_week_hotel_occupation_percent(self):
        return self._hotel.per_week_hotel_occupation_percent
    
    
    @property
    def total_luxury_occupation_percent(self):
        return self._hotel.total_luxury_occupation_percent(self._modeling_days)
    
    @property
    def total_junior_occupation_percent(self):
        return self._hotel.total_junior_occupation_percent(self._modeling_days)
    
    @property
    def total_double_occupation_percent(self):
        return self._hotel.total_double_occupation_percent(self._modeling_days)
    
    @property
    def total_single_occupation_percent(self):
        return self._hotel.total_single_occupation_percent(self._modeling_days)
    
    @property
    def total_hotel_occupation_percent(self):
        return self._hotel.total_hotel_occupation_percent(self._modeling_days)
    
    
    @property
    def current_luxury_total_earnings(self):
        return self._hotel.current_luxury_total_earnings
    
    @property
    def current_junior_total_earnings(self):
        return self._hotel.current_junior_total_earnings
    
    @property
    def current_double_total_earnings(self):
        return self._hotel.current_double_total_earnings
    
    @property
    def current_single_total_earnings(self):
        return self._hotel.current_single_total_earnings
    
    @property
    def current_hotel_total_earnings(self):
        return self._hotel.current_hotel_total_earnings
    
    
    @property
    def luxury_served_guests(self):
        return self._hotel.luxury_served_guests
    
    @property
    def junior_served_guests(self):
        return self._hotel.junior_served_guests
    
    @property
    def double_served_guests(self):
        return self._hotel.double_served_guests
    
    @property
    def single_served_guests(self):
        return self._hotel.single_served_guests
    
    @property
    def hotel_served_guests(self):
        return self._hotel.hotel_served_guests
    
    
    @property
    def total_lost_clients(self):
        return self._hotel.total_lost_clients
    

    @property
    def percent_of_surved_clients(self):
        return self._hotel.percent_of_surved_clients