---
title: "Copias de seguridad VPS"
slug: "copias-de-seguridad-vps"
description: "Copias de seguridad VPS: define RPO y RTO, combina imágenes del proveedor con copias externas independientes, protege bases de datos, configura la retención y comprueba las restauraciones."
image: "images/home/vps-for-website-hero.webp"
---

Una estrategia de copias de seguridad VPS no consiste en «activar una instantánea diaria». Un plan de recuperación útil define **cuántos datos se pueden perder (RPO), cuánto puede durar la recuperación (RTO), qué datos deben conservarse, dónde están las copias independientes, durante cuánto tiempo se guardan las versiones y si alguien ha probado a restaurarlas**.

Normalmente conviene combinar la recuperación rápida que proporciona el proveedor con copias independientes fuera del servidor y respaldos coherentes de la base de datos. La combinación depende de la velocidad a la que cambian los datos y del coste de una interrupción.

Debe haber una persona responsable. Si nadie atiende los trabajos fallidos, las pruebas de restauración y las decisiones de recuperación, hay que resolver primero esa responsabilidad: consulta [VPS administrado o no administrado](/es/vps-administrado-vs-no-administrado/).

Para la elección general de servidor, consulta [VPS para alojar sitios web](/es/).

[Resumen](#quick-answer) · [Comprobador](#vps-backup-strategy-checker) · [RPO y RTO](#start-with-rpo-and-rto) · [Tipos de copias](#snapshot-image-file-backup-and-replication-are-different) · [Regla 3-2-1](#a-practical-3-2-1-model-for-vps) · [Pruebas](#test-restores-and-measure-real-rto) · [VDSina](#how-vdsina-backups-fit-the-strategy) · [Preguntas frecuentes](#faq)

<a id="quick-answer"></a>
## Resumen

Un esquema práctico de recuperación de un VPS necesita varias capas:

| Capa | Función principal | Lo que no garantiza |
|---|---|---|
| **Imagen o instantánea del proveedor** | Reversión rápida o reconstrucción del servidor | Recuperación independiente si falla la cuenta o el almacenamiento del proveedor |
| **Copia coherente de la base de datos** | Recuperar el estado de la aplicación y las últimas escrituras | Restaurar por sí sola toda la configuración del servidor |
| **Copia de archivos y configuración** | Restaurar archivos subidos, parámetros, datos de la aplicación | Reconstrucción rápida de todo el servidor |
| **Copia externa independiente** | Sobrevivir a un fallo del servidor, cuenta o proveedor principal | Un RTO corto si no se ha ensayado la restauración |
| **Prueba de restauración** | Comprobar que funcionan copias, claves e instrucciones | Que los futuros trabajos seguirán funcionando sin supervisión |

Para muchas webs alojadas en un VPS, una base razonable es:

- disponer de una imagen o instantánea del proveedor para revertir rápidamente;
- guardar una copia independiente y cifrada de archivos, configuración y bases de datos en otro ámbito de fallo;
- conservar varios puntos de restauración;
- determinar la frecuencia de las copias de la base de datos según la pérdida aceptable;
- realizar pruebas de restauración periódicas.

Esto aporta más seguridad que confiar en un único estado de «copia realizada correctamente».

<a id="vps-backup-strategy-checker"></a>
## Comprobador de la estrategia de copias de seguridad

Este comprobador ayuda a identificar la arquitectura de recuperación necesaria. No garantiza que una restauración vaya a funcionar.

<div class="rounded-2xl bg-light p-6 dark:bg-darkmode-light">
<form id="vps-backup-strategy-checker-form">
  <div class="mb-6">
    <label for="bk-workload" class="form-label">Tipo de carga de trabajo</label>
    <select id="bk-workload" class="form-input">
      <option value="static">Sitio estático, informativo o que cambia poco</option>
      <option value="cms">WordPress, CMS o web de empresa</option>
      <option value="transactional">WooCommerce, pedidos, suscripciones o escrituras frecuentes</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rpo" class="form-label">Pérdida máxima de datos aceptable (RPO)</label>
    <select id="bk-rpo" class="form-input">
      <option value="24">Hasta 24 horas</option>
      <option value="4">Hasta 4 horas</option>
      <option value="1">Hasta 1 hora</option>
      <option value="lt1">Menos de 1 hora</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-rto" class="form-label">Interrupción máxima aceptable (RTO)</label>
    <select id="bk-rto" class="form-input">
      <option value="24">Hasta 24 horas</option>
      <option value="4">Hasta 4 horas</option>
      <option value="1">Alrededor de 1 hora</option>
      <option value="lt1">Menos de 1 hora</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-offsite" class="form-label">¿Existe una copia independiente fuera del servidor?</label>
    <select id="bk-offsite" class="form-input"><option value="no">No</option><option value="yes">Sí</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-db" class="form-label">¿Se ha verificado una copia coherente de la base de datos?</label>
    <select id="bk-db" class="form-input">
      <option value="na">No procede; no hay base de datos</option>
      <option value="no">No / no se sabe</option>
      <option value="yes">Sí</option>
    </select>
  </div>
  <div class="mb-6">
    <label for="bk-restore" class="form-label">¿Se ha completado correctamente una prueba de restauración reciente?</label>
    <select id="bk-restore" class="form-input"><option value="no">No</option><option value="yes">Sí</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-creds" class="form-label">¿Se guardan fuera del VPS las credenciales y la clave de recuperación de la copia cifrada?</label>
    <select id="bk-creds" class="form-input"><option value="no">No / no se sabe</option><option value="yes">Sí</option></select>
  </div>
  <div class="mb-6">
    <label for="bk-versions" class="form-label">¿Existen varios puntos de restauración y un historial de retención?</label>
    <select id="bk-versions" class="form-input"><option value="no">Solo el último / no se sabe</option><option value="yes">Sí</option></select>
  </div>
  <button class="btn btn-primary" type="submit">Evaluar la estrategia de copias</button>
</form>
<p id="vps-backup-strategy-result" class="mt-6 rounded border border-border p-4 dark:border-darkmode-border" role="status" aria-live="polite">Selecciona los requisitos de recuperación que correspondan a tu caso.</p>
</div>

<script>
document.addEventListener("DOMContentLoaded", function () {
  var form = document.getElementById("vps-backup-strategy-checker-form");
  if (!form) return;

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    function val(id) { return document.getElementById(id).value; }

    var workload = val("bk-workload");
    var rpo = val("bk-rpo");
    var rto = val("bk-rto");
    var offsite = val("bk-offsite") === "yes";
    var db = val("bk-db");
    var restore = val("bk-restore") === "yes";
    var creds = val("bk-creds") === "yes";
    var versions = val("bk-versions") === "yes";

    var criticalGap = !offsite || !restore || !creds || !versions || (db === "no");
    var result;

    if (criticalGap) {
      result = "FALLOS CRÍTICOS DE RESPALDO: la estrategia aún depende de un método de recuperación no probado o no independiente. Añade copias externas, varios puntos de restauración, credenciales y claves separadas, copias coherentes de la base de datos cuando proceda y una prueba real de recuperación.";
    } else if (rto === "lt1" || rto === "1") {
      result = "RTO BAJO: revisa la arquitectura de recuperación. Aunque las copias sean correctas, reconstruir manualmente puede superar una hora. Cronometra una prueba completa y considera automatización, imágenes preparadas, un servidor de reserva o separación de cargas si el RTO medido es demasiado alto.";
    } else if (workload === "transactional" || rpo === "lt1" || rpo === "1") {
      result = "SISTEMA TRANSACCIONAL: conserva las copias independientes y ajusta la frecuencia de respaldo de la base de datos al RPO necesario. Una copia nocturna no cumple un objetivo de pérdida máxima de una hora.";
    } else {
      result = "ESTRATEGIA BÁSICA DE RECUPERACIÓN: están presentes los componentes esenciales. Conserva los puntos del proveedor y las copias externas independientes, vigila los errores, guarda varias versiones y repite las restauraciones cronometradas.";
    }

    document.getElementById("vps-backup-strategy-result").textContent = result;
  });
});
</script>

