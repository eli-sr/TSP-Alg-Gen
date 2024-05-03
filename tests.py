#!/usr/bin/env python3

import unittest
from main import *
from unittest.mock import patch

class Tests(unittest.TestCase):
    def test_gen_cromosomas_aleatorios(self):
        # El valor del cromosoma no contiene el valor inicial
        poblacion = gen_cromosomas_aleatorios(1, CIUDADES_INDEX, 0)
        cromosoma = poblacion[0]
        assert 0 not in cromosoma.value
    
    def test_get_lowest_fitness(self):
        # El cromosoma con menor fitness es devuleto
        cromosoma1 = Cromosoma(13,[2]) # Pamplona -> Bilbao
        cromosoma2 = Cromosoma(13,[4]) # Pamplona -> Cádiz
        cromosoma1.calc_fitness() # Menor fitness
        cromosoma2.calc_fitness() # Mayor fitness
        cromosomas = [cromosoma1, cromosoma2] 
        assert get_lowest_fitness(cromosomas) == cromosoma1
    
    @patch('main.random.randint')
    def test_cruce_parcialmente_mapeado(self, mock_randint):
        # El hijo devuelto es el correcto
        mock_randint.side_effect = [3, 6]  # Valores para punto_cruzamiento1 y punto_cruzamiento2
        padre1 = Cromosoma(13,[1,2,3,4,5,6,7,8,9])
        padre2 = Cromosoma(13,[9,3,7,8,2,6,5,1,4])
        hijoSol = Cromosoma(13,[9,3,2,4,5,6,7,1,8])
        hijo = cruce_parcialmente_mapeado(padre1, padre2) 
        assert np.array_equal(hijo.value, hijoSol.value)

        # El hijo devuelto es el correcto
        mock_randint.side_effect = [0, 8]
        padre1 = Cromosoma(13,[0,1,2,3,4,5,6,7,8,9,10,11,12,14,15,16,17,18,19])
        padre2 = Cromosoma(13,[19,7,4,14,3,8,16,9,10,17,6,0,11,15,12,2,5,18,1])
        hijoSol = Cromosoma(13,[0,1,2,3,4,5,6,7,8,17,16,19,11,15,12,14,10,18,9])
        hijo = cruce_parcialmente_mapeado(padre1, padre2) 
        assert np.array_equal(hijo.value, hijoSol.value)

        # El hijo devuelto es el correcto
        mock_randint.side_effect = [3, 6]
        padre1 = Cromosoma(13,[1,2,3,4,5,6,7,8,9])
        padre2 = Cromosoma(13,[4,5,3,1,8,7,6,9,2])
        hijoSol1 = Cromosoma(13,[1,8,3,4,5,6,7,9,2])
        hijo1 = cruce_parcialmente_mapeado(padre1, padre2) 
        assert np.array_equal(hijo1.value, hijoSol1.value)

        # El hijo devuelto es el correcto
        mock_randint.side_effect = [3, 6]
        hijoSol2 = Cromosoma(13,[4,2,3,1,8,7,6,5,9])
        hijo2 = cruce_parcialmente_mapeado(padre2, padre1) 
        assert np.array_equal(hijo2.value, hijoSol2.value)


if __name__ == '__main__':
    unittest.main()
