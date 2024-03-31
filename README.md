# SD-Flask
    Este proyecto fue desarrollado como parte del curso de "Sistemas Distribuidos"
    con el propósito de explorar   el funcionamiento de este tipo de sistemas.

    El proyecto consiste en un sistema de mensajería en tiempo real, implementado 
    utilizando tecnologías como Python y el framework Flask para la creación del 
    servidor. La comunicación en tiempo real se logra mediante el uso de SocketIO, 
    lo que permite una interacción fluida entre el cliente y el servidor, así como 
    la creación de salas que facilitan la conversación privada entre los usuarios.

Los datos generados por el sistema se almacenan en una base de datos no relacional, 
en este caso, MongoDB. Esta elección se realizó para garantizar que el sistema pueda 
manejar grandes volúmenes de datos de manera eficiente.

## Autor:
    Jorge Antonio Gálvez Pino

## TEcnologias Utilizadas
    
    Lenguaje de Programación: Python 3.11.4
    Framework: Flask
    Comunicación en Tiempo Real: SocketIO
    Base de Datos: MongoDB 7.0.6

## Requisitos

    Para la instalacion de las librerias mecesaria para ejecutaer el programa
    debe ejecutar el siguiente comando
    ´´´bash
        "pip install -r .\requirements.txt"