<a id="start-with-rpo-and-rto"></a>
## Empieza por el RPO y el RTO

Hay dos cifras que deben determinar la estrategia.

### Objetivo de punto de recuperación: RPO

El RPO responde a la pregunta **¿cuántos datos recientes puede permitirse perder la empresa?**

- **24 horas:** quizá baste con un punto de recuperación diario válido.
- **4 horas:** una copia al día es insuficiente.
- **1 hora:** el estado cambiante de la aplicación o de la base de datos debe protegerse como mínimo con esa frecuencia.
- **Minutos:** las copias programadas tradicionales pueden no bastar.

El RPO mide **pérdida de datos**, no tiempo de inactividad.

### Objetivo de tiempo de recuperación: RTO

El RTO responde a **¿cuánto tiempo puede permanecer inaccesible el sitio o servicio?**

Una copia puede cumplir el RPO sin cumplir el RTO. Por ejemplo:

- se copia la base de datos cada hora;
- se perdería menos de una hora de información;
- pero preparar otro VPS, descargar los datos, restaurar la base de datos y validar la web requiere seis horas.

La estrategia puede satisfacer un RPO de una hora y tener un RTO real cercano a seis horas.

Las guías de continuidad de NIST distinguen el momento al que deben recuperarse los datos (RPO) del periodo máximo de indisponibilidad aceptable (RTO). Fija estos objetivos antes de elegir las herramientas.

