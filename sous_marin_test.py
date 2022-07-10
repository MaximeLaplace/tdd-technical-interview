from sous_marin import SousMarin

# 1 - Ecriture d'un test
# 2 - minimal code
# 3 - refactoring

'''

. . . . # # . .
. . . . # # # .
. . . . . . . .
# . . . . . . #
. . # # # # . #
. # # # # # # #

'''

sample_ocean = [
    [0, 0, 0, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 1, 1, 1, 1, 0, 1],
    [0, 1, 1, 1, 1, 1, 1, 1],
]


class TestSousMarin:
    def test_radar_1(self):
        """ test si au milieu ça marche """
        sm = SousMarin(4,2,sample_ocean)
        assert sm.radar() == {
            'up':True,
            'forward':False,
            'backward':False,
            'down':False
        }

    def test_radar_2(self):
        """ test si sur les bords ça marche """
        sm = SousMarin(0,0, sample_ocean)

        assert sm.radar()['backward'] == True
        assert sm.radar()['up'] == True

        sm.x = len(sample_ocean[0]) - 1
        sm.y = len(sample_ocean) - 1
        assert sm.radar()['forward'] == True
        assert sm.radar()['down'] == True

    def test_is_in_danger(self):
        sm = SousMarin(2,2,sample_ocean,1,5)

        assert sm.is_in_danger() == {
            'fuel_danger': True,
            'oxygen_danger': False
        }
        sm.fuel = 5
        sm.oxygen = 1

        assert sm.is_in_danger() == {
            'fuel_danger' : False,
            'oxygen_danger' : True
        }

        sm.fuel = 0
        sm.oxygen = 0

        assert sm.is_in_danger() == {
            'fuel_danger' : True,
            'oxygen_danger' : True
        }

    def test_step_up(self) :
        sm = SousMarin(3,0,sample_ocean,2,2)
        sm.step_up()
        assert sm.y == 0
        assert sm.fuel == 2
        assert sm.oxygen == 2

        sm = SousMarin(3,2,sample_ocean,1,2)
        sm.step_up()
        assert sm.y == 2
        assert sm.fuel == 1
        assert sm.oxygen == 2

        sm = SousMarin(3,2,sample_ocean,2,1)
        sm.step_up()
        assert sm.y == 2
        assert sm.fuel == 2
        assert sm.oxygen == 1

        sm = SousMarin(3,2,sample_ocean,2,2)
        sm.step_up()
        assert sm.y == 1
        assert sm.fuel == 1
        assert sm.oxygen == 1

    def test_step_down(self) :
        sm = SousMarin(3,5,sample_ocean,2,2)
        sm.step_down()
        assert sm.y == 5
        assert sm.fuel == 2
        assert sm.oxygen == 2

        sm = SousMarin(3,2,sample_ocean,1,2)
        sm.step_down()
        assert sm.y == 2
        assert sm.fuel == 1
        assert sm.oxygen == 2

        sm = SousMarin(3,2,sample_ocean,2,1)
        sm.step_down()
        assert sm.y == 2
        assert sm.fuel == 2
        assert sm.oxygen == 1

        sm = SousMarin(3,2,sample_ocean,2,2)
        sm.step_down()
        assert sm.y == 3
        assert sm.fuel == 1
        assert sm.oxygen == 1

    def test_step_forward(self) :
        sm = SousMarin(len(sample_ocean[0])-1,0,sample_ocean,2,2)
        sm.step_forward()
        assert sm.x == len(sample_ocean[0])-1
        assert sm.fuel == 2
        assert sm.oxygen == 2

        sm = SousMarin(len(sample_ocean[0])-2,0,sample_ocean,1,2)
        sm.step_forward()
        assert sm.x == len(sample_ocean[0])-2
        assert sm.fuel == 1
        assert sm.oxygen == 2

        sm = SousMarin(len(sample_ocean[0])-2,0,sample_ocean,2,1)
        sm.step_forward()
        assert sm.x == len(sample_ocean[0])-2
        assert sm.fuel == 2
        assert sm.oxygen == 1

        sm = SousMarin(len(sample_ocean[0])-2,0,sample_ocean,2,2)
        sm.step_forward()
        assert sm.x == len(sample_ocean[0])-1
        assert sm.fuel == 1
        assert sm.oxygen == 1

    def test_step_backward(self) :
        sm = SousMarin(0,3,sample_ocean,2,2)
        sm.step_backward()
        assert sm.x == 0
        assert sm.fuel == 2
        assert sm.oxygen == 2

        sm = SousMarin(3,2,sample_ocean,1,2)
        sm.step_backward()
        assert sm.x == 3
        assert sm.fuel == 1
        assert sm.oxygen == 2

        sm = SousMarin(3,2,sample_ocean,2,1)
        sm.step_backward()
        assert sm.x == 3
        assert sm.fuel == 2
        assert sm.oxygen == 1

        sm = SousMarin(3,2,sample_ocean,2,2)
        sm.step_backward()
        assert sm.x == 2
        assert sm.fuel == 1
        assert sm.oxygen == 1

    def test_move_down(self):
        # Ne peut pas move quand un rocher est dans le chemin
        sm = SousMarin(0,2,sample_ocean,10,10)
        sm.move_down(2)
        assert sm.y == 2
        assert sm.fuel == 10
        assert sm.oxygen == 10

        # Ne peut pas move quand pas de fuel
        sm = SousMarin(1,2,sample_ocean,2,10)
        sm.move_down(2)
        assert sm.y == 2
        assert sm.fuel == 2
        assert sm.oxygen == 10

        # Ne peut pas move quand pas d oxygene
        sm = SousMarin(1,2,sample_ocean,10,1)
        sm.move_down(2)
        assert sm.y == 2
        assert sm.fuel == 10
        assert sm.oxygen == 1

        # Peut move
        sm = SousMarin(1,2,sample_ocean,10,10)
        sm.move_down(2)
        assert sm.y == 4
        assert sm.fuel == 8
        assert sm.oxygen == 9

    def test_move_up(self):
        # Ne peut pas move quand un rocher est dans le chemin
        sm = SousMarin(0,5,sample_ocean,10,10)
        sm.move_up(3)
        assert sm.y == 5
        assert sm.fuel == 10
        assert sm.oxygen == 10

        # Ne peut pas move quand pas de fuel
        sm = SousMarin(1,4,sample_ocean,2,10)
        sm.move_up(2)
        assert sm.y == 4
        assert sm.fuel == 2
        assert sm.oxygen == 10

        # Ne peut pas move quand pas d oxygene
        sm = SousMarin(1,2,sample_ocean,10,1)
        sm.move_up(2)
        assert sm.y == 2
        assert sm.fuel == 10
        assert sm.oxygen == 1

        # Peut move
        sm = SousMarin(1,4,sample_ocean,10,10)
        sm.move_up(2)
        assert sm.y == 2
        assert sm.fuel == 8
        assert sm.oxygen == 9

    def test_move_forward(self):
        # Ne peut pas move quand un rocher est dans le chemin
        sm = SousMarin(3,1,sample_ocean,10,10)
        sm.move_forward(4)
        assert sm.x == 3
        assert sm.fuel == 10
        assert sm.oxygen == 10

        # Ne peut pas move quand pas de fuel
        sm = SousMarin(0,0,sample_ocean,2,10)
        sm.move_forward(3)
        assert sm.x == 0
        assert sm.fuel == 2
        assert sm.oxygen == 10

        # Ne peut pas move quand pas d oxygene
        sm = SousMarin(0,0,sample_ocean,10,1)
        sm.move_forward(2)
        assert sm.x == 0
        assert sm.fuel == 10
        assert sm.oxygen == 1

        # Peut move
        sm = SousMarin(0,0,sample_ocean,10,10)
        sm.move_forward(3)
        assert sm.x == 3
        assert sm.fuel == 7
        assert sm.oxygen == 9

    def test_move_backward(self):
        # Ne peut pas move quand un rocher est dans le chemin
        sm = SousMarin(1,3,sample_ocean,10,10)
        sm.move_backward(2)
        assert sm.x == 1
        assert sm.fuel == 10
        assert sm.oxygen == 10

        # Ne peut pas move quand pas de fuel
        sm = SousMarin(3,3,sample_ocean,2,10)
        sm.move_backward(2)
        assert sm.x == 3
        assert sm.fuel == 2
        assert sm.oxygen == 10

        # Ne peut pas move quand pas d oxygene
        sm = SousMarin(3,3,sample_ocean,10,1)
        sm.move_backward(2)
        assert sm.x == 3
        assert sm.fuel == 10
        assert sm.oxygen == 1

        # Peut move
        sm = SousMarin(3,3,sample_ocean,10,10)
        sm.move_backward(2)
        assert sm.x == 1
        assert sm.fuel == 8
        assert sm.oxygen == 9

    def test_shoot(self) :
        #bloqué sous un rocher
        sm = SousMarin(0,4,sample_ocean, 10,10)
        sm.shoot()
        assert sm.x == 0
        assert sm.y == 4
        assert sm.fuel == 10
        assert sm.oxygen == 10

        #pas de fuel
        sm = SousMarin(1,4,sample_ocean, 2,10)
        sm.shoot()
        assert sm.x == 1
        assert sm.y == 4
        assert sm.fuel == 2
        assert sm.oxygen == 10

        #pas d oxygene
        sm = SousMarin(1,4,sample_ocean, 10,1)
        sm.shoot()
        assert sm.x == 1
        assert sm.y == 4
        assert sm.fuel == 10
        assert sm.oxygen == 1

        #ok
        sm = SousMarin(1,4,sample_ocean, 10,10)
        sm.shoot()
        assert sm.x == 1
        assert sm.y == 4
        assert sm.fuel == 8
        assert sm.oxygen == 9
