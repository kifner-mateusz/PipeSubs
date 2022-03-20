
class Categories:
    def __init__(self):
        self._categories = (
            ("ALL", "asterisk.png"),
            ("MUSIC", "music_note.png"),
            ("EDUCATION", "school.png"),
            ("FITNESS", "fitness_center.png"),
            ("SPACE", "telescope.png"),
            ("COMPUTER", "computer.png"),
            ("GAMING", "videogame_asset.png"),
            ("SPORTS", "directions_bike.png"),
            ("NEWS", "campaign.png"),
            ("FAVORITES", "favorite.png"),
            ("CAR", "directions_car.png"),
            ("MOTORCYCLE", "motorcycle.png"),
            ("TREND", "trending_up.png"),
            ("MOVIE", "movie.png"),
            ("BACKUP", "backup.png"),
            ("ART", "palette.png"),
            ("PERSON", "person.png"),
            ("PEOPLE", "people.png"),
            ("MONEY", "attach_money.png"),
            ("KIDS", "child_care.png"),
            ("FOOD", "fastfood.png"),
            ("SMILE", "insert_emoticon.png"),
            ("EXPLORE", "explore.png"),
            ("RESTAURANT", "restaurant.png"),
            ("MIC", "mic.png"),
            ("HEADSET", "headset.png"),
            ("RADIO", "radio.png"),
            ("SHOPPING_CART", "shopping_cart.png"),
            ("WATCH_LATER", "watch_later.png"),
            ("WORK", "work.png"),
            ("HOT", "whatshot.png"),
            ("CHANNEL", "tv.png"),
            ("BOOKMARK", "bookmark.png"),
            ("PETS", "pets.png"),
            ("WORLD", "public.png"),
            ("STAR", "stars.png"),
            ("SUN", "wb_sunny.png"),
            ("RSS", "rss_feed.png"),
        )

    def get_category(self, id):
        return self._categories[id]

    def get_categories(self):
        return self._categories

    def get_category_icon(self, id):
        return self._categories[id][1]

    def get_category_name(self, id):
        return self._categories[id][0]
