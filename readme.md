## Instalación

Para instalar el proyecto debe clonar el repositorio, crear un entorno virtual de Python e instalar las librerías ejecutando los siguientes comandos en la ruta que desee instalar el proyecto:

```bash
#Windows
git clone https://github.com/Julianms11/circuit-tools
python -m venv nombre-entorno
pip install -r requirements.txt
```

## Uso

Active el entorno virtual:

```bash
#Windows
nombre-entorno/Scripts/activate.bat
```

```python
#Ejemplo de uso circuito Estrella-Delta
# Vfuente = 120, angulo = 0,
fuentes = FuentesY(120, 0)
# Carga desbalanceada, para carga balanceada -> imps = Impedancias(10+10j).Z
imps = Impredancias([3+6j, 81-2j, 9+1j]).Z
cirucito = EstrellaDelta(fuentes, imps)
print(circuito) #Imprime tensiones de fase y línea, corrientes de fase
                #y línea, corrimiento de neutro, potencia por fase y compleja.
```
