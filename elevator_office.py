#!/usr/bin/env python

DIRECTION_DOWN = -1
DIRECTION_NONE = 0
DIRECTION_UP = 1


class HardwareElevator(object):
    def move_up(self):
        pass

    def move_down(self):
        pass

    def stop_and_open_doors(self):
        pass

    def set_doors_closed_callback(self, callback):
        pass

    def set_before_floor_callback(self, callback):
        pass

    def get_current_floor(self):
        return 1

    def get_current_direction(self):
        return DIRECTION_UP

class Elevator(object):
    def __init__(self):
        self.hw = HardwareElevator()
        self.hw.set_doors_closed_callback(self._doors_closed)
        self.hw.set_before_floor_callback(self._before_floor)
        self.floors = {
            DIRECTION_UP: set(),
            DIRECTION_DOWN: set(),
            DIRECTION_NONE: None
        }
        self.moving = {
            DIRECTION_UP: self.hw.move_up,
            DIRECTION_DOWN: self.hw.move_down,
            DIRECTION_NONE: None
        }
        self.direction = self.hw.get_current_direction()

    def _doors_closed(self):
        if !self.floors[self.direction]:
            self.direction = -self.direction
        self.moving[self.direction]()

        # Write your code here

    def _before_floor(self):
        current_floor = self.hw.get_current_floor()
        temp_direction = self.direction
        direction_up_floor = False
        direction_down_floor = False

        try:
            direction_up_floor = (current_floor in
               self.floors[DIRECTION_UP] and
               current_floor <= max(self.floors[DIRECTION_UP]))
            direction_down_floor = (current_floor in
               self.floors[DIRECTION_UP] and
               current_floor >= min(self.floors[DIRECTION_DOWN]))
        except ValueError:
                pass

        if direction_up_floor:
            self.floors[DIRECTION_UP].pop(current_floor)
        elif: direction_down_floor:
            self.floors[DIRECTION_DOWN].pop(current_floor)
        else:
            self.directin = DIRECTION_NONE
            return
        self.hw.stop_and_open_doors()
        # Write your code here

    def floor_button_pressed(self, floor, direction):

        check_direction = self.check_floor_direction(floor, direction)
        if check_direction:
            self.floors[direction].add(floor)
        else:
            direction = -direction
            self.floors[direction].add(floor)
        if self.direction == DIRECTION_NONE:
            self.direction = direction
            self.moving[direction]()
        # Write your code here

    def cabin_button_pressed(self, floor):
        current_floor = self.hw.get_current_floor()
        if floor > current_floor:
            self.floors[DIRECTION_UP].add(floor)
        else:
            self.floors[DIRECTION_DOWN].add(floor)

    def check_floor_direction(self, floor, direction):
        current_floor = self.hw.get_current_floor()
        if direction == DIRECTION_UP:
            return floor > current_floor
        elif direction == DIRECTION_DOWN:
            return floor < current_floor
