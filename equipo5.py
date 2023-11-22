from dagor import JuegoCaballosBailadores, JugadorCaballosBailadoresAleatorio, JugadorCaballosBailadores
from random import randint, choice
import time

class JugadorCaballosBailadoresEquipo5(JugadorCaballosBailadores): 
    
    def evaluar_posiciones_estrategicas(self, mi_caballo, posicion):
        centro = (self.juego.renglones // 2, self.juego.columnas // 2)
        distancia_centro = abs(mi_caballo[0] - centro[0]) + abs(mi_caballo[1] - centro[1])
        # Cuanto más cerca del centro, mayor es el valor
        return max(self.juego.renglones, self.juego.columnas) - distancia_centro
        
    def evaluar_agresividad(self, mi_caballo, caballo_oponente):
        # Calcula la distancia al caballo oponente
        distancia_caballo_oponente = abs(mi_caballo[0] - caballo_oponente[0]) + abs(mi_caballo[1] - caballo_oponente[1])
        # Cuanto más cerca del caballo oponente, mayor es el valor
        return max(self.juego.renglones, self.juego.columnas) - distancia_caballo_oponente
        
    def evaluar_riesgo(self, mi_caballo, caballo_oponente):
        if caballo_oponente in self.posiciones_ataque(mi_caballo):
            # Penalización alta si el caballo oponente puede capturar al mío
            return -200
        return 0
    
    def heuristica(self, posicion):
        _, _, _, rB, rN, cB, cN = posicion
        mi_caballo = cB if self.simbolo == 'B' else cN
        caballo_oponente = cN if self.simbolo == 'B' else cB
        rey_oponente = rN if self.simbolo == 'B' else rB

        # Cálculos de distancias
        distancia_rey = abs(mi_caballo[0] - rey_oponente[0]) + abs(mi_caballo[1] - rey_oponente[1])
        distancia_caballo = abs(mi_caballo[0] - caballo_oponente[0]) + abs(mi_caballo[1] - caballo_oponente[1])

        # Seguridad: evitar ser capturado
        seguridad = -100 if caballo_oponente in self.posiciones_ataque(mi_caballo) else 0

        # Movilidad: número de movimientos posibles
        movilidad = len(self.posiciones_siguientes(posicion))

        # Consideraciones adicionales de posicionamiento
        centro = (self.juego.renglones // 2, self.juego.columnas // 2)
        distancia_centro = abs(mi_caballo[0] - centro[0]) + abs(mi_caballo[1] - centro[1])
        distancia_bordes = min(mi_caballo[0], self.juego.renglones - mi_caballo[0]) + min(mi_caballo[1], self.juego.columnas - mi_caballo[1])
        estrategia = self.evaluar_posiciones_estrategicas(mi_caballo, posicion)
        agresividad = self.evaluar_agresividad(mi_caballo, caballo_oponente)
        riesgo = self.evaluar_riesgo(mi_caballo, posicion)
        

        # Ponderaciones ajustables
        ponderacion_distancia_rey = 30
        ponderacion_distancia_caballo = 15
        ponderacion_seguridad = 100
        ponderacion_movilidad = 25
        ponderacion_centro = 15
        ponderacion_bordes = 10
        ponderacion_estrategia = 20
        ponderacion_agresividad = 20
        ponderacion_riesgo = 20

        # Cálculo del valor heurístico
        valor = (-distancia_rey * ponderacion_distancia_rey - 
            distancia_caballo * ponderacion_distancia_caballo +
            seguridad * ponderacion_seguridad + 
            movilidad * ponderacion_movilidad - 
            distancia_centro * ponderacion_centro - 
            distancia_bordes * ponderacion_bordes +
            estrategia * ponderacion_estrategia +
            agresividad * ponderacion_agresividad -
            riesgo * ponderacion_riesgo)
        return valor

    
    def determinar_fase_juego(self):
        # Considera una fase avanzada si se han realizado más de 15 movimientos
        return self.juego._num_tiro > 15

    def posiciones_ataque(self, caballo):
        return [(caballo[0] + r, caballo[1] + c) for r in [-2, -1, 1, 2] for c in [-2, -1, 1, 2] if abs(r) != abs(c)]

    def minimax(self, posicion, profundidad, alpha, beta, es_maximizador):
        if profundidad == 0 or self.juego.juego_terminado(posicion):
            return self.heuristica(posicion)

        if es_maximizador:
            max_eval = float('-inf')
            for nueva_pos in self.juego.posiciones_siguientes(posicion):
                eval = self.minimax(nueva_pos, profundidad - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            for nueva_pos in self.juego.posiciones_siguientes(posicion):
                eval = self.minimax(nueva_pos, profundidad - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def tira(self, posicion):
        mejor_tiro = None
        mejor_evaluacion = float('-inf')
        alpha = float('-inf')
        beta = float('inf')

        # Ajusta la profundidad según la fase del juego
        profundidad = 5 if self.determinar_fase_juego() else 3

        for nueva_pos in self.juego.posiciones_siguientes(posicion):
            eval = self.minimax(nueva_pos, profundidad, alpha, beta, False)
            if eval > mejor_evaluacion:
                mejor_evaluacion = eval
                mejor_tiro = nueva_pos

        return mejor_tiro

# Configuración del juego
n, m = 5, 5  # Tamaño del tablero
jugador1 = JugadorCaballosBailadoresEquipo5('Equipo5')
jugador2 = JugadorCaballosBailadoresAleatorio('RandomBoy')
juego = JuegoCaballosBailadores(jugador1, jugador2, n, m)

# Iniciar el temporizador
inicio = time.time()

# Iniciar 100 juegos
juego.inicia(veces=1000)

# Detener el temporizador y calcular la duración
fin = time.time()
duracion = fin - inicio
print(f"Tiempo total de ejecución: {duracion} segundos")
