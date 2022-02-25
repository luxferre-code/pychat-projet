# Main file on Server
import pip


def installer(to_install: str) -> None:
    """
    Fonction permettant d'installer des modules
  
    param:
    to_install: string
  
    Return type: None
    # Valentin Thuillier
    """
    pip.main(["install", to_install])
    
def updater():
    """
    Fonction permettant de récupérer les données du projet et de mettre à jour le serveur
    
    param:
    None
    
    Return type: None
    # Valentin Thuillier
    """
    pass


if __name__ == "__main__":
    pip.main(["install", "--upgrade", "pip"])
    to_install = ["sqlite3", "os"]
    for elt in to_install:
        installer(elt)