## ¿Qué se debe incluir en las copias?

Clasifica lo que hay en el servidor entre elementos **que se pueden reconstruir** y datos **con estado o difíciles de sustituir**.

### Elementos reconstruibles

Normalmente pueden reproducirse a partir de código o automatización:

- sistema operativo base;
- paquetes;
- código de la aplicación guardado de forma segura en Git;
- imágenes de contenedores que pueden reconstruirse o descargarse;
- paquetes estándar del servidor web.

### Datos con estado o difíciles de recuperar

Suelen tener mayor prioridad:

- bases de datos;
- archivos subidos y contenido multimedia;
- buzones si el correo se aloja en el VPS;
- configuración;
- variables de entorno y secretos necesarios para restaurar;
- claves TLS o privadas si no es sencillo sustituirlas;
- datos generados por las aplicaciones;
- configuración de sitios y paneles;
- tareas cron y procesos en segundo plano;
- registros DNS si se administran en ese servidor;
- scripts propios no guardados en otro lugar.

No llenes el almacenamiento de respaldo con archivos temporales y cachés reconstruibles mientras olvidas la base de datos o las claves imprescindibles para iniciar el servicio.

<a id="snapshot-image-file-backup-and-replication-are-different"></a>
## Instantánea, imagen, copia de archivos y replicación no son lo mismo

No son mecanismos intercambiables.

### Instantánea o imagen del proveedor

Sirve para:

- volver rápidamente a un estado anterior tras una actualización arriesgada;
- recuperar el servidor completo;
- clonar o recrear la máquina virtual.

Limitaciones:

- puede depender del mismo proveedor o de la misma cuenta;
- puede resultar incómoda para recuperar un archivo o un solo sitio;
- hay que verificar la coherencia de las aplicaciones y bases de datos;
- una sola imagen reciente no conserva suficiente historial.

### Copia por archivos

Sirve para respaldar:

- subidas;
- configuraciones;
- datos seleccionados de la aplicación;
- restauraciones puntuales.

Herramientas como restic o Borg permiten guardar copias cifradas y versionadas en repositorios remotos.

### Copia de la base de datos

Emplea un método compatible con el motor:

- volcado lógico;
- herramienta de copia nativa;
- instantánea o proceso coherente con la aplicación.

No presupongas que copiar los archivos de una base de datos en funcionamiento genera una copia restaurable.

### Replicación o servidor de reserva

La replicación puede reducir la pérdida de datos o el tiempo de recuperación, pero no sustituye un historial de copias. También puede replicar un borrado accidental, un error de aplicación o datos dañados.

Utilízala cuando se requiera disponibilidad o un RTO reducido, pero conserva copias versionadas para recuperar estados anteriores.

<a id="a-practical-3-2-1-model-for-vps"></a>
## Aplicación práctica de la regla 3-2-1 a un VPS

La regla habitual 3-2-1 propone:

