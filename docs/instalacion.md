# Instalación

> **En pocas palabras:** hacen falta tres cosas en tu ordenador: **Python** (el lenguaje en
> que están escritos los programas), **Claude Code** y una copia de este repositorio. Después
> se instala un único paquete adicional (`pypdf`, para leer PDF) y se comprueba que todo
> funciona con las pruebas automáticas. Son unos 15 minutos la primera vez.

Si alguna palabra no te suena, consulta el [glosario](glosario.md).

## 1. Instalar Python

1. Comprueba si ya lo tienes: abre la **terminal** y escribe `python3 --version` (en Windows,
   `python --version`). Si aparece `Python 3.10` o un número mayor, pasa al punto 2.
2. Si no, descárgalo de https://www.python.org/downloads/ e instálalo.
   **En Windows**, marca la casilla *"Add Python to PATH"* al instalar.

Dónde está la terminal:
- **macOS:** aplicación *Terminal* (búscala con Cmd + espacio).
- **Windows:** *PowerShell* (búscalo en el menú Inicio).
- **Linux:** *Terminal*.

## 2. Instalar Claude Code

Sigue las instrucciones oficiales: https://code.claude.com/docs (sección de instalación).
Necesitas una cuenta de Claude con suscripción Pro o Max (decisión 0005).

## 3. Descargar este repositorio

En la terminal, ve a la carpeta donde quieras guardarlo y escribe:

```
git clone https://github.com/britoruben/LoRu-Agent.git
cd LoRu-Agent
```

Si no tienes `git`, en la página del repositorio en GitHub pulsa **Code → Download ZIP**,
descomprímelo y abre la terminal en esa carpeta.

## 4. Crear un entorno propio e instalar pypdf

Un **entorno virtual** es una caja donde se instalan los paquetes de este proyecto sin mezclarlos
con el resto del ordenador. Se crea una sola vez:

**macOS y Linux**
```
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

**Windows (PowerShell)**
```
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

Sabrás que el entorno está activo porque la terminal muestra `(.venv)` al principio de la línea.
**Cada vez que abras una terminal nueva** para trabajar con LoRu-Agent, repite solo la segunda
línea (la de `activate`).

## 5. Comprobar que todo funciona

Con el entorno activo:

```
python -m unittest
```

Debe terminar con `OK`. Si algo falla, copia el mensaje y consúltalo.

## 6. Abrir el asistente

Con el entorno activo, escribe `claude`. La primera vez te preguntará si confías en esta carpeta:
responde que sí. Después, prueba el ejemplo de [ejemplos/LEEME.md](../ejemplos/LEEME.md).

## Problemas frecuentes

| Mensaje | Qué pasa | Qué hacer |
|---|---|---|
| `python3: command not found` o `python no se reconoce` | Python no está instalado o no se encuentra | Repite el punto 1; en Windows, marca *"Add Python to PATH"* |
| `Falta el paquete pypdf` | No se ha instalado pypdf o el entorno no está activo | Activa el entorno (punto 4, segunda línea) e instala de nuevo |
| En Windows: `la ejecución de scripts está deshabilitada` | PowerShell bloquea la activación | Escribe `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y responde que sí |
| `externally-managed-environment` | El sistema no deja instalar paquetes fuera de un entorno | Usa el entorno virtual del punto 4 |
