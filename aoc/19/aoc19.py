#!/usr/bin/env python

import random
import numpy as np

## constants for indexing arrays (robots, resources)
ore=0
clay=1
obsidian=2
geode=3


def aoc19(robot_prices, start_resources, start_robots, num_rounds):
    res, robots, choices = simulate_random_strategy(robot_prices, start_resources, start_robots, num_rounds)
    print(f"Num choices this iteration: {np.prod(choices)}")

def strategy_random(feasible, my_robots):
    return random.choice(feasible)

def strategy_most_expensive(feasible, my_robots):
    """very bad: may get stuck forever"""
    if len(feasible) == 1:
        return feasible[0]  # This is 4: wait.
    else:
        for robot_idx in [3,2,1,0]:
            if robot_idx in feasible:
                return robot_idx

def strategy_save_for_new_kind_of_robot(feasible, my_robots):
    """very bad: may get stuck forever"""
    if len(feasible) == 1:
        return feasible[0]  # This is 4: wait.
    else:
        feasible_cp = feasible.copy()
        feasible_cp.remove(4)
        feasible_cp.sort(reverse=True)
        for robot_idx in feasible_cp:  # The 0 is not strictly needed, as we always have one.
            if my_robots[robot_idx] < 1:
                return robot_idx
        # If we did not buy any yet, we have all. Buy the most expensive one we can afford.
        for robot_idx in feasible_cp:  # The 0 is not strictly needed, as we always have one.
            return robot_idx

# TODO: strategy to check what is needed for next robot, how much we get of it per round, and buy robots
# that help to solve the problem asap.

def simulate_random_strategy(robot_prices, start_resources, start_robots, num_rounds, strategy=strategy_save_for_new_kind_of_robot):
    my_resources = start_resources
    my_robots = start_robots
    num_choices_per_round = []
    for round_idx in range(num_rounds):
        print(f"At start of round {round_idx}, we have the following robots: ore={my_robots[ore]}, clay={my_robots[clay]}, obsidian={my_robots[obsidian]}, geode={my_robots[geode]}.")
        print(f"At start of round {round_idx}, we have the following resources: ore={my_resources[ore]}, clay={my_resources[clay]}, obsidian={my_resources[obsidian]}, geode={my_resources[geode]}.")
        feasible = feasible_moves(my_resources, robot_prices)
        num_choices_per_round.append(len(feasible))
        move = strategy(feasible, my_robots)
        print(f"At round {round_idx}, performing move {move} ({len(feasible)} feasible moves: {', '.join(str(f) for f in feasible)}).")
        print(f"At round {round_idx}, the following number of robots are working: ore={my_robots[ore]}, clay={my_robots[clay]}, obsidian={my_robots[obsidian]}, geode={my_robots[geode]}.")
        my_resources = pay_for_move(my_resources, move, robot_prices)
        my_resources = get_rounds_resources(my_resources, my_robots)
        my_robots = get_next_rounds_robots(my_robots, move)
    return my_resources, my_robots, num_choices_per_round

def pay_for_move(my_resources, move, robot_prices):
    if move == 4:
        return my_resources
    else:
        my_resources[0] -= robot_prices[move][0]
        my_resources[1] -= robot_prices[move][1]
        my_resources[2] -= robot_prices[move][2]
        my_resources[3] -= robot_prices[move][3] # No robot costs geodes, so no-op.
    return my_resources



def get_next_rounds_robots(my_robots, move):
    if move == 4:
        return my_robots
    else:
        my_robots[move] += 1
        return my_robots

def feasible_moves(my_resources, robot_prices):
    """Moves. 0..3 = buy respective robot. 4=wait (save up resources)"""
    feasible = [4]
    cbr = can_buy_robots(my_resources, robot_prices)
    print(f" * Feasible moves: can buy robots: ore={cbr[ore]}, clay={cbr[clay]}, obsidian={cbr[obsidian]}, geode={cbr[geode]}")
    for idx, can in enumerate(cbr):
        if can:
            feasible.append(idx)
    return feasible

def can_buy_robots(my_resources, robot_prices):
    """Which robots can be bought this round."""
    can_afford_robot = [False, False, False, False]
    for robot_idx, robot_price in enumerate(robot_prices):
        if my_resources[0] >= robot_price[0] and my_resources[1] >= robot_price[1] and my_resources[2] >= robot_price[2] and my_resources[3] >= robot_price[3]:
            can_afford_robot[robot_idx] = True
    return can_afford_robot


def get_rounds_resources(current_resources, my_robots):
    """Compute what player earns in this round."""
    return [sum(x) for x in zip(current_resources, my_robots)]


if __name__ == "__main__":
    robot_prices = [[4,0,0,0], [2,0,0,0], [3,14,0,0], [2,0,7,0]]
    start_resources = [0,0,0,0]
    start_robots = [1,0,0,0]
    num_rounds = 24
    aoc19(robot_prices, start_resources, start_robots, num_rounds)