- **3 copias** de los datos importantes;
- **2 soportes o modalidades de almacenamiento y fallo distintos**;
- **1 copia externa** fuera del ámbito de fallo principal.

En un VPS podría traducirse en:

1. datos de producción en el VPS;
2. imagen del proveedor para recuperación rápida;
3. copia cifrada externa de archivos y bases de datos en un destino independiente.

El objetivo no es cumplir un eslogan al pie de la letra, sino impedir que un solo incidente destruya la producción y todas las copias.

Posibles ámbitos de fallo:

- sistema de archivos del VPS;
- almacenamiento de copias del proveedor;
- cuenta del proveedor;
- cuenta independiente de almacenamiento de objetos u otro proveedor;
- copia sin conexión o inmutable.

Si alguien que compromete el VPS puede borrar todas las copias con las mismas credenciales, la independencia es insuficiente.

## Copias coherentes de bases de datos

Las bases de datos cambian mientras el sitio está en funcionamiento. Una estrategia válida debe identificar cómo se protege el motor utilizado.

Para WordPress, MySQL o MariaDB pueden usarse:

- volcados lógicos;
- herramientas nativas del motor;
- instantáneas coordinadas;
- software que gestione explícitamente la coherencia de la base de datos.

Para PostgreSQL, emplea mecanismos propios de PostgreSQL, como copias compatibles con recuperación puntual (PITR), si lo exige el RPO.

Lo importante no es la marca de la herramienta, sino que la base de datos restaurada sea coherente y utilizable. Para el estado específico de WordPress, consulta [VPS para WordPress](/es/vps-para-wordpress/).

Comprueba que:

- finaliza el volcado o la copia;
- el archivo no está vacío;
- la restauración o importación funciona;
- existen tablas y registros representativos;
- la aplicación se conecta y puede realizar las lecturas y escrituras esenciales.

## Las webs transaccionales necesitan otro RPO

Una web informativa quizá tolere recuperar datos del día anterior; una tienda con pedidos, no necesariamente.

Para WooCommerce, suscripciones, facturación y pedidos, define la pérdida admisible de:

- pedidos;
- pagos;
- inventario;
- clientes;
- suscripciones;
- formularios enviados;
- archivos subidos.

Si la tienda recibe pedidos cada hora, una copia nocturna de la base de datos puede perder numerosas operaciones.

Consulta [VPS para WooCommerce](/es/vps-para-woocommerce/). Aquí la frecuencia debe fijarse según el periodo máximo aceptable de pérdida de transacciones.

## Frecuencia de las copias y retención

Cada clase de datos necesita una frecuencia compatible con su RPO.

Pueden aplicarse calendarios distintos:

- **Base de datos:** copias frecuentes.
- **Archivos subidos:** copias frecuentes o activadas por eventos.
- **Sistema y configuración:** después de cambios importantes y según calendario.
- **Imagen completa del proveedor:** menos frecuente, pero útil alrededor de cambios arriesgados.

La retención permite recuperar fallos que se descubren tarde. Un ejemplo orientativo puede conservar:

- puntos de recuperación recientes de cada hora;
- varias copias diarias;
- varias semanales;
- algunas mensuales.

La política exacta depende de:

- necesidades empresariales de recuperación;
- coste del almacenamiento;
- ritmo de cambio de los datos;
- obligaciones legales o normativas;
- tiempo durante el que un daño o una intrusión podrían pasar desapercibidos.

No conserves únicamente «la última».

## Mantén una copia independiente fuera del servidor

Una copia en el mismo disco del VPS no protege frente a:

- pérdida del disco o sistema de archivos;
- eliminación del servidor;
- compromiso de acceso root;
- ransomware;
- errores de la cuenta;
- pérdida de esa máquina virtual por parte del proveedor.

Traslada o transmite los datos de recuperación fuera del VPS.

Destinos posibles:

- almacenamiento de objetos;
- otro servicio o proveedor de copias;
- otro VPS utilizado únicamente para respaldos;
- almacenamiento sin conexión o sometido a controles.

Separa las credenciales de los proveedores o cuentas siempre que sea viable.

## Cifra las copias y protege también las claves

Cifra los datos sensibles tanto durante la transferencia como en reposo cuando corresponda.

