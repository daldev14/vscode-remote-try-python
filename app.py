#-----------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See LICENSE in the project root for license information.
#-----------------------------------------------------------------------------------------


import random
import curses
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return app.send_static_file("index.html")

# Define las opciones del juego
opciones = ["piedra", "papel", "tijeras"]
seleccion = 0
puntuacion_jugador = 0

def main(stdscr):
    global seleccion, puntuacion_jugador
    curses.curs_set(0)  # Oculta el cursor
    stdscr.clear()
    
    
    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Elige una opción:")
        
        for i, opcion in enumerate(opciones):
            if i == seleccion:
                 # Cambia el color del texto seleccionado a azul
                stdscr.addstr(i + 1, 0, f"> {opcion}", curses.A_BOLD | curses.color_pair(1))
            else:
                stdscr.addstr(i + 1, 0, f"  {opcion}")

        stdscr.refresh()
        key = stdscr.getch()
        
        if key == curses.KEY_DOWN:
            seleccion = (seleccion + 1) % len(opciones)
        elif key == curses.KEY_UP:
            seleccion = (seleccion - 1) % len(opciones)
        elif key == 10:  # Tecla Enter
            eleccion_jugador = opciones[seleccion]
            eleccion_maquina = random.choice(opciones)
            resultado = determinar_resultado(eleccion_jugador, eleccion_maquina)
            
            stdscr.addstr(len(opciones) + 2, 0, f"Tú elegiste: {eleccion_jugador}")
            stdscr.addstr(len(opciones) + 3, 0, f"La máquina eligió: {eleccion_maquina}")
            stdscr.addstr(len(opciones) + 5, 0, resultado)
            
            if resultado == "¡Ganaste!":
                puntuacion_jugador += 1
                
            stdscr.addstr(len(opciones) + 6, 0, f"Puntuación: {puntuacion_jugador}")
            stdscr.addstr(len(opciones) + 8, 0, "Presiona Enter para jugar de nuevo o Q para salir.")
            stdscr.refresh()
            
            while True:
                key = stdscr.getch()
                if key == 10:
                    break
                elif key == ord('q') or key == ord('Q'):
                    return
        
        if key == ord('q') or key == ord('Q'):
            break

def determinar_resultado(eleccion_jugador, eleccion_maquina):
    if eleccion_jugador == eleccion_maquina:
        return "Es un empate."
    elif (eleccion_jugador == "piedra" and eleccion_maquina == "tijeras") or \
         (eleccion_jugador == "papel" and eleccion_maquina == "piedra") or \
         (eleccion_jugador == "tijeras" and eleccion_maquina == "papel"):
        return "¡Ganaste!"
    else:
        return "La máquina gana."

if __name__ == "__main__":
    curses.wrapper(main)
