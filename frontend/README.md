# Sistema de Agentes IA - Frontend

## Descripción

Frontend React moderno para el sistema de agentes IA con interfaz de usuario intuitiva, soporte para chat en tiempo real, análisis de datos y sistema de notificaciones.

## Características

- **React 18** - Framework moderno con hooks
- **Vite** - Build tool rápido y eficiente
- **Material-UI** - Componentes de UI profesionales
- **WebSockets** - Comunicación en tiempo real
- **Multilenguaje** - Soporte para español e inglés
- **Temas dinámicos** - Modo claro y oscuro
- **Responsive Design** - Optimizado para móviles y desktop
- **React Router** - Navegación entre páginas
- **React Query** - Gestión de estado del servidor
- **React Hook Form** - Formularios optimizados

## Instalación

1. **Clonar el repositorio:**
```bash
git clone <repository-url>
cd agent_ia/frontend
```

2. **Instalar dependencias:**
```bash
npm install
```

3. **Configurar variables de entorno:**
```bash
cp .env.example .env
# Editar .env con la URL del backend
```

4. **Ejecutar en modo desarrollo:**
```bash
npm run dev
```

## Estructura del Proyecto

```
frontend/
├── src/
│   ├── components/           # Componentes React
│   │   ├── NavBar.jsx        # Barra de navegación
│   │   ├── LoginForm.jsx     # Formulario de login
│   │   ├── Chat.jsx          # Chat básico
│   │   ├── ChatWS.jsx        # Chat con WebSocket
│   │   ├── DataAnalysisWS.jsx # Análisis de datos
│   │   ├── NotificationsWS.jsx # Notificaciones
│   │   ├── ProtectedRoute.jsx # Ruta protegida
│   │   └── *.css             # Estilos de componentes
│   ├── api/                  # Cliente API
│   │   ├── auth.js           # Autenticación
│   │   ├── client.js         # Cliente HTTP
│   │   └── useWebSocket.js   # Hook WebSocket
│   ├── i18n.js               # Traducciones
│   ├── App.jsx               # Componente principal
│   └── main.jsx              # Punto de entrada
├── package.json              # Dependencias
├── vite.config.js            # Configuración de Vite
└── README.md                 # Este archivo
```

## Componentes Principales

### NavBar
Barra de navegación con selectores de idioma y tema dinámico.

### LoginForm
Formulario de autenticación con validación y estilos optimizados.

### Chat
Interfaz de chat básico con envío de mensajes y respuestas.

### ChatWS
Chat en tiempo real con WebSockets, indicadores de estado y mensajes en vivo.

### DataAnalysisWS
Interfaz para análisis de datos con consultas y resultados en tiempo real.

### NotificationsWS
Sistema de notificaciones en tiempo real con animaciones.

## Configuración

### Variables de Entorno

Crear archivo `.env` en la raíz del frontend:

```env
# URL del backend
VITE_API_URL=http://localhost:8000
VITE_WS_URL=ws://localhost:8000

# Configuración de la aplicación
VITE_APP_NAME=Sistema de Agentes IA
VITE_APP_VERSION=1.0.0

# Configuración de desarrollo
VITE_DEBUG=true
```

### Temas

El sistema soporta dos temas:

- **Claro**: Colores claros con mejor legibilidad
- **Oscuro**: Colores oscuros para reducir fatiga visual

Los temas se aplican automáticamente a todos los componentes y se guardan en localStorage.

### Idiomas

Soporte para:
- **Español** (por defecto)
- **English**

El idioma se detecta automáticamente del navegador y se puede cambiar manualmente.

## Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Ejecutar servidor de desarrollo
npm run build        # Construir para producción
npm run preview      # Previsualizar build de producción

# Linting
npm run lint         # Verificar código
npm run lint:fix     # Corregir problemas automáticamente
```

## Desarrollo

### Ejecutar en modo desarrollo
```bash
npm run dev
```

La aplicación estará disponible en `http://localhost:5173`

### Construir para producción
```bash
npm run build
```

Los archivos optimizados se generarán en la carpeta `dist/`

### Previsualizar build
```bash
npm run preview
```

## Estructura de Estilos

### CSS Variables
El sistema usa variables CSS para temas:

```css
:root {
  /* Tema claro */
  --light-bg: #ffffff;
  --light-surface: #f8f9fa;
  --light-primary: #007bff;
  --light-text: #212529;
  
  /* Tema oscuro */
  --dark-bg: #1a1a1a;
  --dark-surface: #2d2d2d;
  --dark-primary: #4dabf7;
  --dark-text: #f8f9fa;
}
```

### Responsive Design
Todos los componentes son responsivos y se adaptan a:
- **Desktop**: > 768px
- **Tablet**: 768px - 480px
- **Mobile**: < 480px

## API Integration

### Cliente HTTP
```javascript
import api from './api/client';

// Ejemplo de uso
const response = await api.post('/chat/message', { message: 'Hola' });
```

### WebSockets
```javascript
import { useWebSocket } from './api/useWebSocket';

// Ejemplo de uso
const { messages, sendMessage, status } = useWebSocket('ws://localhost:8000/ws/chat', token);
```

## Internacionalización

### Agregar nuevas traducciones
Editar `src/i18n.js`:

```javascript
const translations = {
  es: {
    newKey: "Nueva traducción en español"
  },
  en: {
    newKey: "New translation in English"
  }
};
```

### Usar traducciones
```javascript
import { t } from '../i18n';

// En componentes
const message = t('newKey', language);
```

## Optimizaciones

### Performance
- **Code Splitting** automático con Vite
- **Lazy Loading** de componentes
- **Memoización** de componentes pesados
- **Optimización** de imágenes

### SEO
- **Meta tags** dinámicos
- **Títulos** de página
- **Descripciones** optimizadas

### Accesibilidad
- **ARIA labels** en componentes
- **Navegación** por teclado
- **Contraste** de colores optimizado
- **Screen readers** compatibles

## Troubleshooting

### Problemas comunes

1. **Error de conexión al backend**
   - Verificar que el backend esté ejecutándose
   - Comprobar URL en `.env`
   - Verificar CORS en el backend

2. **WebSockets no conectan**
   - Verificar URL del WebSocket
   - Comprobar token de autenticación
   - Verificar configuración del backend

3. **Estilos no se aplican**
   - Verificar importación de CSS
   - Comprobar variables CSS
   - Limpiar caché del navegador

## Contribución

1. Fork el proyecto
2. Crear una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abrir un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles. 