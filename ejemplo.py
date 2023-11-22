from dagor import JuegoD10, JugadorD10Interactivo, JugadorD10Aleatorio, JugadorD10Estrategico

j1 = JugadorD10Interactivo("Humano")
j2 = JugadorD10Estrategico("Maquina")

juego = JuegoD10(j2, j1)

juego.inicia()