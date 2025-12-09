import os
import sys
from packages.GameManager import GameManager


def game_invoker():
    mgr = GameManager()
    mgr.menu(True)


def main():
    if os.name == "posix":
        if os.getuid() != 0:
            print("AVISO:")
            print("O Linux restringe a obtenção de estado de teclas para evitar que programas maliciosos obtenham dados sensíveis")
            print("Por conta disso, o programa precisa ser executado com permissões elevadas, a seguir será requisitado a senha do sistema")

            args = ["sudo", sys.executable] + sys.argv
            os.execvp("sudo", args)

        game_invoker()

    if os.name == "nt":
        game_invoker()


if __name__ == "__main__":
    main()
