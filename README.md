# Proyecto de Ecommerce en Django
Primeramente estoy trabajando con la version  de python 3.9.6 lo descargo es el de x86-64 executable installer
Uno ves instalado entramos al cmd
Luego estamos trabajando con django==3.2.6
Creamos la carpeta "django" en nuestros Documentos
Luego en el cmd -> ingresamos cd Documents, luego -> cd django
Estando ahi dentro de la carpeta crearemos el entorno llamado "calendario" :
py -m venv calendario
Asi podemos confiar, entrando a la carpeta y que este creada la carpeta calendario
Entonces ingresaremos al cd calendario-> cd Scripts -> activate
Una vez activato, te tiene que salir adelante de la ruta -> (calendario)
Ya estando alli, tenemos que instalar django -> con el comando "pip install Django==3.2.6"
En ese momento se estara ejecutando y descargando
Luego el comando -> "pip freeze" donde te aparece que esta instalado django y unas aplicacione mas
Ahi creados nuestro proyecto: con el comando " django-admin startproject Django_Ecommerce"
Para comprobar que esta bien, entonces ingresamos al cd Django_Ecommerce
Y ejecutamos python manage.py runserver y te deje dirigir al servidor.

Por ultimo en nuestro vs code, abrimos nuestro proyecto de Django_Ecommerce.
Para ejecutar nueustro servidor en vs code en la parte del terminal en la parte superior derecho, donde se encuentra
powershell existe un mas le das click y seleccionas el command prompt, ahi tenemos que:
retroceder hasta django -> con cd.. 
Una vez estando en la carpeta de django ingresamos: cd calendario -> cd Scripts -> activate django
se mostrará en adelante (calendario)
Luego de eso tenemos que retroceder hasta django y ahi ejecutamos -> cd Django_Ecommerce -> cd src
Estando en esa dirección vamos a ejecutar el sgt comando : python manage.py runserver (para el servidor)


Para crear un super usuario : es " python manage.py createsuperuser" le damos click y te pide que escribas usuario, email y password.
Una vez hecho eso, ejecutamos el servidor y en el url le agregamos: /admin
Te redirige al panel donde podras agregar productos, tamaño, etc.
Para salir del servidor es control + c

Para crear migraciones: primero se tiene que eliminar las migraciones de todas las carpetas y la base de datos (db.sqlite3)
Luego se utiliza el comando : python manage.py makemigratons cart (tiene q aparecer todo lo q esta en la carpeta cart)
python manage.py migrate (ejecuta el proyecto completo).
