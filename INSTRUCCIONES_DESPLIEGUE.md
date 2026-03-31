# Instrucciones para el Despliegue Seguro (GitHub y Vercel)

Para evitar la fuga de credenciales o llaves de tu base de datos (Supabase), se ha añadido un archivo `.gitignore` que impide que archivos sensibles como el `.env` sean subidos a tu repositorio.

## 1. Subir tu proyecto a GitHub
1. Si no lo has hecho, inicializa Git en tu proyecto o simplemente usa tu gestor gráfico (GitHub Desktop / VS Code).
2. Agrega los cambios:
   ```bash
   git add .
   ```
3. Crea un "commit":
   ```bash
   git commit -m "Modernización de la API"
   ```
4. Sube los cambios a tu repositorio:
   ```bash
   git push origin main
   ```
*(Nota: Si GitHub Desktop te pregunta si quieres subir archivos `.env`, **recházalo o ignóralo**. El archivo `.gitignore` ya se encargará de esto si usas la consola).*

## 2. Configuración en Vercel
Dado que el archivo `.env` ya no se sube a internet (lo cual es excelente por seguridad), Vercel no sabe cuáles son tus llaves. 

Para proporcionárselas de manera segura:
1. Entra a tu proyecto en el panel de control (Dashboard) de [Vercel](https://vercel.com).
2. Ve a la pestaña de **Settings** de tu proyecto.
3. En el menú izquierdo, haz clic en **Environment Variables**.
4. Ahora, vas a añadir las siguientes variables (exactamente como están en tu archivo `.env` local):
   * **Key**: `SUPABASE_URL` | **Value**: *(La URL de tu base de datos y le das a Save)*
   * **Key**: `SUPABASE_KEY` | **Value**: *(La llave anónima o service_role de tu base de datos y le das a Save)*
   * **Key**: `MASTER_KEY` | **Value**: *(Crea una contraseña segura para tu propia API, por ej: `MiClaveSecreta123`)*

## 3. Desplegar
Una vez guardadas esas 3 propiedades, ve a la pestaña de **Deployments** en Vercel y haz clic en los 3 puntitos del último despliegue -> **Redeploy**.

¡Y listo! Tu API estará en la mejor versión, hermosa y completamente segura de miradas indiscretas. 

---

### Notas de las mejoras realizadas:
- **Root Automático**: Cuando entres a tu dominio de Vercel (por ejemplo `eco.vercel.app/`), la pantalla cargará directo tus Documentos de la API. ¡Ya no más error 404!
- **Protección**: La API usa `x-api-key`. Cuando quieras subir datos, la interfaz requerirá que pongas la contraseña (`MASTER_KEY`) que configuraste en Vercel.
