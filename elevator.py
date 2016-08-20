#!/usr/bin/python3
from bisect import bisect, insort
from typing import Callable
from time import sleep

DIRECTION = {
    0: "up",
    1: "down",
}
ELEVATOR_DONT_MOVE = 'Elevator %d don`t move'
ELEVATOR_MOVE = 'Elevator %d move %s'
ELEVATOR_STOP = 'Elevator %d stop at %d floor'


class Elevator():

    direction = 0
    current_floor = 0
    target_floor_num = 0
    is_move = False

    def __init__(self,
                 e_id: int,
                 pickup: Callable[[int, int], None],
                 remove: Callable[[int, int], None],
                 *ar, **kw) -> None:
        self.e_id = e_id
        # Use pickup func from ElevatorSystem to set new goal floor inside elevator
        self.pickup = pickup
        self.remove = remove

    def move(self) -> None:
        '''
        Elevator moving depending on direction and target floor
        '''
        self._close_door()
        self.is_move = True
        while self.is_move:
            self.is_move = False

            if self.direction == 0:
                if self.current_floor < self.target_floor_num:
                    print(ELEVATOR_MOVE % (self.e_id, DIRECTION[self.direction]))
                    self.is_move = True
                    sleep(5)
                    self.current_floor += 1
                elif self.current_floor == self.target_floor_num:
                    self.remove(self.e_id, self.current_floor)
                    print(ELEVATOR_STOP % (self.e_id, self.current_floor))
                else:
                    print(ELEVATOR_DONT_MOVE % self.e_id)
            else:
                if self.current_floor > self.target_floor_num:
                    print(ELEVATOR_MOVE % (self.e_id, DIRECTION[self.direction]))
                    self.is_move = True
                    sleep(5)
                    self.current_floor -= 1
                elif self.current_floor == self.target_floor_num:
                    self.remove(self.e_id, self.current_floor)
                    print(ELEVATOR_STOP % (self.e_id, self.current_floor))
                else:
                    print(ELEVATOR_DONT_MOVE % self.e_id)
        self._open_door()

    def change_target(self, direction: int, floor: int) -> None:
        self.direction = direction
        self.target_floor_num = floor

    def _open_door(self) -> None:
        '''
        Send signal for opening door
        '''
        print('Elevator %d open door on %d floor' % (self.e_id, self.current_floor))

    def _close_door(self) -> None:
        '''
        Send signal for closing door
        '''
        print('Elevator %d close door on %d floor' % (self.e_id, self.current_floor))


class ElevatorSystem():
    '''
    System for manipulating several elevators
    '''
    elevators = {}
    goal_floors = {}

    def __init__(self, elevator_number: int, floor_number: int, *ar, **kw) -> None:
        self.elevators = {i: Elevator(i, self.pickup, self.remove_goal_floor) for i in range(elevator_number)}
        self.goal_floors = {i: [] for i in range(elevator_number)}
        self.last_floor = floor_number

    def status(self, e_id: int) -> (int, int):
        '''
        Return status of elevator
        Args:
            e_id (int): Elevator Id.

        Returns:
            int: Current floor
            int: Target floor
        '''
        if 0 <= e_id <= len(self.elevators):
            el = self.elevators[e_id]
            return el.current_floor, el.target_floor_num

    def pickup(self, e_id: int, floor_num: int) -> None:
        '''
        Set new goal floor outside elevator
        Args:
            e_id (int): Elevator Id.
            e_id (int): Goal floor number.

        Returns:
            None
        '''
        if 0 <= floor_num <= self.last_floor:

            # git list with goal floors for current elevator
            g_list = self.goal_floors[e_id]
            # insert floor into sorted list floor
            insort(g_list, floor_num)
            # get elevator
            el = self.elevators[e_id]
            # index of current floors in sorted goal list
            num = bisect(g_list, el.current_floor)

            # check if elevator higher than last goal floor
            if num >= len(g_list):
                el.change_target(1, g_list[-1])
            # check if elevator lower than first goal floor
            elif num == 0:
                el.change_target(0, g_list[0])
            else:
                if el.current_floor < g_list[num]:
                    el.target_floor_num = g_list[num]
                elif el.current_floor > g_list[num]:
                    el.target_floor_num = g_list[num - 1]

            if not el.is_move:
                el.move()
        else:
            return Exception('Wrong floor')

    def remove_goal_floor(self, e_id: int, floor: int) -> None:
        '''
        Remove floor from goal list for elevator
        Args:
            e_id (int): Elevator Id.
            floor (int): Used goal floor.

        Returns:
            None
        '''
        g_list = self.goal_floors[e_id]
        if floor in g_list:
            g_list.remove(floor)

    def __str__(self) -> str:
        return '%d elevators for %d floors' % (len(self.elevators), self.last_floor)