El cifrado añade una dependencia importante: no guardes la **única** contraseña o clave de recuperación:

- solo en el VPS;
- solo en la misma cuenta o gestor de contraseñas que podría quedar inaccesible;
- solo dentro de la propia copia cifrada.

Conserva credenciales y claves en un lugar independiente y seguro. Comprueba durante los simulacros que se puede acceder a ellas.

## Separa las credenciales de copia y los permisos de borrado

Comprometer el servidor de producción no debería otorgar automáticamente la posibilidad de eliminar todas las copias.

Conviene usar:

- credenciales de copia con alcance limitado;
- permiso de escritura sin autorización general de borrado, si el almacenamiento lo permite;
- credenciales administrativas separadas;
- bloqueo de retención o inmutabilidad cuando proceda;
- copias desconectadas para datos de gran valor.

El diseño exacto depende del servicio. Las copias de seguridad también son una medida de seguridad: consulta [Seguridad del VPS](/es/seguridad-vps/).

## Supervisa los trabajos de copia

La automatización evita olvidos, pero un proceso automatizado también puede fallar en silencio.

Vigila:

- hora de la última copia correcta;
- trabajos fallidos o incompletos;
- disponibilidad del repositorio y almacenamiento;
- caducidad de credenciales;
- espacio libre antes de preparar archivos temporales;
- cuota de almacenamiento externo;
- fallos de los volcados de bases de datos;
- cambios en la duración de los trabajos;
- copias anormalmente pequeñas;
- errores de retención o limpieza.

Que cron marque un trabajo como ejecutado no significa que la restauración funcione.

Para alertas generales del sistema, consulta [Supervisión del VPS](/es/monitorizacion-vps/). La salud de los respaldos sigue siendo parte de la recuperación.

<a id="test-restores-and-measure-real-rto"></a>
## Ensaya restauraciones y mide el RTO real

Una copia solo resulta fiable cuando se ha demostrado que puede restaurarse.

Haz los ensayos en un destino limpio y aislado. Comprueba una secuencia suficientemente completa:

1. preparar un VPS nuevo o entorno de pruebas;
2. localizar el punto de recuperación correcto;
3. recuperar las credenciales del repositorio y del cifrado;
4. restaurar archivos y configuración;
5. importar o restaurar la base de datos;
6. recuperar secretos y certificados necesarios;
7. configurar servicios y red;
8. iniciar la aplicación;
9. probar las páginas y transacciones importantes;
10. verificar tareas e integraciones;
11. medir el tiempo total de recuperación.

Registra el resultado.

Si el RTO empresarial es de cuatro horas y el ensayo tarda ocho, el plan no cumple ese requisito, aunque se hayan recuperado todos los archivos.

NIST destaca la necesidad de crear copias periódicamente, probar su restauración y realizar ejercicios de recuperación.

## Importa el nivel de detalle de la restauración

Una buena estrategia debe responder al tipo de fallo real.

### Recuperación de un solo archivo o sitio

Necesaria para:

- archivo subido eliminado;
- configuración incorrecta;
- un sitio comprometido;
- restaurar una base de datos o tabla concreta.

### Recuperación del servidor completo

Necesaria para:

- VPS averiado o eliminado;
- fallo del sistema de archivos;
- compromiso grave;
- sustitución del servidor o proveedor.

Una imagen de disco completa puede resultar poco práctica para recuperar un archivo. Un respaldo limitado a archivos puede hacer demasiado lenta la reconstrucción del VPS. Combina ambos métodos.

## Varios sitios necesitan restauraciones independientes

En un VPS con varios sitios, recuperar el sitio A no debería devolver los sitios B, C y D al estado de ayer.

Prefiere copias que permitan restaurar:

- una carpeta raíz de documentos;
- una base de datos;
- un usuario o cuenta del panel;
- un conjunto de archivos subidos;
- el VPS completo únicamente cuando sea necesario.

Sobre arquitectura y separación de riesgos, consulta [VPS para varios sitios web](/es/vps-para-varios-sitios-web/).

## Las copias también pueden causar interrupciones

Los trabajos de respaldo consumen recursos:

