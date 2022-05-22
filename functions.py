import os
import configparser
import re
from zipfile import *
import shutil
def first_step(steam_path):              #Первый запуск, создание нужных директорий
    os.mkdir(steam_path+"\game\D2MO", mode=511, dir_fd=None)
    print("directories were created")

def create_config(path):
    config = configparser.ConfigParser()
    config.add_section('D2MO')
    config.set("D2MO", "first_start", "True")
    config.set("D2MO", "path_steam", "C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game")
    with open("config.ini", 'w') as config_file:
        config.write(config_file)

def find_all(script):
    with open(script, encoding='utf-8', mode='r') as d2mo_script_file:
        text = d2mo_script_file.read()
        text_re = re.findall(r'({\W*"n..."[\s\S]+)\n.*"to"|({\W*"n..."[\s\S]+)\n.+\Z', text)
        return text_re

def vpk_create(items_game, files, path, steam_path):
    if os.path.exists('pak01_dir'):
        os.system(r'rmdir /Q /S pak01_dir')
    else:
        print('no such directory')
    os.system(rf'decompiler\decompiler.exe -i "{steam_path}\game\dota\pak01_dir.vpk" -f "scripts\items\items_game.txt" --output "pak01_dir"')
    with open(items_game, encoding="utf-8", mode='r+') as items_game_file:
        items_game_text = items_game_file.read()
        for i in files:
            print(i)
            zip_file = ZipFile('mods/'+i, mode="r")
            zip_namelist = zip_file.namelist()
            for n in zip_namelist:
                if n.find('/') >= 0 and not n == "d2mo_scripts/" and not n.find('d2mo_scripts/script') >= 0:
                    zip_file.extract(n, path)
                elif n.find('d2mo_scripts/script') >= 0:
                    zip_file.extract(n, path)
                    text_re = find_all('pak01_dir/' + n)
                    print(n)
                    if text_re[0][0] in items_game_text:
                        items_game_text = items_game_text.replace(text_re[0][0], text_re[1][1])
                        os.remove('pak01_dir/' + n)
                    else:
                        print("NO such script in game's script file")
                        os.remove('pak01_dir/' + n)
        os.removedirs('pak01_dir/d2mo_scripts')
        items_game_file.seek(0)
        items_game_file.write(items_game_text)
        items_game_file.close()
        print('all done', os.path.exists('pak01_dir'))
        os.system(r"echo %cd% ")
        os.system(r'vpk\vpk.exe pak01_dir pak01_dir')
        if os.path.exists(f'{steam_path}\game\D2MO\pak01_dir.vpk'):
            os.remove(f'{steam_path}\game\D2MO\pak01_dir.vpk')
        shutil.move('pak01_dir.vpk', f'{steam_path}\game\D2MO')

def ConfigParser():
    c = configparser.ConfigParser()
    c.read('config.ini')
    return c['D2MO']['first_start'], c['D2MO']['path_steam'], int(c['D2MO']['width']), int(c['D2MO']['height'])