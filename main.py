from functions import *
import dearpygui.dearpygui as dpg
class Interface(object):
    def __init__(self, heroes, slots, items, width, height):
        super().__init__()
        self.view_resizable = True
        self.width = width
        self.height = height
        self.items = items
        self.heroes = heroes
        self.slots = slots
        print(slots[0])
        self.interface()

    def heroes_search(self,sender, App_data):
        heroes_new = []
        if App_data is not None or not '':
            for i in self.heroes:
                if App_data in i:
                    heroes_new.append(i)
            dpg.configure_item("Heroes_list", items=heroes_new)
    def items_search(self, sender, App_data):
        items_new = []
        if App_data is not None or not '':
            for i in self.items:
                if App_data in i:
                    items_new.append(i)
            dpg.configure_item("Item_list", items=items_new)
    def interface(self):
        dpg.create_context()
        with dpg.font_registry():
            default_font = 'fonts/Roboto-Light.ttf'
            with dpg.font(default_font, 20) as default_font:
                dpg.add_font_range_hint(hint=dpg.mvFontRangeHint_Cyrillic)
            bold_font = 'fonts/Roboto-Bold.ttf'
            with dpg.font(bold_font, 18) as bold_font:
                dpg.add_font_range_hint(hint=dpg.mvFontRangeHint_Cyrillic)
        #styles
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
                dpg.add_theme_color(dpg.mvThemeCol_FrameBgHovered, (10,67,47,103), category=cat)

        dpg.add_viewport_menu_bar(tag='Menu_bar')
        dpg.add_menu(parent="Menu_bar", label='Файлы', tag='Files')
        dpg.add_menu_item(label='Собрать моды', parent='Files')
        dpg.add_menu_item(label='Настройки', parent='Files')
        dpg.add_menu(parent='Menu_bar', label='Окна', tag='View')
        dpg.add_menu_item(label='Герои', parent='View')
        dpg.add_menu_item(label='Слоты', parent='View')
        dpg.add_menu_item(label='Предметы', parent='View')
        dpg.add_checkbox(label='Закрепить размер окон', parent='View', callback=self.View_resizable)
        with dpg.window(label="Герои", width=int(0.4*self.width), height=300, no_close=True, no_resize=False, pos=[0, 30], tag='Heroes'):
            Heroes_filter = dpg.add_input_text(label='поиск', callback=self.heroes_search)
            Heroes_list = dpg.add_listbox(tag='Heroes_list', num_items=5, items=self.heroes, callback=self.Hero_select)
            dpg.bind_font(default_font)
        with dpg.window(label='Слоты', width=int(0.4*self.width), height=300, no_resize=False, no_close=True, pos=[int(0.4*self.width), 30], tag='Slots'):
            Slots_list = dpg.add_listbox(tag='Slots_list', num_items=5, items=[])
            dpg.bind_font(default_font)
        with dpg.window(label='Предметы', width=int(0.3*self.width), height=420, no_resize=False, no_close=True, pos=[0,329], tag='Items'):
            Items_filter = dpg.add_input_text(label='поиск', callback=self.items_search)
            Item_list = dpg.add_listbox(tag='Item_list', num_items=5, items=self.items)
            pass
        #Font
        dpg.bind_item_font(Heroes_list, bold_font)
        dpg.bind_item_font(Slots_list, bold_font)
        dpg.bind_item_font(Item_list, bold_font)
        dpg.bind_item_font(Heroes_filter, bold_font)
        dpg.bind_item_font(Items_filter, bold_font)
        dpg.bind_theme(global_theme)
        dpg.create_viewport(title='D2MO v4.0', width=self.width, resizable=True, clear_color=(20, 33, 61), min_width=(1024), min_height=720)
        dpg.setup_dearpygui()
        dpg.show_viewport()
        while dpg.is_dearpygui_running():
            dpg.render_dearpygui_frame()
            if self.view_resizable == False:
                pass
            elif self.view_resizable==True and self.width==dpg.get_viewport_width() and self.height==dpg.get_viewport_height():
                pass
            else:
                self.width = dpg.get_viewport_width()
                self.height = dpg.get_viewport_height()
                dpg.configure_item('Heroes', width=int(0.4*self.width), height=300)
                dpg.configure_item('Slots', width=int(0.4*self.width), height=300, pos=[int(0.4*self.width), 30])
                dpg.configure_item('Items', width=int(0.3*self.width), height=420)




        dpg.destroy_context()
    def View_resizable(self, sender, App_data):
        if App_data == True:
            self.view_resizable = False
        else:
            self.view_resizable = True
    def Hero_select(self, sender, App_data):
        dpg.configure_item('Slots_list', items=self.slots[int(App_data)])

def main():
    items = []
    heroes = []
    slots = {}
    first_start, steam_path, width, height = ConfigParser()
    for i in range(0, 5):
        heroes.append(str(i))
    for i in range(0, 5):
        list = []
        for n in range(0, 1+i):
            list.append(str(n))
        slots[i] = list
    for i in range(0, 5):
        items.append(str(i))
    Interface(heroes, slots, items, width=width, height=height)

if __name__ == '__main__':
    main()