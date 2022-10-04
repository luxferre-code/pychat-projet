import os, cutie

if(cutie.prompt_yes_or_no('Voulez-vous créer un fichier "downloads.lxf" pour le dossier client ?')):
    
    ver = cutie.secure_input('Merci d\'entrer la version de PyChat Client | ')
    
    os.chdir('client')
    all_files = os.listdir()
    for rang in range(len(all_files)):
        if('.' not in all_files[rang]):
            # Est un dossier
            os.chdir(all_files[rang])
            dico = {'./server_pychat/client/' + all_files[rang] + '/': os.listdir()}
            os.chdir('..')
            all_files[rang] = dico
    
    string = ver + '\n'
    for elt in all_files:
        if(isinstance(elt, str)):
            string += './server_pychat/client/' + elt + '\n'
        else:
            for keys, values in elt.items():
                for sous_elt in values:
                    string += keys + sous_elt + '\n'
        
    os.chdir('..')
    if('downloads.lxf' in os.listdir()): os.remove('downloads.lxf')
    with open('downloads.lxf', 'a', encoding='UTF-8') as file:
        file.write(string)