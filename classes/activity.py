from dataclasses import dataclass

@dataclass
class Activity():
    # def __init__(self, activity_type, activity_name, year, age_rating, duration, source_url):
    #     self.activity_type = activity_type
    #     self.activity_name = activity_name
    #     self.year = year
    #     self.age_rating = age_rating
    #     self.duration = duration
    #     self.source_url = source_url
    activity_type: str
    activity_name: str
    year: int
    age_rating: str
    duration: int
    source_url: str
    categories: list
    description: str
    

    @staticmethod
    def runtime_to_minutes(runtime_str, round_up=False):
        # Parses the JustWatch runtime_str into minutes
        # Input format: runtime_str = '2h 28min'
        # If round_up, rounds up to the next 15-minute increment
        # logging.debug('Converting runtime:')
        # logging.debug(f'{runtime_str=}')
        if 'h' in runtime_str:
            # split into hours/minutes
            runtime_split = runtime_str.split("h")
            runtime_minutes = (int(runtime_split[0]) * 60) + int(runtime_split[1].split("min")[0])
        else:
            runtime_minutes = int(runtime_str.split("min")[0])
        # logging.debug(f'{str(runtime_minutes)=}')

        if round_up:
            # logging.debug('Rounding:')
            # runtime_rounded_up = runtime_minutes + 15 - (runtime_minutes % 15)
            # logging.debug(f'{str(runtime_rounded_up)=}')
            # return runtime_rounded_up
            return Activity.round_to_next_quarter_hr(runtime_minutes)
        else:
            return runtime_minutes

    @staticmethod
    def minutes_to_hour_and_minute(runtime_minutes):
        hours = runtime_minutes // 60
        minutes = runtime_minutes % 60
        return [hours, minutes]
    
    @staticmethod
    def round_to_next_quarter_hr(runtime_minutes):
        return runtime_minutes + 15 - (runtime_minutes % 15)


# @dataclass
# class Show(Activity):
#     # def __init__(self, activity_type, show_name, year, age_rating, runtime, source_url, genres, synopsis):
#     #     super().__init__(activity_type, show_name, year, age_rating, runtime, source_url)
#     #     self.genres = genres
#     #     self.synopsis = synopsis
#     genres: []
#     synopsis: str


# @dataclass
# class Movie(Show):
#     # def __init__(self, movie_name, year, age_rating, runtime, source_url, genres, synopsis):
#     #     super().__init__('movie', movie_name, year, age_rating, runtime, source_url, genres, synopsis)
#     pass


@dataclass
class Tvshow(Activity):
    # def __init__(self, show_name, year, age_rating, runtime, source_url, genres, synopsis, season_data):
    #     super().__init__(self, 'tv', show_name, year, age_rating, runtime, source_url, genres, synopsis)
    #     self.season_data = season_data
    season_data: list
    

# @dataclass
# class Boardgame(Activity):
#     # def __init__(self, game_name, year, age_rating, playtime, source_url, categories, description):
#     #     super().__init__('boardgame', game_name, year, age_rating, playtime, source_url)
#     #     self.categories = categories
#     #     self.description = description
#     categories: []
#     description: str


# @dataclass
# class Book(Activity):
#     # def __init__(self, book_name, year, age_rating, pages, source_url, genres, description, author):
#     #     super().__init__('book', book_name, year, age_rating, pages, source_url)
#     #     self.genres = genres
#     #     self.description = description
#     #     self.author = author
#     genres: []
#     description: str
#     author: str
