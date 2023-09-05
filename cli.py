# Interfaz de línea de comandos en desarrollo
from pick import pick

title = "Escoger tipo de circuito: "
options = ["Delta-Delta", "Estrella-Estrella", "Delta-Estrella", "Estrella-Delta", "Estrella-Estrella 3 Hilos"]

option, index = pick(options, title)

print(option)
print(index)
