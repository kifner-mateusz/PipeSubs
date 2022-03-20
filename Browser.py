import webbrowser


class Browser:
    """ obsługuje otwieranie przeglądarki (myslałem że będzie tu więcej) """

    def __init__(self):
        # TODO: możliwość wybrania przeglądarki
        self._browser_path = ""

    def open_webpage(self, url):
        """ Otwiera przeglądarkę z podanym url  """
        webbrowser.get().open(url, new=2)
