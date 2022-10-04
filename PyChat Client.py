import pysftp, os, cutie

server = '89.86.152.239'
username = 'valjul'
password = 'bp2022pjt'
cnopts = pysftp.CnOpts(knownhosts=os.path.expanduser(os.path.join('~', '.ssh', 'fake_known_hosts')))
cnopts.hostkeys = None

def update_client(all_files_direct: list):
    if(cutie.prompt_yes_or_no('Autorisez-vous PyChat a téléchargé la mise à jour disponible sur le serveur ?')):
        try: os.mkdir('font')
        except: pass
        try: os.mkdir('textures')
        except: pass
        try: os.mkdir('receive')
        except: pass
        try: os.mkdir('send')
        except: pass
        with pysftp.Connection(host=server, username=username, password=password, private_key=".ppk", cnopts=cnopts) as sftp:
            try:
                for rang in range(1, len(all_files_direct)):
                    sftp.get(all_files_direct[rang], all_files_direct[rang][9:])
            except Exception as e:
                print(e)
                return False
        if('version.lxf' in os.listdir()): os.remove('version.lxf')
        with open('version.lxf', 'a', encoding='UTF-8') as file:
            file.write(all_files_direct[0])
        return True
    return False
    
def get_downloads():
    if('downloads.lxf' in os.listdir()): os.remove('downloads.lxf')
    with pysftp.Connection(host=server, username=username, password=password, private_key=".ppk", cnopts=cnopts) as sftp:
        sftp.get('./server_pychat/downloads.lxf', './downloads.lxf')
    with open('downloads.lxf', 'r', encoding='UTF-8') as file:
        final = file.readlines()
    for rang in range(len(final)):
        final[rang] = final[rang][:-1]
    return final

def meme_version():
    with open('downloads.lxf', 'r', encoding='UTF-8') as file:
        ver_downloads = file.readline()[:-1]
    if('version.lxf' not in os.listdir()): return False
    with open('version.lxf', 'r', encoding='UTF-8') as file:
        ver_origin = file.readline()
    return ver_downloads == ver_origin

if __name__ == '__main__':
    all_file = get_downloads()
    if not(meme_version()):
        if(update_client(all_file)):
            import main
            main.login_page()
        else:
            print('Impossible de mettre à jour le client, merci de faire la mise à jour !')
    else:
        import main
        main.login_page()