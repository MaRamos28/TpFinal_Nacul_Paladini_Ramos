from menu import mostrar_menu
from juego import juego
if __name__ == "__main__":
    while True:
        mostrar_menu()
        resultado = juego()

        if resultado == "volver a jugar":
            resultado = juego()
        if resultado == "menu":
            continue
        else:
            breakz