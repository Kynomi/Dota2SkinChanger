from functions import *
import dearpygui.dearpygui as dpg


class Interface(object):

    def __init__(self):
        super().__init__()
        data, heroes = configparser()
        self.steam_path = data[0]['steam_path']
        self.slots = heroes[0]['heroes']
        heroes = []
        for i in self.slots:
            heroes.append(i)
        self.heroes = heroes
        self.current_items = []
        self.view_resizable = True
        self.width = data[0]['width']
        self.height = data[0]['height']
        self.items = []
        self.interface()
        self.current_hero = None
        self.current_slot = None
        if data[0]['first_start'] is True or os.path.exists('config.yaml') is False:
            print('first_start')
            first_step(steam_path=self.steam_path)

    def heroes_search(self, sender, app_data):
        heroes_new = []
        if app_data is not None or not '':
            for i in self.heroes:
                if app_data.lower() in i.lower():
                    heroes_new.append(i)
            dpg.configure_item("Heroes_list", items=heroes_new)
        else:
            dpg.configure_item("Heroes_list", items=self.heroes)

    def items_search(self, sender, app_data):
        items_new = []
        if app_data is not None or not '':
            for i in self.items:
                if app_data.lower() in i.lower():
                    items_new.append(i)
            dpg.configure_item("Item_list", items=items_new)
        else:
            dpg.configure_item("Item_list", items=self.heroes)

    def view_menu_bar_button(self, sender, app_data):

        if sender == 'Heroes_menu_bar_button':
            dpg.configure_item('Heroes', collapsed=False, show=True)
        elif sender == 'Items_menu_bar_button':
            dpg.configure_item('Items', collapsed=False, show=True)
        elif sender == "Slots_menu_bar_button":
            dpg.configure_item('Slots', collapsed=False, show=True)
        elif sender == 'Resizable_menu_bar_button':
            if app_data is True:
                self.view_resizable = False
            else:
                self.view_resizable = True

    def select(self, sender, app_data):
        if sender == 'Heroes_list':
            dpg.configure_item('Item_list', items=[])
            dpg.configure_item('Slots_list', items=self.slots[app_data])
            self.current_hero = app_data
        elif sender == 'Slots_list':
            self.current_slot = app_data
            self.items = os.listdir('mods/' + self.current_hero + '/' + self.current_slot)
            dpg.configure_item('Item_list', items=self.items)
        elif sender == 'Item_list':
            if len(self.current_items) == 0:
                self.current_items.append(f'{self.current_hero}/{self.current_slot}/{app_data}')
                dpg.configure_item('Item_list_text', items=self.current_items)
            elif f'{self.current_hero}/{self.current_slot}/{app_data}' in self.current_items:
                pass
            else:
                repeat = False
                for i in self.current_items:
                    if f'{self.current_hero}/{self.current_slot}' in i:
                        index = self.current_items.index(i)
                        self.current_items[index] = f'{self.current_hero}/{self.current_slot}/{app_data}'
                        dpg.configure_item('Item_list_text', items=self.current_items)
                        repeat = True
                if repeat is False:
                    self.current_items.append(f'{self.current_hero}/{self.current_slot}/{app_data}')
                    dpg.configure_item('Item_list_text', items=self.current_items)

    def vpk_create(self):

        vpk_create(items_game=r'pak01_dir\scripts\items\items_game.txt', files=self.current_items,
                   path='pak01_dir', steam_path=self.steam_path)

    def interface(self):
        dpg.create_context()
        with dpg.font_registry():
            default_font = 'fonts/Roboto-Light.ttf'
            with dpg.font(default_font, 20) as default_font:
                dpg.add_font_range_hint(hint=dpg.mvFontRangeHint_Cyrillic)
            bold_font = 'fonts/Roboto-Bold.ttf'
            with dpg.font(bold_font, 18) as bold_font:
                dpg.add_font_range_hint(hint=dpg.mvFontRangeHint_Cyrillic)
        # styles
        with dpg.theme() as global_theme:
            cat = dpg.mvThemeCat_Core
            with dpg.theme_component(dpg.mvAll):
                # Roundings
                dpg.add_theme_style(dpg.mvStyleVar_FrameRounding, 12, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_WindowRounding, 12, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarRounding, 0, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_GrabRounding, 6, category=cat)
                # Main
                dpg.add_theme_style(dpg.mvStyleVar_WindowPadding, 10, 10, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_FramePadding, 8, 4, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_ItemSpacing, 13, 4, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_GrabMinSize, 9, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_ScrollbarSize, 13, category=cat)
                # Borders
                dpg.add_theme_style(dpg.mvStyleVar_FrameBorderSize, 1, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_WindowBorderSize, 1, category=cat)
                # Alignment
                dpg.add_theme_style(dpg.mvStyleVar_WindowTitleAlign, 0.5, 0.5, category=cat)
                dpg.add_theme_style(dpg.mvStyleVar_SelectableTextAlign, 0.0, 0.5, category=cat)
                # Colors
                dpg.add_theme_color(dpg.mvThemeCol_WindowBg, (13, 19, 33), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_ChildBg, (29, 45, 68), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_Border, (240, 235, 216), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBg, (62, 92, 118), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgActive, (13, 19, 33), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBg, (116, 140, 171, 255), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgActive, (29, 45, 68, 255), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_TitleBgCollapsed, (0, 0, 0, 125), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_CheckMark, (0, 0, 0), category=cat)
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (10, 67, 47, 103), category=cat)
        dpg.add_viewport_menu_bar(tag='Menu_bar')
        dpg.add_menu(parent="Menu_bar", label='Файл', tag='Files')
        dpg.add_menu_item(label='Собрать моды', parent='Files', callback=self.vpk_create)
        dpg.add_menu_item(label='Настройки', parent='Files')
        dpg.add_menu_item(label='Появились новые герои', parent='Files')
        dpg.add_menu_item(label='Добавить моды', parent='Files')
        dpg.add_menu(parent='Menu_bar', label='Окна', tag='View')
        dpg.add_menu_item(label='Герои', parent='View', tag='Heroes_menu_bar_button',
                          callback=self.view_menu_bar_button)
        dpg.add_menu_item(label='Слоты', parent='View', tag='Slots_menu_bar_button',
                          callback=self.view_menu_bar_button)
        dpg.add_menu_item(label='Предметы', parent='View', tag='Items_menu_bar_button',
                          callback=self.view_menu_bar_button)
        dpg.add_checkbox(label='Закрепить размер окон', parent='View', tag='Resizable_menu_bar_button',
                         callback=self.view_menu_bar_button)
        with dpg.window(label="Герои", width=int(0.4*self.width), height=300, no_close=False,
                        no_resize=False, pos=[0, 30], tag='Heroes'):
            heroes_filter = dpg.add_input_text(label='поиск', callback=self.heroes_search)
            heroes_list = dpg.add_listbox(tag='Heroes_list', num_items=5, items=self.heroes, callback=self.select)
            dpg.bind_font(default_font)
        with dpg.window(label='Слоты', width=int(0.4*self.width), height=300, no_resize=False,
                        no_close=False, pos=[int(0.4*self.width), 30], tag='Slots'):
            slots_list = dpg.add_listbox(tag='Slots_list', num_items=5, items=[], callback=self.select)
            dpg.bind_font(default_font)
        with dpg.window(label='Предметы', width=int(0.3*self.width), height=420, no_resize=False,
                        no_close=False, pos=[0, 329], tag='Items'):
            items_filter = dpg.add_input_text(label='поиск', callback=self.items_search)
            item_list = dpg.add_listbox(tag='Item_list', num_items=5, items=self.items, callback=self.select)
        with dpg.window(no_title_bar=True, width=int(0.5*self.width), height=420,
                        pos=[int(0.3*self.width), 329], tag='Current_mods'):
            item_list_text = dpg.add_text(default_value='Моды которые вы выбрали:')
            current_item_list = dpg.add_listbox(items=self.current_items, width=400, tag='Item_list_text')
        # Font
        dpg.bind_item_font(heroes_list, bold_font)
        dpg.bind_item_font(slots_list, bold_font)
        dpg.bind_item_font(item_list, bold_font)
        dpg.bind_item_font(heroes_filter, bold_font)
        dpg.bind_item_font(items_filter, bold_font)
        dpg.bind_item_font(item_list_text, bold_font)
        dpg.bind_item_font(current_item_list, bold_font)
        dpg.bind_theme(global_theme)
        dpg.create_viewport(title='D2MO v4.0', width=self.width, resizable=True, clear_color=(20, 33, 61),
                            min_width=1024, min_height=720)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            width = dpg.get_viewport_width()
            height = dpg.get_viewport_height()
            dpg.render_dearpygui_frame()
            if self.view_resizable is False:
                pass
            elif self.view_resizable is True and self.width == width and self.height == height:
                pass
            else:
                self.width = dpg.get_viewport_width()
                self.height = dpg.get_viewport_height()
                dpg.configure_item('Heroes', width=int(0.4*self.width), height=300)
                dpg.configure_item('Slots', width=int(0.4*self.width), height=300)
                dpg.configure_item('Items', width=int(0.3*self.width), height=420)
                dpg.configure_item('Current_mods', width=int(0.5*self.width), height=420)
        dpg.destroy_context()


def main():
    Interface()


if __name__ == '__main__':
    main()
