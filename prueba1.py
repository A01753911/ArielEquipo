from dagor import JuegoCaballosBailadores, JugadorCaballosBailadoresAleatorio, JugadorCaballosBailadores
from random import choice, randint
import time

class JugadorCaballosBailadoresEquipo5(JugadorCaballosBailadores):

    def distancia(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def movimientos_posibles(self, posicion_caballo):
        movimientos = []
        for dx, dy in [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]:
            nuevo_x, nuevo_y = posicion_caballo[0] + dx, posicion_caballo[1] + dy
            if 0 <= nuevo_x < self._juego.renglones and 0 <= nuevo_y < self._juego.columnas:
                movimientos.append((nuevo_x, nuevo_y))
        return movimientos

    def centro_del_tablero(self):
        centro_x = [self._juego.renglones // 2, (self._juego.renglones - 1) // 2]
        centro_y = [self._juego.columnas // 2, (self._juego.columnas - 1) // 2]
        return [(x, y) for x in centro_x for y in centro_y]

    def heuristica(self, posicion):
        _, _, _, rB, rN, cB, cN = posicion
        mi_caballo = cB if self.simbolo == 'B' else cN
        caballo_oponente = cN if self.simbolo == 'B' else cB
        rey_oponente = rN if self.simbolo == 'B' else rB

        valor = 0
        control_centro = 150 if mi_caballo in self.centro_del_tablero() else 0
        valor += control_centro

        # Incrementar la agresividad hacia el rey oponente
        if mi_caballo == rey_oponente:
            valor += 600
        else:
            distancia_rey = self.distancia(mi_caballo, rey_oponente)
            valor -= distancia_rey * 40  # Mayor penalización por distancia al rey

        # Estrategia defensiva ajustada
        if mi_caballo == caballo_oponente:
            valor -= 400

        return valor

    def minimax(self, posicion, profundidad, jugador_maximizador, alfa=-float('inf'), beta=float('inf')):
        # Aumentar la profundidad de búsqueda
        if profundidad == 0 or self._juego.juego_terminado(posicion):
            return self.heuristica(posicion)

        if jugador_maximizador:
            max_eval = -float('inf')
            for p in self.posiciones_siguientes(posicion):
                eval = self.minimax(p, profundidad - 1, False, alfa, beta)
                max_eval = max(max_eval, eval)
                alfa = max(alfa, eval)
                if beta <= alfa:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for p in self.posiciones_siguientes(posicion):
                eval = self.minimax(p, profundidad - 1, True, alfa, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alfa:
                    break
            return min_eval

    def tira(self, posicion):
        mejor_movimiento = None
        mejor_valor = -float('inf')
        empates = []

        for p in self.posiciones_siguientes(posicion):
            valor = self.minimax(p, 4, False)  # Aumento de la profundidad a 4
            if valor > mejor_valor:
                mejor_valor = valor
                mejor_movimiento = p
                empates = [p]
            elif valor == mejor_valor:
                empates.append(p)

        if len(empates) > 1:
            return choice(empates)

        return mejor_movimiento

# Configuración del juego
n, m = 5, 5  # Tamaño del tablero
jugador1 = JugadorCaballosBailadoresEquipo5('Equipo5')
jugador2 = JugadorCaballosBailadoresAleatorio('RandomBoy')
juego = JuegoCaballosBailadores(jugador1, jugador2, n, m)

# Iniciar el temporizador
inicio = time.time()

# Iniciar 1000 juegos
juego.inicia(veces=1000)

# Detener el temporizador y calcular la duración
fin = time.time()
duracion = fin - inicio
print(f"Tiempo total de ejecución: {duracion} segundos")
