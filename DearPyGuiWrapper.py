from threading import Thread
import dearpygui.dearpygui as dpg


class DearPyGuiWrapper:
    """ Wrapper for dearpygui window """

    def __init__(self, title):
        self._ready = False
        self._viewport_size = [1280, 720]
        self._title = title
        self.dpg = dpg
        self._gui_thread = Thread(target=self._start_gui)
        self._gui_thread.start()
        # self._del_callback = del_callback
        # wait for thread to init
        while not(self._ready):
            pass

    def _start_gui(self):
        self.dpg.create_context()
        self.dpg.create_viewport(
            title=self._title, width=self._viewport_size[0], height=self._viewport_size[1])
        self.dpg.add_window(label="Window", tag="Window")

        self.dpg.set_primary_window("Window", True)
        self.dpg.set_viewport_resize_callback(self._on_resize)
        self.dpg.setup_dearpygui()
        self.dpg.show_viewport()
        self._ready = True

        with self.dpg.font_registry():
            with self.dpg.font("Roboto-Regular.ttf", 16) as default_font:
                self.dpg.add_font_range(0x0100, 0x017F)
                self.dpg.bind_font(default_font)
        self.dpg.start_dearpygui()
        # call del before context gets destroyed, it won't be called automatically
        self.__del__()
        self.dpg.destroy_context()

    def _on_resize(self, sender, app_data, user_data):
        self._viewport_size = (app_data[0], app_data[1])

    def get_size(self):
        return self._viewport_size

    def get_title(self):
        return self._title

    def set_title(self, new_title):
        self.dpg.set_viewport_title(new_title)
        self._title = new_title

    def __del__(self):
        pass


if __name__ == "__main__":

    class TestApp(DearPyGuiWrapper):

        def __init__(self):
            self.count = 0
            DearPyGuiWrapper.__init__(self, "PipeSubs")
            self.dpg.add_button(
                parent="Window", callback=self.set_button_value)

        def set_button_value(self, sender, app_data, user_data):
            self.count += 1
            self.dpg.configure_item(sender, label=str(self.count))
            self.dpg.add_button(parent="Window")

    app = TestApp()
