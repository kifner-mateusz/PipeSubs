from PipeDatabase import PipeDatabase
from YouTubeDL import YouTubeDL
import requests
import os
from Categories import Categories
from DearPyGuiWrapper import DearPyGuiWrapper
from Browser import Browser
import pyperclip


class App(DearPyGuiWrapper):

    def __init__(self):
        super().__init__("PipeSubs")
        self.pipeDatabase = None
        self.ytdl = YouTubeDL()
        self.debug = False
        self.categories = Categories()
        self.browser = Browser()
        if not(os.path.exists("./.cache")):
            os.makedirs("./.cache")
        # load icons
        with self.dpg.texture_registry():
            for icon in self.categories.get_categories():
                try:
                    width, height, channels, data = self.dpg.load_image(
                        "./FeedGroupIcons/"+icon[1])
                    self.dpg.add_static_texture(
                        width, height, data, tag=icon[1])
                except:
                    if self.debug:
                        print("loading icon "+icon[0]+" failed ("+icon[1]+")")

        self.tabs = ("Subscriptions", "Feed_groups",
                     "Feed_group_sub_join", "Playlists", "Playlist_stream_join", "Streams")
        self.add_icon = 0
        self.current_sub = 0
        with self.dpg.menu_bar(parent="Window"):
            # przycisk do ładowania plików, po wciśnięciu pokazuje okno wyboru plików
            self.dpg.add_button(
                label="Load", callback=lambda: self.dpg.show_item("file_dialog_load_id"))
            # etykietka pokazuje status połączenia
            self.dpg.add_text("nie wybrano bazy danych", tag="status",
                              color=(150, 150, 150, 255))

        with self.dpg.group(horizontal=True, parent="Window"):
            self.dpg.add_button(label="Subscriptions",
                                callback=self.change_tab, user_data="Subscriptions")
            self.dpg.add_button(label="Feed groups", callback=self.change_tab,
                                user_data="Feed_groups")
            self.dpg.add_button(label="Feed groups sub join", callback=self.change_tab,
                                user_data="Feed_group_sub_join")
            self.dpg.add_button(label="Playlists", callback=self.change_tab,
                                user_data="Playlists")
            self.dpg.add_button(label="Playlist_stream_join", callback=self.change_tab,
                                user_data="Playlist_stream_join")
            self.dpg.add_button(label="Streams", callback=self.change_tab,
                                user_data="Streams")

        # dodaj table z danymi
        with self.dpg.group(parent="Window"):
            self.dpg.add_table(header_row=True, policy=self.dpg.mvTable_SizingFixedFit, tag="Subscriptions",
                               borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True)
            self.dpg.add_table(header_row=True, policy=self.dpg.mvTable_SizingFixedFit, tag="Feed_groups",
                               borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, show=False)
            self.dpg.add_table(header_row=True, policy=self.dpg.mvTable_SizingFixedFit, tag="Feed_group_sub_join",
                               borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, show=False)
            self.dpg.add_table(header_row=True, policy=self.dpg.mvTable_SizingFixedFit, tag="Playlists",
                               borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, show=False)
            self.dpg.add_table(header_row=True, policy=self.dpg.mvTable_SizingFixedFit, tag="Playlist_stream_join",
                               borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, show=False)
            self.dpg.add_table(header_row=True, policy=self.dpg.mvTable_SizingFixedFit, tag="Streams",
                               borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, show=False)

            # grupa z polami tekstowymi do modyfikacji i dodawania nowych wierszy pod tabelą
        with self.dpg.group(horizontal=True, show=True, tag="add_section", parent="Window"):
            # dodaje pola tekstowe
            self.dpg.add_input_text(tag="id", width=20, enabled=False)
            self.dpg.add_input_text(tag="name", width=200, hint="Name")
            self.dpg.add_image_button(
                self.categories.get_category_icon(self.add_icon), tag="icon", callback=lambda: self.dpg.configure_item("modal_icon", show=True))
            # dodaje przycisk
            self.dpg.add_button(label="Add", tag="add_button",
                                callback=self.add_or_modify_feed_group)

        with self.dpg.file_dialog(directory_selector=False, show=False, callback=self.file_dialog_load, id="file_dialog_load_id", min_size=(int(self.get_size()[0]*0.8), int(self.get_size()[1]*0.8))):
            # dodaje rozpoznane rozszeżenia
            self.dpg.add_file_extension(".db", color=(
                150, 255, 150, 255), custom_text="[Sqlite3]")
            # dpg.add_file_extension(".*")

        with self.dpg.window(label="Choose icon", modal=True, show=False, id="modal_icon", no_title_bar=True):
            count = 0
            while(count < len(self.categories.get_categories())):
                row = 0
                with self.dpg.group(horizontal=True):
                    while(row < 10 and count < len(self.categories.get_categories())):
                        self.dpg.add_image_button(
                            self.categories.get_category_icon(count), user_data=count, callback=self.choose_icon)
                        count += 1
                        row += 1

        with self.dpg.window(label="Choose feed", show=False, id="modal_feed", height=self.get_size()[1]-130, width=self.get_size()[0], pos=[0, 0], no_move=True, no_resize=True, no_title_bar=True):
            with self.dpg.table(policy=self.dpg.mvTable_SizingFixedFit, tag="modal_feed_table",  borders_innerH=True, borders_outerH=True, borders_innerV=True, borders_outerV=True, header_row=False):
                self.dpg.add_table_column()
                with self.dpg.table_row():
                    self.dpg.add_text("testname", tag="sub_name")
                with self.dpg.table_row():
                    self.dpg.add_image(
                        self.categories.get_category_icon(0), tag="sub_icon")
                with self.dpg.table_row():
                    self.dpg.add_text("testdesc", tag="sub_desc")
                with self.dpg.table_row():
                    self.dpg.add_text("", tag="sub_group")
                with self.dpg.table_row():
                    self.dpg.add_button(
                        label="Open webpage", tag="sub_button", callback=self.open_webpage_callback, height=60, width=self.get_size()[0]-10)
                with self.dpg.table_row():
                    self.dpg.add_text("\n\nTitles of videos  ")
                    # self.dpg.add_image(self.categories.get_category_icon(0), tag="video_thum")
                with self.dpg.table_row():
                    self.dpg.add_text(
                        "", tag="video_title")

        with self.dpg.window(label="Choose feed buttons", show=False, id="modal_feed_buttons", height=120, width=self.get_size()[0]-110, pos=[0, self.get_size()[1]-130], no_move=True, no_resize=True, no_title_bar=True):
            self.dpg.add_group(horizontal=True, tag="feed_buttons")

        self.dpg.add_button(parent="Window", label="Start Sorting", height=60, width=110,
                            pos=[self.get_size()[0]-110, 28], callback=self.start_sorting, show=False, tag="start_sorting")
        self.dpg.add_button(parent="Window", label="  Exit Sort  ", height=100, width=110,
                            pos=[self.get_size()[0]-110, self.get_size()[1]-100], callback=self.end_sorting, show=False, tag="end_sorting")

    def set_table_subsciptions(self, parent, clear_cache=False):
        """ ustawia/aktualizuje dane w tablicy subscriptions w gui """
        self.dpg.delete_item(parent, children_only=True)
        self.dpg.add_table_column(label="uid / name", parent=parent)
        self.dpg.add_table_column(label="avatar", parent=parent)
        self.dpg.add_table_column(label="description", parent=parent)

        for sub in self.pipeDatabase.get_data("subscriptions", clear_cache=clear_cache):
            with self.dpg.table_row(parent=parent):
                with self.dpg.table_cell():
                    self.dpg.add_text(default_value=sub[0])
                    self.dpg.add_text(default_value=sub[3])
                # print(sub[4])
                if not(os.path.exists("./.cache/"+sub[3]+".png")):
                    if self.debug:
                        print("not in cashe: ", sub[3])
                    with open("./.cache/"+sub[3]+".png", 'wb') as f:
                        f.write(requests.get(sub[4]).content)
                try:
                    width, height, channels, data = self.dpg.load_image(
                        "./.cache/"+sub[3]+".png")

                    with self.dpg.texture_registry():
                        self.dpg.add_static_texture(
                            width, height, data, tag=sub[3]+"_image")
                except:
                    if self.debug:
                        print("loading image for "+sub[3]+" failed")
                with self.dpg.table_cell():
                    try:
                        self.dpg.add_image(sub[3]+"_image")
                    except:
                        pass
                with self.dpg.table_cell():
                    self.dpg.add_text(default_value=sub[6])

    def set_table_feed_groups(self, parent, clear_cache=False):
        """ ustawia/aktualizuje dane w tablicy feed_group w gui """

        self.dpg.delete_item(parent, children_only=True)
        self.dpg.add_table_column(label="uid", parent=parent)
        self.dpg.add_table_column(label="name", parent=parent)
        self.dpg.add_table_column(label="icon", parent=parent)
        self.dpg.add_table_column(parent=parent)
        self.dpg.add_table_column(parent=parent)
        for data in self.pipeDatabase.get_data("feed_group", clear_cache=clear_cache):
            with self.dpg.table_row(parent=parent):
                with self.dpg.table_cell():
                    self.dpg.add_text(data[0])
                with self.dpg.table_cell():
                    self.dpg.add_text(data[1])
                with self.dpg.table_cell():
                    self.dpg.add_image(
                        self.categories.get_category_icon(data[2]))
                with self.dpg.table_cell():
                    self.dpg.add_button(
                        label="update", callback=self.update_feed_group_callback, user_data=data)
                with self.dpg.table_cell():
                    self.dpg.add_button(
                        label="remove", callback=self.remove_feed_group_callback, user_data=data[0])

    def set_table_feed_group_sub_join(self, parent, clear_cache=False):
        """ ustawia/aktualizuje dane w tablicy feed_group_subscription_join w gui """

        self.dpg.delete_item(parent, children_only=True)
        self.dpg.add_table_column(label="group_id", parent=parent)
        self.dpg.add_table_column(label="subscription_id", parent=parent)
        feed_group = self.pipeDatabase.get_data("feed_group")
        feed_group_subscription_join = self.pipeDatabase.get_data(
            "feed_group_subscription_join", clear_cache=clear_cache)
        subscriptions = self.pipeDatabase.get_data("subscriptions")
        all_feed_group_subscription_join = []
        for fg in feed_group:
            with self.dpg.table_row(parent=parent):
                with self.dpg.table_cell():
                    self.dpg.add_text(fg[1])
                    self.dpg.add_image(
                        self.categories.get_category_icon(fg[2]))
                with self.dpg.table_cell():
                    for data in feed_group_subscription_join:
                        if (data[0] == fg[0]):
                            sub = None
                            for s in subscriptions:
                                if (s[0] == data[1]):
                                    all_feed_group_subscription_join.append(
                                        s[0])
                                    self.dpg.add_button(
                                        label=s[3]+" (click to remove)", callback=self.remove_feed_group_sub_join_callback, user_data=(data[0], data[1]))
        with self.dpg.table_row(parent=parent):
            with self.dpg.table_cell():
                self.dpg.add_text("NOT GROUPED")
            with self.dpg.table_cell():
                for sub in subscriptions:
                    if not sub[0] in all_feed_group_subscription_join:
                        self.dpg.add_text(sub[3])
        # print(all_feed_group_subscription_join)

    def set_table_playlists(self, parent, clear_cache=False):
        self.dpg.delete_item(parent, children_only=True)
        self.dpg.add_table_column(label="uid", parent=parent)
        self.dpg.add_table_column(label="name", parent=parent)
        self.dpg.add_table_column(label="urls", parent=parent)
        self.dpg.add_table_column(label="thumbnail", parent=parent)
        streams = self.pipeDatabase.get_data("streams")
        playlist_stream_join = self.pipeDatabase.get_data(
            "playlist_stream_join")
        for data in self.pipeDatabase.get_data("playlists"):
            with self.dpg.table_row(parent=parent):
                with self.dpg.table_cell():
                    self.dpg.add_text(data[0])
                with self.dpg.table_cell():
                    self.dpg.add_text(data[1])
                with self.dpg.table_cell():
                    videos_str = ""
                    for join_stream in playlist_stream_join:
                        if (data[0] == join_stream[0]):
                            for st in streams:
                                if (join_stream[1] == st[0]):
                                    videos_str += st[2] + "\n"
                    self.dpg.add_button(
                        label="copy to clipboard", callback=self.copy_to_clipboard, user_data=videos_str)
                    self.dpg.add_text(videos_str)

                with self.dpg.table_cell():
                    self.dpg.add_button(
                        label=data[2], callback=self.copy_to_clipboard, user_data=data[2])
                    # self.dpg.add_text(data[2])

    def set_table(self, parent, table_name, clear_cache=False):
        self.dpg.delete_item(parent, children_only=True)
        for column in self.pipeDatabase.get_columns(table_name):
            self.dpg.add_table_column(label=column[1], parent=parent)
        for data in self.pipeDatabase.get_data(table_name, clear_cache=clear_cache):
            with self.dpg.table_row(parent=parent):
                for d in data:
                    with self.dpg.table_cell():
                        if type(d) == str and d.startswith("http"):
                            self.dpg.add_button(
                                label="url", user_data=d, callback=self.open_webpage_callback)
                        else:
                            self.dpg.add_text(d)

    def refresh(self, clear_cache=True):
        """ ustawia/aktualizuje dane w tablicach w gui  """
        self.set_table_subsciptions("Subscriptions", clear_cache=clear_cache)
        self.set_table_feed_groups("Feed_groups", clear_cache=clear_cache)
        self.set_table_feed_group_sub_join(
            "Feed_group_sub_join", clear_cache=clear_cache)
        self.set_table_playlists(
            "Playlists", clear_cache=clear_cache)
        self.set_table(
            "Playlist_stream_join", "playlist_stream_join", clear_cache=clear_cache)
        self.set_table(
            "Streams", "streams", clear_cache=clear_cache)

    def update_feed_group_callback(self, sender, app_data, user_data):
        """ callback przycisku, przygotowuje dane wiersza z feed_group do edycji """
        self.dpg.set_value("id", user_data[0])
        self.dpg.set_value("name", user_data[1])
        self.add_icon = user_data[2]
        self.dpg.configure_item(
            "icon", texture_tag=self.categories.get_category_icon(self.add_icon))
        self.dpg.configure_item("add_button", label="update")

    def remove_feed_group_callback(self, sender, app_data, user_data):
        """ callback przycisku, przekazuej wiersz z feed_group do usunięcia """
        self.remove_feed_group(user_data)

    def add_feed_group(self, name, icon_id, sort_order=0):
        """ dodaje wiersz do feed_group """
        self.pipeDatabase.add_row(
            "feed_group", name=name, icon_id=icon_id, sort_order=sort_order)
        self.refresh()

    def remove_feed_group(self, uid):
        """ usuwa wiersz z feed_group oraz wszystkie asociacje """
        self.pipeDatabase.remove_row("feed_group", uid=uid)
        self.pipeDatabase.remove_all_with(
            "feed_group_subscription_join", group_id=uid)
        self.refresh()

    def update_feed_group(self, uid, name, icon_id,  sort_order=0):
        """ aktualizuje dane wiersza w feed_group """
        self.pipeDatabase.update_row(
            "feed_group", uid=uid, name=name, icon_id=icon_id, sort_order=sort_order)
        self.refresh()

    def add_feed_group_sub_join(self, group_id, subscription_id):
        """ dodaje asocjacje feed_group z subscrypcją, jeśli nie istnieje """
        for fg_sub_join in self.pipeDatabase.get_data("feed_group_subscription_join"):
            if (fg_sub_join[0] == group_id and fg_sub_join[1] == subscription_id):
                print("already added")
                return
        self.pipeDatabase.add_row(
            "feed_group_subscription_join", group_id=group_id, subscription_id=subscription_id)
        # self.refresh()

    def remove_feed_group_sub_join_callback(self, sender, app_data, user_data):
        """ callback przycisku, przekazuje asocjacje feed_group z subscrypcją do usunięcia """
        self.remove_feed_group_sub_join(user_data[0], user_data[1])

    def remove_feed_group_sub_join(self,  group_id, subscription_id):
        """ usuwa asocjacje feed_group z subscrypcją """
        # print(group_id, subscription_id)
        self.pipeDatabase.remove_all_with(
            "feed_group_subscription_join", group_id=group_id, subscription_id=subscription_id)
        self.refresh()

    def change_tab(self, tag, app_data, user_data):
        """ zmienia zakładkę w gui """
        for tab in self.tabs:
            self.dpg.configure_item(tab, show=False)
        self.dpg.configure_item(user_data, show=True)
        self.dpg.configure_item(
            "add_section", show=(user_data == "Feed_groups"))
        self.dpg.configure_item("start_sorting",
                                show=(user_data == "Feed_group_sub_join"))

    def choose_icon(self, tag, app_data, user_data):
        """ callback przycisku, wyświetla menu do wyboru ikony """
        self.dpg.configure_item("modal_icon", show=False)
        self.add_icon = user_data
        self.dpg.configure_item(
            "icon", texture_tag=self.categories.get_category_icon(self.add_icon))

    def add_or_modify_feed_group(self, tag, app_data, user_data):
        """ callback przycisku, dodaje lub modyfikuje feed_group, jest to zależne od tego czy podano id"""
        if (self.dpg.get_value("id") == ""):
            name = self.dpg.get_value("name")
            self.add_feed_group(name, self.add_icon)
        else:
            uid = self.dpg.get_value("id")
            name = self.dpg.get_value("name")
            self.update_feed_group(uid, name, self.add_icon)
            self.dpg.set_value("id", "")
            self.dpg.set_value("name", "")
            self.add_icon = 0
            self.dpg.configure_item(
                "icon", texture_tag=self.categories.get_category_icon(self.add_icon))
            self.dpg.configure_item("add_button", label="add")

    def file_dialog_load(self, sender, file_data):
        """ callback, otwiera bazę podaną z przęglądarki plików """
        # print(file_data)
        self.pipeDatabase = PipeDatabase(file_data["file_path_name"])
        self.dpg.set_value("status", file_data["file_path_name"])
        self.refresh()
        print("tables: ", self.pipeDatabase.get_tables(), "\n")
        print("subscriptions: ", self.pipeDatabase.get_columns(
            "Subscriptions"), "\n")
        print("feed_groups: ", self.pipeDatabase.get_columns("feed_group"), "\n")
        print("feed_groups_sub_join: ", self.pipeDatabase.get_columns(
            "feed_group_subscription_join"), "\n")
        print("playlists: ", self.pipeDatabase.get_columns(
            "playlists"), "\n")
        print("playlist_stream_join: ", self.pipeDatabase.get_columns(
            "playlist_stream_join"), "\n")
        print("streams: ", self.pipeDatabase.get_columns(
            "streams"), "\n")

    def start_sorting(self, sender, app_data, user_data):
        """ callback przycisku, rozpoczyna przydzialanie subskrybcji do grup, wyświetla wszytkie wymagane okna gui """
        self.dpg.configure_item("start_sorting", show=False)
        self.dpg.configure_item("modal_feed_buttons", show=True, height=100, width=self.get_size()[
                                0]-110, pos=[0, self.get_size()[1]-100])
        self.dpg.configure_item("end_sorting", show=True)
        self.dpg.configure_item("modal_feed", show=True, height=self.get_size()[
                                1]-100, width=self.get_size()[0], pos=[0, 0])
        # self.dpg.configure_item("modal_feed", show=True)

        self.current_sub = 0
        self.dpg.delete_item("feed_buttons", children_only=True)

        feed_group = self.pipeDatabase.get_data("feed_group")
        for fg in feed_group:
            with self.dpg.group(parent="feed_buttons"):
                self.dpg.add_image_button(
                    self.categories.get_category_icon(fg[2]), callback=self.sort_choose_feed, user_data=fg[0], width=92)
                self.dpg.add_button(
                    label=fg[1], callback=self.sort_choose_feed, user_data=fg[0], width=100)
        self.dpg.add_button(
            label="Skip", callback=self.sort_choose_feed, user_data="skip", height=60, width=60, parent="feed_buttons")
        self.set_subscription_data(0)

    def end_sorting(self, sender, app_data, user_data):
        """ callback przycisku, kończy przydzialanie subskrybcji do grup, zamyka wszystkie związane okna """
        self.dpg.configure_item("start_sorting", show=True)
        self.dpg.configure_item("modal_feed_buttons", show=False)
        self.dpg.configure_item("end_sorting", show=False)
        self.dpg.configure_item("modal_feed", show=False)
        self.refresh()

    def sort_choose_feed(self, sender, app_data, user_data):
        """ callback przycisku, wyświetla kolejną subskrypcję do przydzielenia do grupy """
        self.dpg.set_value("video_title", "")
        subscriptions = self.pipeDatabase.get_data("subscriptions")
        if str(user_data) != "skip":
            uid = subscriptions[self.current_sub][0]
            # print(user_data, uid)
            self.add_feed_group_sub_join(user_data, uid)
        self.current_sub += 1
        if self.current_sub < len(subscriptions):
            self.set_subscription_data(self.current_sub)
        else:
            self.end_sorting("", None, None)

    def set_subscription_data(self, id):
        """ funkcja pomocnicza, ustawia dane subskrypcji w gui od wyboru grupy """
        sub = self.pipeDatabase.get_data("subscriptions")[id]
        # print(sub)
        self.dpg.set_value("sub_name", sub[3])
        self.dpg.configure_item(
            "sub_icon", texture_tag=sub[3]+"_image")
        self.dpg.set_value("sub_desc", sub[6])
        self.dpg.configure_item("sub_desc", wrap=self.get_size()[0]-20)
        self.dpg.configure_item("sub_button", user_data=sub[2])

        # self.ytdl.get_channel_data_callback_async(
        #     sub[2], self.set_subscription_data_async_callback)

        count = 0
        videos_str = ""
        streams = self.pipeDatabase.get_data("streams")
        for stream in streams:
            if (sub[3] == stream[6]):
                videos_str += stream[3] + "\n"
                if (count > 10):
                    break
                count += 1
        self.dpg.set_value("video_title", videos_str)

        feed_group = self.pipeDatabase.get_data("feed_group")
        group_str = ""
        for sub_join in self.pipeDatabase.get_data(
                "feed_group_subscription_join"):
            if sub_join[1] == sub[0]:
                for fg in feed_group:
                    if fg[0] == sub_join[0]:
                        group_str += fg[1]+"\n"
        self.dpg.set_value("sub_group", group_str)

    # def set_subscription_data_async_callback(self, data):
    #     """ callback, przyjmuje asynchronicznie dane o filmach na kanale i wyświetla listę """
    #     # Texture loading is not avaiable now

    #     # print("data:", data)
    #     # video_data = data[0]
    #     # if not(os.path.exists("./.cache/"+video_data["title"]+".jpg")):
    #     #     if self.debug:
    #     #         print("not in cashe: ", video_data["title"])
    #     #     with open("./.cache/"+video_data["title"]+".jpg", 'wb') as f:
    #     #         f.write(requests.get(video_data["thumbnail"]).content)
    #     # # try:
    #     # width, height, channels, img_data = self.dpg.load_image(
    #     #     "./.cache/"+video_data["title"]+".jpg")

    #     # with self.dpg.texture_registry():
    #     #     self.dpg.add_static_texture(
    #     #         width, height, img_data, tag=video_data["title"]+"_image")
    #     # self.dpg.configure_item(
    #     #     "video_thum", texture_tag=video_data["title"]+"_image")
    #     # # except:
    #     # #     if self.debug:
    #     # #         print("loading image for "+video_data["title"]+" failed")
    #     if (data["title"].startswith(self.dpg.get_value("sub_name"))):
    #         vid_str = ""
    #         for vid in data["entries"]:
    #             vid_str += vid["title"]+"\n"
    #         self.dpg.set_value("video_title", vid_str)

    def open_webpage_callback(self, sender, app_data, user_data):
        """ callback przycisku, otiera stronę internetową z kanałem """
        # print(user_data)
        self.browser.open_webpage(user_data)

    def copy_to_clipboard(self, sender, app_data, user_data):
        pyperclip.copy(user_data)

    def __del__(self):
        """ upewnia się że baza danych jest zamknięta """
        if self.pipeDatabase:
            self.pipeDatabase.__del__()


if __name__ == "__main__":
    App()
