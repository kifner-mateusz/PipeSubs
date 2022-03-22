import youtube_dl
from threading import Thread, Lock
import json


class YouTubeDL:
    """ Klasa integruje się z youtube-dl i służy do pobierania danych o kanale na yt """

    def __init__(self):
        # self.cache = []
        self.last_index = -1
        self.lock = Lock()
        self.threads = []
        self.options = {'outtmpl': '%(id)s.%(ext)s', "skip_download": True,
                        "playlistend": 3, "quiet": True}

    # def get_channel_data_async(self, url):
    #     self.remove_stopped_threads()
    #     self.end += 1

    #     index = None
    #     with self.lock:
    #         self.last_index += 1
    #         index = self.last_index
    #         self.cache.append({"ready": False, "entries": []})
    #         self.threads.append(
    #             Thread(target=self.get_channel_data_to_cache, args=(url, index)))
    #     self.threads[index].start()
    #     return index

    # def get_data_from_cache(self, index):
    #     if not(self.cache[index]["ready"]):
    #         return
    #     del self.threads[index]
    #     return self.cache[index]["entries"]

    # def get_channel_data_to_cache(self, url, index):
    #     ytdl = youtube_dl.YoutubeDL(self.options)
    #     with ytdl:
    #         result = ytdl.extract_info(
    #             url
    #         )

    #         for entry in result["entries"]:
    #             for entry2 in entry["entries"]:
    #                 for tumb in entry2["thumbnails"]:
    #                     if (tumb["height"] == 188):
    #                         with self.lock:
    #                             self.cache[index]["entries"].append({
    #                                 "title": entry2["title"], "thumbnail": tumb["url"]
    #                             })
    #                             self.cache[index]["ready"] = True
    #                         end

    def get_channel_data_callback_async(self, url, callback):
        """ Tworzy nowy wątek w aplikacji i wywołuje w nim `get_channel_data_callback`"""
        self.remove_stopped_threads()
        index = None
        with self.lock:
            self.last_index += 1
            index = self.last_index
            # self.cache.append({"ready": False})
            self.threads.append(
                Thread(target=self.get_channel_data_callback, args=(url, callback)))
        self.threads[index].start()
        return index

    def get_channel_data_callback(self, url, callback):
        """ pobiera dane o filmach na kanale yt i odsyła je callbackiem jako słownik """
        ytdl = youtube_dl.YoutubeDL(self.options)
        channel_data = {"title": "", 'entries': []}
        with ytdl:
            # result = ytdl.extract_info(
            #     url
            # )
            # if result:
            #     channel_data = {"title": result["title"], 'entries': []}
            #     try:
            #         if "entries" in result:
            #             for entry in result["entries"]:
            #                 if "entries" in entry:
            #                     for entry2 in entry["entries"]:
            #                         if "thumbnails" in entry2:
            #                             for thum in entry2["thumbnails"]:
            #                                 if (thum["height"] == 188):
            #                                     with self.lock:
            #                                         channel_data["entries"].append({
            #                                             "title": entry2["title"], "thumbnail": thum["url"]
            #                                         })
            #                                     break
            #                         elif "entries" in entry2:
            #                             for entry3 in entry2["entries"]:
            #                                 if "thumbnails" in entry3:
            #                                     for thum in entry3["thumbnails"]:
            #                                         if (thum["height"] == 188):
            #                                             with self.lock:
            #                                                 channel_data["entries"].append({
            #                                                     "title": entry2["title"], "thumbnail": thum["url"]
            #                                                 })
            #                                             break
            #     except:
            #         pass

            callback(channel_data)
            return

    def remove_stopped_threads(self):
        """ Usuwa wątki które zakończyły pracę """
        for i in range(len(self.threads)):
            if self.threads[i] and not(self.threads[i].is_alive()):
                # del self.threads[i]
                self.threads[i] = None


if __name__ == "__main__":
    # testy
    ytdl = YouTubeDL()

    def data(d):
        print(d)

    index = ytdl.get_channel_data_callback_async(
        "https://www.youtube.com/channel/UCtxCXg-UvSnTKPOzLH4wJaQ", data)
    print(index)
    print("sync code")

    # index = ytdl.get_channel_data_callback_async(
    #     "https://www.youtube.com/c/explainingcomputers", data)
    # while not(ytdl.end == 0):
    #     pass
    # print(ytdl.threads)
    # ytdl.remove_stopped_threads()
    # print(ytdl.threads)