- CPU al exportar bases de datos;
- CPU al comprimir;
- operaciones de lectura del almacenamiento;
- espacio temporal en disco;
- ancho de banda al enviar datos al almacenamiento externo;
- interferencia con importaciones, análisis, cachés o picos de tráfico.

No intentes crear un archivo temporal de 30 GB en un VPS con solo 10 GB libres.

Cuando sea posible:

- transmite las copias directamente fuera del servidor;
- vigila el uso temporal del disco;
- programa los trabajos pesados fuera de las horas punta;
- limita la velocidad si la herramienta lo permite;
- mide su duración.

<a id="how-vdsina-backups-fit-the-strategy"></a>
## Cómo encajan las copias de VDSina en la estrategia

La documentación pública de VDSina describe varias funciones de recuperación:

- crear manualmente copias del servidor;
- programar copias;
- restaurar una copia sobre el servidor de origen;
- crear un servidor nuevo desde una copia;
- clonar un servidor;
- descargar una imagen de copia.

La documentación sobre descarga muestra nombres de archivo como:

<code>vXXX.backup.hosted-by-vdsina.com.img.gz</code>

Descargar la imagen favorece la portabilidad: no es necesario guardar todas las copias dentro del panel del proveedor.

No obstante:

- considera la imagen del proveedor **una capa**, no toda la estrategia;
- prueba cómo utilizar el archivo descargado en el entorno de recuperación elegido;
- no supongas que todos los hipervisores podrán abrirlo sin convertirlo;
- conserva respaldos de aplicaciones, archivos y bases de datos para recuperación selectiva;
- guarda una copia en un ámbito de fallo independiente cuando el riesgo lo justifique.

Los términos de VDSina atribuyen al cliente la responsabilidad sobre las copias y recomiendan una rutina de respaldo con pruebas periódicas de restauración.

Según sus notas de ayuda, crear un VPS a partir de una copia puede exigir condiciones concretas de ubicación y espacio suficiente; después de restaurar quizá haya que ajustar la red.

No confundas copia con migración. Un respaldo ayuda a tener una vía de retorno, pero el cambio definitivo, las últimas escrituras, el DNS y la reversión son cuestiones separadas: consulta [Migración del sitio web a un VPS](/es/migrar-un-sitio-web-a-vps/).

<p><a class="btn btn-primary" href="https://www.vdsina.com/?partner=ni8gzrvz75" target="_blank" rel="sponsored nofollow noopener">Consultar opciones actuales de copias VPS</a></p>
<p><small>Aviso: el editor mantiene una relación profesional con VDSina. Este sitio puede recibir una comisión si contratas mediante el enlace de afiliado. Las funciones del proveedor no sustituyen las copias independientes ni las pruebas de restauración.</small></p>

## Procedimiento documentado de recuperación

Escribe el procedimiento antes de sufrir una caída.

Como mínimo, registra:

- destinos de las copias;
- nombres de los puntos y periodos de retención;
- credenciales de los repositorios;
- ubicación de las claves de descifrado;
- clasificación de archivos, bases de datos y configuración;
- pasos para preparar un servidor nuevo;
- versiones de software y entorno de ejecución;
- orden de restauración;
- DNS y configuración de red;
- integraciones y webhooks;
- pruebas de aceptación;
- responsable de decidir si se recupera o se revierte.

Guarda este procedimiento en un lugar accesible incluso cuando el VPS no lo esté.

## Lista de comprobación de copias VPS

| Control | Condición que debe cumplirse |
|---|---|
| RPO | Pérdida máxima de datos aceptable definida |
| RTO | Interrupción máxima aceptable definida |
| Inventario | Bases de datos, archivos subidos, configuración, secretos y otros estados clasificados |
| Recuperación del proveedor | Frecuencia y alcance de imágenes e instantáneas conocidos |
| Base de datos | Método coherente con el motor y realmente restaurable |
| Copia externa | Datos fuera del ámbito de fallo del VPS |
| Credenciales | Cuenta de copia de alcance limitado y separada de producción |
| Cifrado | Datos sensibles cifrados cuando proceda |
| Recuperación de claves | Contraseña o clave disponible fuera del VPS averiado |
| Retención | Varios puntos históricos disponibles |
| Supervisión | Fallos, trabajos incompletos y copias antiguas detectables |
| Disco y E/S | El proceso no llena ni sobrecarga producción sin avisar |
| Recuperación selectiva | Posibilidad de restaurar archivos, sitios y bases de datos |
| Recuperación completa | Procedimiento para reconstruir todo el VPS y sus servicios |
| Prueba | Restauración satisfactoria en un entorno aislado |
| RTO medido | Tiempo real documentado y dentro del objetivo |
| Procedimiento | Orden, credenciales, DNS y pruebas de aceptación registrados |
| Responsable | Persona o equipo encargado de las copias y restauraciones |

