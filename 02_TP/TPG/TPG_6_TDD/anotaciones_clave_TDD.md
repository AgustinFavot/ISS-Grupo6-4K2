# Notas clase virtual TDD
La clase virtual se encuentra subida en la UV, he realizado un par de anotaciones para darle base teórica y justificación al desarrollo de la TDD del trabajo práctico grupal correctamente.
La información está basada en la bibiliografía "TDD By Example" de Kent Beck

## El ¿Que? y ¿Cómo? del TDD
Las pruebas TDD se deben hacer con un enfoque proactivo por medio de pruebas unitarias automatizada, con ello defino que debe hacer el software.

## 3 leyes del TDD
1- No escribir código de producción sin antes haber escrito test unitarios que fallen.
2- Escribir el mínimo de código para provocar el fallo, si no compila también se considera un fallo.
3- Escribir el mínimo de código de producción para que el test pase.

## Ciclo del TDD
Hay 3 etapas que se realizan cíclicamente durante el TDD:
1- RED: en ella se declara una intención "Quiero que al pasarle [datos] el sistema devuelva [este] resultado"
2- GREEN: se realiza un enfoque imperativo, hago el mínimo de código posible para que la prueba falle.
3- REFACTOR: se reestructura el código interno sin alterar el comportamiento externo del mismo, se deben aplicar buenas prácticas que se destallarán a continuación para mejores resultados.

## Estructura de un test
- Definición de la función del test
- Precondiciones: lo que necesito previo a ejecutar el test (datos, crear un objeto, loguearse al sistema, permisos de usuario, etc)
- Pasos: es la ejecución paso a paso de la prueba unitaria
- Resultado: comprobación para ver si el test unitario pasa ó falla

## Patrones/Buenas prácticas de TDD
No te dan una manera exacta de hacer las cosas sino recomendaciónes que ya han sido probadas.

### Para RED
- Starter test: "debo arrancar con un test inicial, lo importante es comenzar"
- One step: "continúo el próximo test más sencillo según la escala de complejidad" se refiere a tomar test de menor a mayor complejidad, esto puede transladarse a la escapa de estimación de una US por ejemplo.
- Expedition test: "cuando ya estoy avanzando con la prueba si se presenta un debate sobre el desarrollo del mismo debo generar un test para solventar las dudas"
- Learning test: "si utilizo una herramienta externa para la prueba debo hacer un test para aprender cómo esta funciona"
- Another test: "si durante el desarrollo de la prueba se presentan diversos resultados posibles no debo alejarme de la de la intención inicial por la que se hizo el test, lo que puedo hacer es anotar ese posible desenlace y desarrollarlo después"
- Regresion test: "si se presenta un problema durante la ejecución de la prueba debo definir un test con el paso a paso para replicar este fallo y que no vuelva a suceder"

### Para GREEN
- Fake it: "falsificar la información de la prueba para que genere el resultado que espero y pase"
- Triangulación: "hacer tantas pruebas sean necesarias para asegurarse no haya errores"
- Obvius Implementation: "implementar de la manera más simple y obvia posible"
- One-to-many: "si la funncionalidad puede ejecutarse en múltiples casos individuales a la vez, primero debo hacer que funcione en una unidad y luego implementar para que funcione en varias"

### Para el Diseño de Test
- Isolated test: "las pruebas deben ser lo más independientes posible entre sí"
- Test first: "primero escribo una prueba y luego desarrollo el código"
- Assert text: "si es complejo el test arranco por lo que se quiere probar y luego voy en inversa desde el resultado hasta el objetivo desglozando el código parte por parte"
- Test data: "la información a usar en pruebas debe ser lo más sencilla y fácil de entender posible"
- Evident data: "se debe entendere la relación entre las entradas y salidas de la prueba"
