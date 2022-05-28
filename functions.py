from os import system, path, mkdir, remove, removedirs, listdir
from yaml import dump, load, FullLoader
from re import findall
from zipfile import ZipFile
from shutil import move
from bs4 import BeautifulSoup
from requests import get
from time import sleep


def create_config():
    config_info = [
        {
            'first_start': False,
            'steam_path': r"C:\Program Files (x86)\Steam\steamapps\common\dota 2 beta\game",
            'width': 1280,
            'height': 720
        }
    ]
    with open("config.yaml", 'w') as yaml_config:
        dump(config_info, yaml_config)
        yaml_config.close()


def first_step(steam_path):              # Первый запуск, создание нужных директорий
    if not path.exists(steam_path+r'\D2MO'):
        mkdir(steam_path+r"\D2MO", mode=511, dir_fd=None)
        print("directories were created")
    if not path.exists('config.yaml'):
        create_config()
    with open('config.yaml', 'r') as yaml_config:
        data = load(yaml_config, FullLoader)
        yaml_config.close()
    with open('config.yaml', 'w') as yaml_config:
        data[0]['first_start'] = False
        dump(data, yaml_config)
        yaml_config.close()
    if not path.exists('mods'):
        mkdir('mods')
    with open('heroes.yaml', 'r', encoding='utf-8') as hero_yaml:
        heroes = load(hero_yaml, FullLoader)[0]['heroes']
        for i in heroes:
            if path.exists('mods/' + i):
                for n in heroes[i]:
                    if not path.exists('mods/' + i + '/' + n):
                        mkdir('mods/' + i + '/' + n)
            else:
                mkdir('mods/' + i)
                for n in heroes[i]:
                    if not path.exists('mods/' + i + '/' + n):
                        mkdir('mods/' + i + '/' + n)


def find_all(script):
    with open(script, encoding='utf-8', mode='r') as d2mo_script_file:
        text = d2mo_script_file.read()
        text_re = findall(r'({\W*"n..."[\s\S]+)\n.*"to"|({\W*"n..."[\s\S]+)\n.+\Z', text)
        return text_re


def vpk_create(items_game, files, pak_path, steam_path):
    if path.exists('pak01_dir'):
        system(r'rmdir /Q /S pak01_dir')
    else:
        print('no such directory')
    script = r"scripts\items\items_game.txt"
    command = rf'decompiler\decompiler.exe -i "{steam_path}\dota\pak01_dir.vpk" -f {script} --output "pak01_dir"'
    system(command)
    sleep(1)
    with open(items_game, encoding="utf-8", mode='r+') as items_game_file:
        items_game_text = items_game_file.read()
        for i in files:
            print(i)
            zip_file = ZipFile('mods/'+i, mode="r")
            zip_namelist = zip_file.namelist()
            for n in zip_namelist:
                if n.find('/') >= 0 and not n == "d2mo_scripts/" and not n.find('d2mo_scripts/script') >= 0:
                    zip_file.extract(n, pak_path)
                elif n.find('d2mo_scripts/script') >= 0:
                    zip_file.extract(n, pak_path)
                    text_re = find_all('pak01_dir/' + n)
                    print(n)
                    if text_re[0][0] in items_game_text:
                        items_game_text = items_game_text.replace(text_re[0][0], text_re[1][1])
                        remove('pak01_dir/' + n)
                    else:
                        print("NO such script in game's script file")
                        remove('pak01_dir/' + n)
        removedirs('pak01_dir/d2mo_scripts')
        items_game_file.seek(0)
        items_game_file.write(items_game_text)
        items_game_file.close()
        print('all done', path.exists('pak01_dir'))
        system(r"echo %cd% ")
        system(r'vpk\vpk.exe pak01_dir pak01_dir')
        if path.exists(rf'{steam_path}\D2MO\pak01_dir.vpk'):
            remove(rf'{steam_path}\D2MO\pak01_dir.vpk')
        move('pak01_dir.vpk', rf'{steam_path}\D2MO')


def configparser():
    with open('config.yaml', 'r', encoding='utf-8') as yaml_config:
        data = load(yaml_config, FullLoader)
    with open('heroes.yaml', 'r', encoding='utf-8') as hero_config:
        heroes = load(hero_config, FullLoader)

    return data, heroes


def dota2heroesparser():
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                      ' (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif'
                  ',image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'
    }
    url = 'https://www.dotabuff.com/heroes'
    response = get(url=url, headers=headers, timeout=1000000)
    soup = BeautifulSoup(response.text, 'lxml')
    quotes = soup.find_all('div', {'class': 'name'})
    with open('heroes.yaml', 'r', encoding='utf-8') as heroes_yaml:
        heroes = load(heroes_yaml, FullLoader)
        # noinspection PyBroadException
        try:
            for i in quotes:
                if i.text not in heroes[0]['heroes']:
                    heroes[0]['heroes'][i.text] = ['0']
                    heroes_yaml.close()
                    print(heroes)
                with open('heroes.yaml', 'w', encoding='utf-8') as heroes_yaml_config:
                    dump(heroes, heroes_yaml_config, allow_unicode=True)
                    heroes_yaml.close()
        except Exception:
            heroes = {'heroes': {}}
            for i in quotes:
                heroes['heroes'][i.text] = ['0']
            with open('heroes.yaml', 'w', encoding='utf-8') as heroes_yaml_config:
                dump(heroes, heroes_yaml_config, allow_unicode=True)
                heroes_yaml.close()
