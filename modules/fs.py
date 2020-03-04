import foursquare
import random

TEMPLATE_INPUT = {
    "budget_per_person": 80,
    "minimum_rating": 4.4,
    "number_of_stops": 2,
    "current_location": {"lat": 40.6865628, "lng": -73.977101},
    "max_uber_time": 20,
    "final_destination": {"lat": 40.6863959, "lng": -73.9719153},
    "radius": 250,
}


"""
    Categories to choose from: https://developer.foursquare.com/docs/resources/categories
"""

AVAILABLE_CATEGORIES = {
    "4bf58dd8d48988d11e941735": {"repeat": True, "name": "cocktail_bar"},
    "4bf58dd8d48988d155941735": {"repeat": False, "name": "gastropub"},
    # "4bf58dd8d48988d16a941735": {"repeat": False, "name": "bakery"},
}


class FridayNight(object):
    def __init__(self, preference_profile={}):
        self.budget_per_person = preference_profile.get(
            "budget_per_person", TEMPLATE_INPUT["budget_per_person"]
        )
        self.radius = preference_profile.get("radius", TEMPLATE_INPUT["radius"])
        self.minimum_rating = preference_profile.get(
            "minimum_rating", TEMPLATE_INPUT["minimum_rating"]
        )
        self.number_of_stops = preference_profile.get(
            "number_of_stops", TEMPLATE_INPUT["number_of_stops"]
        )
        self.current_location = preference_profile.get(
            "current_location", TEMPLATE_INPUT["current_location"]
        )
        self.max_uber_time = preference_profile.get(
            "max_uber_time", TEMPLATE_INPUT["max_uber_time"]
        )
        self.final_destination_coords = preference_profile.get(
            "final_destination", TEMPLATE_INPUT["final_destination"]
        )

        self._init_foursquare_client()
        self._current_venue_location = self.current_location
        self.visited_categories = []

    def _init_foursquare_client(self):
        self.fsc = foursquare.Foursquare(
            client_id="K14FVC2J10UYPEHTE2JL1PHXNRX3CCPXSB0KUMCYOSNQUY5Y",
            client_secret="STMMKGZ3JNJEOTTUPQBQBUYBQF0V1M1RUZFTKN4EIUP2UNUT",
        )

    def _choose_random_venue_by_category(self, category_id):
        if not self.fsc:
            return

        current_location = f"{self._current_venue_location['lat']},{self._current_venue_location['lng']}"

        nearby = self.fsc.venues.explore(
            params={
                "ll": current_location,
                "categoryId": category_id,
                "openNow": True,
                "radius": self.radius,
            }
        )

        nearby_venues = {
            venue["venue"]["name"]: venue["venue"]["location"]
            for venue in nearby["groups"][0]["items"]
        }

        venue_name = random.choice(list(nearby_venues.keys()))
        while venue_name in self.current_stops.keys():
            venue_name = random.choice(list(nearby_venues.keys()))

        return venue_name, nearby_venues[venue_name]

    def find_venue_by_category(self, category_id):
        return self._choose_random_venue_by_category(category_id)

    def create_thread(self):
        self.current_stops = {}
        self.visited_categories = []

        while len(self.current_stops.keys()) < self.number_of_stops:
            chosen_category = random.choice(list(AVAILABLE_CATEGORIES.keys()))

            if (
                chosen_category in self.visited_categories
                and not AVAILABLE_CATEGORIES[chosen_category]["repeat"]
            ):
                continue

            self.visited_categories.append(chosen_category)
            venue_name, venue_location = self.find_venue_by_category(chosen_category)

            self.current_stops[venue_name] = {
                **venue_location,
                "category": AVAILABLE_CATEGORIES[chosen_category]["name"],
            }
            self._current_venue_location = {
                "lat": venue_location["lat"],
                "lng": venue_location["lng"],
            }

        output = []
        for n, v in self.current_stops.items():
            output.append(f"{n}: {v['category']}")

        return output


if __name__ == "__main__":
    INPUT = {
        "number_of_stops": 5,
        "current_location": {"lat": 40.6865628, "lng": -73.977101},
        "final_destination": {"lat": 40.6863959, "lng": -73.9719153},
    }

    friday = FridayNight(preference_profile=INPUT)
    friday.create_thread()
