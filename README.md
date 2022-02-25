# App-videoconferencia

Esta herramienta se diseñó mediante scripts de Linux para cumplir con las distintas funcionalidades y los experimentos se efectuaron en ordenadores con sistema operativo Ubuntu 20.04. Para efectuar los diferentes cálculos también se implementaron scripts en Python 3.7. 

Esta es una herramienta para transmitir y reproducir audio y video utilizando GStreamer. Para la transmisión de audio y video en tiempo real con una interfaz gráfica, la misma que reúne las características de reuniones individuales y la capacidad de video adaptativo. La herramienta funciona
en conjunto con un servidor disponible en https://github.com/christianquinde/server

En la siguiente Figura se presenta un diagrama secuencial del funcionamiento de la herramienta para la transmisión
de audio y video en tiempo real. 
![app_func](https://user-images.githubusercontent.com/68077496/155751207-8791a812-5f26-4c02-8958-02666c7f2c68.png)

La interfaz gráfica diseñada se presenta en la siguiente Figura. 

# Funcionamiento

Esta herramienta requiere de un nombre y un apellido.

## 1: Ingresar
Se da clic en el botón "Ingresar" con el cual se envían los datos ingresados y también la dirección
IP a un servidor local.

![screen1](https://user-images.githubusercontent.com/68077496/155751426-9fd21cac-83a9-48e9-879d-db9b070e9ad9.png)

## 2: Listo para realizar 
Se despliega una nueva interfaz, la cual se observa en la siguiente Figura, donde se presentan todos los usuarios que están registrados en el servidor.
La aplicación está a la escucha de un iperf para poder establecer una llamada, al momento que un usuario llama a un contacto este se convierte
en un cliente iperf enviando paquetes UDP a un puerto específico (8001). 

![screen2](https://user-images.githubusercontent.com/68077496/155751469-ab60a85e-a053-48b6-a6ee-dd7d5f48cc7f.png)

## 3: Listo para recibir una llamada
El usuario que recibe la llamada funciona como servidor iperf. De esta manera al detectar mensajes UDP entrantes en el
puerto específico se despliega una nueva interfaz, mostrada en la siguiente figura, para aceptar o declinar la llamada.

![screen3](https://user-images.githubusercontent.com/68077496/155751632-44b95351-bf0a-437a-858f-f3e37f1635bd.png)

En este contexto el usuario que recibe la llamada escucha un tono de llamada entrante. Además, con los
resultados obtenidos del iperf se mide el ancho de banda de la red y así dependiendo de los umbrales del
throughput obtenidos se codifica con diferentes valores de bitrate. De esta manera se consigue una opción de
vídeo adaptativo, el cual es transparente al usuario.

## 4: Colgar
Al finalizar la llamada con el botón "Colgar", los dos usuarios
regresan a la interfaz principal y se ponen a la escucha de un iperf nuevamente.
