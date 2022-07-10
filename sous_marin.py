
class SousMarin:
    def __init__(self, x, y, ocean, fuel=5, oxygen=5):
        self.x = x
        self.y = y
        self.ocean = ocean
        self.fuel = fuel
        self.oxygen = oxygen

    def get_report(self):
        return self.__dict__

    def radar(self):
        radar_output = {}
        if self.x == 0  :
            radar_output['backward'] = True
            radar_output['forward'] = self.ocean[self.y][self.x+1] == 1
        elif self.x == len(self.ocean[0])-1:
            radar_output['forward'] = True
            radar_output['backward'] = self.ocean[self.y][self.x-1] == 1
        else:
            radar_output['backward'] = self.ocean[self.y][self.x-1] == 1
            radar_output['forward'] = self.ocean[self.y][self.x+1] == 1

        if self.y == 0  :
            radar_output['up'] = True
            radar_output['down'] = self.ocean[self.y+1][self.x] == 1
        elif self.y == len(self.ocean)-1:
            radar_output['down'] = True
            radar_output['up'] = self.ocean[self.y-1][self.x] == 1
        else:
            radar_output['down'] = self.ocean[self.y+1][self.x] == 1
            radar_output['up'] = self.ocean[self.y-1][self.x] == 1

        return radar_output

    def is_in_danger(self):
        return {'fuel_danger' : self.fuel <= 1,
        'oxygen_danger' : self.oxygen <= 1 }

    def _is_in_failure(self):
        danger_status = self.is_in_danger()
        return danger_status['oxygen_danger'] or danger_status['fuel_danger']

    def step_up(self):
        if self.radar()['up'] or self._is_in_failure():
            return
        self.y -= 1
        self.fuel -= 1
        self.oxygen -= 1

    def step_down(self):
        if self.radar()['down'] or self._is_in_failure():
            return
        self.y += 1
        self.fuel -= 1
        self.oxygen -= 1

    def step_forward(self):
        if self.radar()['forward'] or self._is_in_failure():
            return
        self.x += 1
        self.fuel -= 1
        self.oxygen -= 1

    def step_backward(self):
        if self.radar()['backward'] or self._is_in_failure():
            return
        self.x -= 1
        self.fuel -= 1
        self.oxygen -= 1

    def move_down(self, n: int):
        y_initial = self.y
        if self.fuel < n+1 or self.oxygen < 2:
            return
        for i in range(n) :
            if self.radar()['down'] :
                self.y = y_initial
                return
            self.y += 1

        self.fuel -= n
        self.oxygen -= 1


    def move_up(self, n: int):
        y_initial = self.y
        if self.fuel < n+1 or self.oxygen < 2:
            return
        for i in range(n) :
            if self.radar()['up'] :
                self.y = y_initial
                return
            self.y -= 1

        self.fuel -= n
        self.oxygen -= 1

    def move_forward(self, n: int):
        x_initial = self.x
        if self.fuel < n+1 or self.oxygen < 2:
            return
        for i in range(n) :
            if self.radar()['forward'] :
                self.x = x_initial
                return
            self.x += 1

        self.fuel -= n
        self.oxygen -= 1

    def move_backward(self, n: int):
        x_initial = self.x
        if self.fuel < n+1 or self.oxygen < 2:
            return
        for i in range(n) :
            if self.radar()['backward'] :
                self.x = x_initial
                return
            self.x -= 1

        self.fuel -= n
        self.oxygen -= 1

    def shoot(self):
        '''conso 2 fuel 1 oxy'''
        if self.fuel <= 2 or self.oxygen <= 1 :
            return
        for i in range(self.y) :
            if self.ocean[i][self.x] :
                return
        self.fuel -= 2
        self.oxygen -= 1


