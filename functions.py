import os
import yaml
import re
from zipfile import *
import shutil
from bs4 import BeautifulSoup
import requests
import random

def create_config():
    config_info = [
        {
            'first_start': False,
            'steam_path': "C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game",
            'width': 1280,
            'height': 720
        }
    ]
    with open("config.yaml", 'w') as yaml_config:
        yaml.dump(config_info, yaml_config)
        yaml_config.close()


def first_step(steam_path, heroes):              #Первый запуск, создание нужных директорий
    if not os.path.exists(steam_path+'\D2MO'):
        os.mkdir(steam_path+"\D2MO", mode=511, dir_fd=None)
        print("directories were created")
    if not os.path.exists('config.yaml'):
        create_config()
    with open('config.yaml', 'r') as yaml_config:
        data = yaml.load(yaml_config, yaml.FullLoader)
        yaml_config.close()
    with open('config.yaml', 'w') as yaml_config:
        data[0]['first_start'] = False
        yaml.dump(data, yaml_config)
        yaml_config.close()
    if not os.path.exists('mods'):
        os.mkdir('mods')
    with open('heroes.yaml', 'r', encoding='utf-8') as hero_yaml:
        heroes = yaml.load(hero_yaml, yaml.FullLoader)[0]['heroes']
        for i in heroes:
            if os.path.exists('mods/' + i):
                for n in heroes[i]:
                    if not os.path.exists('mods/' + i + '/' + n):
                        os.mkdir('mods/' + i + '/' + n)
            else:
                os.mkdir('mods/' + i)
                for n in heroes[i]:
                    if not os.path.exists('mods/' + i + '/' + n):
                        os.mkdir('mods/' + i + '/' + n)

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
    with open('config.yaml', 'r', encoding='utf-8') as yaml_config:
        data = yaml.load(yaml_config, yaml.FullLoader)
    with open('heroes.yaml', 'r', encoding='utf-8') as hero_config:
        heroes = yaml.load(hero_config, yaml.FullLoader)

    return data, heroes
def Dota2HeroesParser():
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    url = 'https://www.dotabuff.com/heroes'
    response = requests.get(url=url, headers=headers, timeout=1000000)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', {'class': 'name'})
    with open('heroes.yaml', 'r', encoding='utf-8') as heroes_yaml:
        heroes = yaml.load(heroes_yaml, yaml.FullLoader)
        try:
            for i in quotes:
                if i.text not in heroes[0]['heroes']:
                    heroes[0]['heroes'][i.text] = ['0']
                    heroes_yaml.close()
                    print(heroes)
                with open('heroes.yaml', 'w', encoding='utf-8') as heroes_yaml:
                    yaml.dump(heroes, heroes_yaml, allow_unicode=True)
                    heroes_yaml.close()
        except:
            heroes = {'heroes': {}}
            for i in quotes:
                heroes['heroes'][i.text] = ['0']
            with open('heroes.yaml', 'w', encoding='utf-8') as heroes_yaml:
                yaml.dump(heroes, heroes_yaml, allow_unicode=True)
                heroes_yaml.close()