## Referencias técnicas

- NIST SP 800-34 Rev.1: RPO, RTO y planificación de contingencias.
- NIST SP 1339: creación de copias, pruebas y ejercicios de recuperación.
- Ubuntu: herramientas de copia y restauración restic.
- Ubuntu: BorgBackup.
- Términos de VDSina: responsabilidad del cliente sobre las copias.
- VDSina: copias, restauración y servidores nuevos desde una copia.
- VDSina: copias programadas.
- VDSina: descarga y utilización de una copia del servidor.

<a id="faq"></a>
## Preguntas frecuentes

### ¿Qué es una buena estrategia de copias para un VPS?

Define RPO y RTO, conserva copias independientes, protege las bases de datos con un método coherente con la aplicación, retén varias versiones, supervisa los trabajos fallidos y restaura periódicamente en un entorno de pruebas limpio.

### ¿Basta con una instantánea del VPS?

No como única medida. Una imagen o instantánea del proveedor sirve para revertir rápido o recuperar el servidor completo, pero puede depender de la misma cuenta y no facilita recuperar elementos aislados.

### ¿Qué significa 3-2-1 en un VPS?

Mantener los datos activos y varias copias de recuperación distribuidas en sistemas de almacenamiento y ámbitos de fallo independientes, con al menos una copia fuera de la ruta de fallo principal.

### ¿Cada cuánto debo hacer copias de un VPS?

Según el RPO de cada tipo de dato. Un sitio estático quizá tolere copias diarias; una base de datos transaccional puede necesitar protección cada hora o con mayor frecuencia.

### ¿En qué se diferencian el RPO y el RTO?

El RPO limita la pérdida de datos recientes aceptable; el RTO limita cuánto tiempo puede quedar inactivo el servicio antes de recuperarlo.

### ¿Debo copiar todo el VPS o solo los archivos de la web?

Normalmente conviene combinar ambos métodos. La imagen permite recuperar el servidor completo con rapidez; las copias de archivos y bases de datos facilitan recuperaciones selectivas y coherentes.

### ¿Cómo se respaldan MySQL o PostgreSQL de forma segura?

Con un volcado lógico, una herramienta nativa del motor o un procedimiento coordinado que mantenga la coherencia. Después hay que restaurar o importar la copia en un entorno aislado y comprobar los datos.

### ¿Hay que cifrar las copias?

Los datos sensibles deben cifrarse cuando corresponda; pero la clave o contraseña necesaria para recuperarlos debe guardarse de forma segura fuera del VPS.

### ¿La replicación es una copia de seguridad?

Por sí sola, no. Puede replicar errores, datos dañados o borrados malintencionados. Conserva además copias versionadas para recuperar estados históricos.

### ¿VDSina ofrece copias de seguridad VPS?

Su documentación describe copias manuales y programadas, funciones de restauración y creación de servidores desde copias, así como imágenes descargables. Sus condiciones siguen atribuyendo al cliente la responsabilidad de proteger sus datos y recomiendan probar las restauraciones.

### ¿Cada cuánto conviene probar la restauración?

Según un calendario definido y después de cambios importantes en la arquitectura o en el método de respaldo. Las cargas críticas o de rápida evolución necesitan ensayos suficientemente frecuentes para confiar en el tiempo medido de recuperación.

### ¿Qué ocurre si mi RTO es inferior a una hora?

Una estrategia basada únicamente en copias puede tardar demasiado. Cronometra una recuperación completa y considera automatización, imágenes preparadas, servidores de reserva o cambios de arquitectura si el resultado supera el objetivo.
