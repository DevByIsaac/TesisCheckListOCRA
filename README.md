# ERGO-TECH

**ERGO-TECH** es una aplicación web diseñada para facilitar el análisis ergonómico en el entorno laboral. Utiliza tecnologías modernas para ofrecer herramientas interactivas y eficientes para evaluar posturas y movimientos. El proyecto permite a los usuarios registrarse, iniciar sesión y acceder a diversas herramientas y métodos de evaluación.

## Características

- **Registro de Usuarios**: Permite a los usuarios crear una cuenta y almacenar sus datos de manera segura.
- **Inicio de Sesión**: Los usuarios pueden iniciar sesión en la aplicación para acceder a sus datos y herramientas personalizadas.
- **Métodos de Evaluación**: Incluye herramientas para evaluar el riesgo ergonómico utilizando métodos como OCRA.
- **Interfaz de Usuario**: Proporciona una interfaz intuitiva con navegación moderna y responsive utilizando Bootstrap.

## Tecnologías Utilizadas

- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **Backend**: Python, Flask
- **Base de Datos**: PostgreSQL
- **Otros**: jQuery, Popper.js

## Instalación

1. **Clona el Repositorio**

   ```bash
   git clone https://github.com/DevByIsaac/TesisCheckListOCRA.git

2. **Instala las Dependencias**
Crea un entorno virtual y activa:

python -m venv venv
source venv/bin/activate  # Para Unix/macOS
venv\Scripts\activate     # Para Windows

Instala las dependencias:
pip install -r requirements.txt

3. **Configura la Base de Datos**
Crea una base de datos en PostgreSQL y actualiza la configuración en el archivo config_postgres.py con los detalles de tu base de datos.

4. **Ejecuta la Aplicación**
Inicia la aplicación con:
flask run
La aplicación estará disponible en http://127.0.0.1:5000/.

Uso
Registro de Usuario: Accede a /registro para crear una nueva cuenta.
Inicio de Sesión: Accede a /login para iniciar sesión con tus credenciales.
Métodos de Evaluación: Explora las herramientas de evaluación disponibles desde la barra de navegación.
Contribuciones
Si deseas contribuir al proyecto, por favor sigue estos pasos:

Fork el Repositorio
Crea una Rama para tu Feature: git checkout -b feature/nueva-funcionalidad
Realiza tus Cambios y Commits
Push a tu Rama: git push origin feature/nueva-funcionalidad
Crea un Pull Request
Licencia
Este proyecto está licenciado bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.

Contacto
Para más información o consultas, puedes contactar al autor a través de isaac_gomez_elmaster@live.com

