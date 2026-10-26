<div align="center">

# ✈️ Ace Combat 2 Recompiled
### *Port Nativo para PC (Windows x64) mediante Recompilación Estática MIPS R3000A*

[![Platform](https://img.shields.io/badge/Plataforma-Windows%20x64%20Nativo-blue.svg?style=for-the-badge&logo=windows)](https://github.com)
[![Resolution](https://img.shields.io/badge/Resoluci%C3%B3n-4K%20UHD%20(3840x2160)-brightgreen.svg?style=for-the-badge)](https://github.com)
[![Framerate](https://img.shields.io/badge/Refresco-60%20%2F%20120%20%2F%20144%20FPS-orange.svg?style=for-the-badge)](https://github.com)
[![Aspect Ratio](https://img.shields.io/badge/Modos-16%3A9%20Full--Screen%20%26%204%3A3%20UHD-purple.svg?style=for-the-badge)](https://github.com)
[![Geometry](https://img.shields.io/badge/Geometr%C3%ADa-Rock--Solid%20(Sin%20Glitches)-success.svg?style=for-the-badge)](https://github.com)
[![License](https://img.shields.io/badge/Licencia-MIT-lightgrey.svg?style=for-the-badge)](LICENSE)

---

</div>

## 📖 Descripción del Proyecto

**Ace Combat 2 Recompiled** es una adaptación nativa para PC de 64 bits del legendario juego de combate aéreo lanzado por **Namco** en 1997 para la Sony PlayStation 1.

A diferencia de los emuladores convencionales (que interpretan el código máquina MIPS en un bucle virtual con sobrecoste de CPU y latencia de entrada), este proyecto realiza una **traducción estática completa** del código binario de PS1 a código C nativo optimizado para procesadores x86-64 modernos.

El ejecutable resultante interactúa directamente con la GPU a través de OpenGL/Vulkan de bajo nivel, ofreciendo una experiencia fluida, nítida y con latencia ultrabaja imposible de alcanzar en el hardware original de 32 bits.

---

## ✨ Características y Mejoras Implementadas

### 🎯 1. Fijación de Blancos y Minimapa Milimétricos
- **Sincronización 1:1 en 3D:** Los recuadros verdes y rojos de fijación de misiles (`Target Lock-On`) se mantienen **exactamente centrados sobre los cazas enemigos** en todo momento, eliminando el desplazamiento artificial que sufrían los hacks convencionales de pantalla ancha.
- **Minimapa Integrado:** La brújula, el círculo de radar y los puntos de aeronaves permanecen cohesionados y alineados dentro de la interfaz sin separarse ni sufrir desajustes.

### 🌊 2. Geometría de Terreno y Océano Libre de Glitches
- **Estabilización de Cuadrícula:** Corrección matemática en la proyección de vértices del mar y las cadenas montañosas. Se eliminan las grietas, polígonos parpadeantes y "explosiones" de malla habituales de PGXP en simuladores de vuelo.
- **Superficie de Agua Fluida y Homogénea:** El océano se renderiza con textura continua y sólida sin desgarros entre tiles adyacentes.

### 🖥️ 3. Modos de Visualización Adaptativos

| Modo | Lanzador | Descripción |
|---|---|---|
| **16:9 Panorámico Pantalla Completa** | `AceCombat2.exe`<br>`JUGAR_ACE_COMBAT_2.bat` | Llena el **100% de la pantalla** sin bandas negras laterales. Los vídeos cinemáticos (FMV MDEC) conservan automáticamente la proporción original 4:3 para no deformarse. |
| **4:3 UHD Puro Pixel-Perfect** | `JUGAR_ACE_COMBAT_2_4K_43.bat` | Proporción clásica 4:3 en resolución nativa **4K UHD (2160p)**. Cero pop-in en bordes laterales y radar circular perfecto. |

### 🎨 4. Shader Post-Procesado OLED Crystal-Clear
- **Contraste y Profundidad:** Canal de color optimizado para pantallas modernas y paneles OLED.
- **Azules Profundos y Fuego Vivo:** Mayor saturación selectiva en el cielo y el mar, con estelas de condensación, humo y explosiones nítidas sin artefactos de realce de bordes 2D.

### 🔇 5. Lanzador Nativo Silencioso (`.exe`)
- `AceCombat2.exe` compilado con Clang en modo `-mwindows`, arrancando de manera inmediata sin consolas de texto CMD de fondo.
- Se incluye también un script silencioso adicional `JUGAR_ACE_COMBAT_2_SIN_VENTANAS.vbs`.

---

## 🎮 Compatibilidad Universal de Discos

El preparador universal integrado (`tools/setup_disc.py`) detecta y configura automáticamente las siguientes regiones:

| Región | Código de Disco | Título | Frecuencia | Idioma |
|---|---|---|---|---|
| **PAL Europa** | `SCES-00699` | Ace Combat 2 | 50.0 Hz | Inglés |
| **PAL España** | `SCES-00710` | Ace Combat 2 | 50.0 Hz | Castellano / Multilenguaje |
| **NTSC-U** | `SLUS-00404` | Ace Combat 2 | 59.94 Hz | Inglés |
| **NTSC-J** | `SLPS-00830` | Ace Combat 2 (v1.0) | 59.94 Hz | Japonés |
| **NTSC-J The Best** | `SLPS-91060` | Ace Combat 2 (PlayStation The Best) | 59.94 Hz | Japonés |
| **NTSC-J NamCollection** | `SLPM-80512` | Ace Combat 2 (NamCollection) | 59.94 Hz | Japonés |

Formatos aceptados: **`.BIN/.CUE`**, **`.PBP`** (PSP/PS3 eBoot), **`.ISO`**, **`.IMG`**, **`.CHD`**.

---

## 🚀 Guía de Instalación y Uso Rápido

1. **Descarga el release:**
   Descarga y descomprime `Ace_Combat_2_Recompiled_v1.0_Windows_x64.zip`.

2. **Añade tu juego legal:**
   Copia tu imagen de disco de Ace Combat 2 en la subcarpeta `disc/` (o en la carpeta raíz del juego).

3. **Ejecuta el preparador:**
   Haz doble clic en **`PREPARAR_DISCO.bat`**. Detectará tu copia, extraerá los archivos necesarios si es un `.PBP` y configurará el motor automáticamente.

4. **¡A volar!:**
   - Para jugar en **16:9 Panorámico Completo**: ejecuta `AceCombat2.exe` o `JUGAR_ACE_COMBAT_2.bat`.
   - Para jugar en **4:3 UHD Puro Clásico**: ejecuta `JUGAR_ACE_COMBAT_2_4K_43.bat`.

---

## 🕹️ Controles por Defecto

Compatible de forma nativa con **Mandos de Xbox Series/One/360, PlayStation DualSense/DualShock 4, Mandos Genéricos DirectInput/XInput y Teclado**.

| Acción en Vuelo | Mando (Xbox / PS) | Teclado (Alternativo) |
|---|---|---|
| **Alabeo y Cabeceo (Guiar Avión)** | Stick Izquierdo / Cruceta | `Flechas de Dirección` |
| **Acelerar (Postquemador)** | `R1` / `RB` | `Z` |
| **Frenar / Aerofrenos** | `L1` / `LB` | `X` |
| **Timón de Cola (Guiñada Izq / Der)** | `L2` / `R2` (`LT` / `RT`) | `A` / `S` |
| **Disparar Cañón** | `Cuadrado` / `X` | `Espacio` |
| **Lanzar Misil** | `Cruz` / `A` | `Enter` |
| **Cambiar Blanco (`Target`)** | `Círculo` / `B` | `Tab` |
| **Cambiar Cámara (Cabina / Exterior)** | `Triángulo` / `Y` | `C` |
| **Pausa / Menú de Misión** | `Start` | `Escape` |

---

## 📂 Estructura del Paquete

```text
Ace_Combat_2_Recompiled/
├── AceCombat2.exe                     # Lanzador nativo Windows silencioso
├── Ace_Combat_2_Recompiled.exe         # Ejecutable principal del motor recompilado
├── game.toml                           # Configuración de renderizado 4K, PGXP y aspecto
├── settings.toml                       # Preferencias de usuario portables
├── disc.cfg                            # Ruta al descriptor del disco
├── JUGAR_ACE_COMBAT_2.bat              # Acceso rápido en 16:9 Full-Screen
├── JUGAR_ACE_COMBAT_2_4K_43.bat        # Acceso rápido en 4:3 UHD Puro
├── JUGAR_ACE_COMBAT_2_SIN_VENTANAS.vbs # Acceso 100% silencioso
├── PREPARAR_DISCO.bat                  # Asistente de detección de disco
├── LEEME_INSTRUCCIONES.txt             # Guía rápida en texto plano
├── README.md                           # Documentación completa
├── LICENSE                             # Licencia MIT del proyecto
├── disc/                               # Carpeta donde depositar el juego legal
│   └── PON_TU_JUEGO_AQUI.txt
├── saves/                              # Tarjetas de memoria virtuales (.mcd)
├── shaders/                            # Shaders HD Crystal-Clear OLED
│   ├── hd2d.glsl
│   └── hd2d.pfx
└── tools/                              # Utilidad multiplataforma de ingestión
    └── setup_disc.py
```

---

## 💻 Requisitos del Sistema

- **Sistema Operativo:** Windows 10 / Windows 11 (64-bit).
- **Procesador:** Cualquier CPU moderna con soporte x86-64 (Intel Core i3 / AMD Ryzen 3 o superior).
- **Memoria RAM:** 2 GB mínimo.
- **Tarjeta Gráfica:** Compatible con OpenGL 3.3 o superior (Intel HD Graphics 4000+, NVIDIA GeForce GT 710+, AMD Radeon HD 7000+ o cualquier GPU dedicada moderna).
- **Almacenamiento:** ~650 MB para la imagen de disco del juego.

---

## ⚖️ Aviso Legal y Cumplimiento

* **Ace Combat 2** es una marca registrada de **Bandai Namco Entertainment Inc.**
* Este proyecto es una reimplementación independiente de código limpio desarrollada con fines de preservación técnica e investigación histórica.
* **Este paquete NO contiene ninguna BIOS de Sony PlayStation, ni imágenes de disco, música, vídeos ni ningún archivo con derechos de autor.**
* Cada usuario debe poseer una copia original del juego para generar los activos necesarios para jugar.
