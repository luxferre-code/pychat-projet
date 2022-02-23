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


if __name__ == "__main__":
  to_install = ["sqlite3"]
