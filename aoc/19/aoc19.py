#!/usr/bin/env python

import random
import numpy as np

## constants for indexing arrays (robots, resources)
ore=0
clay=1
obsidian=2
geode=3
resource_names = ["ore", "clay", "obsidian", "geode"]

def aoc19(robot_prices, start_resources, start_robots, num_rounds):
    res, robots, choices = run_strategy(robot_prices, start_resources, start_robots, num_rounds)
    print(f"Num choices this iteration: {np.prod(choices)}")

def strategy_random(feasible, my_robots, my_resources, robot_prices, round_idx):
    return random.choice(feasible)

def strategy_most_expensive(feasible, my_robots, my_resources, robot_prices, round_idx):
    """very bad: may get stuck forever"""
    if len(feasible) == 1:
        assert feasible[0] == 4
        return feasible[0]  # This is 4: wait.
    else:
        for robot_idx in [3,2,1,0]:
            if robot_idx in feasible:
                return robot_idx

def strategy_save_for_new_kind_of_robot(feasible, my_robots, my_resources, robot_prices, round_idx):
    """very bad: may get stuck forever"""
    if len(feasible) == 1:
        assert feasible[0] == 4
        return feasible[0]  # This is 4: wait.
    else:
        feasible_cp = feasible.copy()
        feasible_cp.remove(4)
        feasible_cp.sort(reverse=True)
        for robot_idx in feasible_cp:  # The 0 is not strictly needed, as we always have one.
            if my_robots[robot_idx] < 1:
                return robot_idx
        # If we did not buy any yet, we have all we can afford. Buy the most expensive one we can afford.
        for robot_idx in feasible_cp:  # The 0 is not strictly needed, as we always have one.
            return robot_idx

# TODO: strategy to check what is needed for next robot, how much we get of it per round, and buy robots
# that help to solve the problem asap.
def stategy_towards_next_robot(feasible, my_robots, my_resources, robot_prices, round_idx):
    """returns next action to take"""
    if len(feasible) == 1:
        assert feasible[0] == 4
        return feasible[0]  # This is 4: wait.
    else:
        next_wanted_robot = _get_next_wanted_robot(my_robots)
        return _get_best_step_towards_robot(next_wanted_robot, feasible, my_robots, my_resources, robot_prices, round_idx)

def _get_next_wanted_robot(my_robots):
    """Get next long-term wanted robot. This can be one we cannot currently afford, i.e. one that is not feasible."""
    next_wanted_robot = None
    for robot_idx in range(3):
        if my_robots[robot_idx] < 1: # we have no such robot
            next_wanted_robot = robot_idx
            print(f" * we want more robots of type {resource_names[next_wanted_robot]} because this is the highest one we do not own yet.")
            break
    if next_wanted_robot is None:
        next_wanted_robot = 3  # get more geode robots if we have all robots.
        print(f" * we want more robots of type {resource_names[next_wanted_robot]} because we have all types already.")
    return next_wanted_robot

def _get_best_step_towards_robot(next_wanted_robot, feasible, my_robots, my_resources, robot_prices, round_idx):
    if next_wanted_robot in feasible:
        return next_wanted_robot # We can simply buy it.
    else:
        resources_missing = _get_missing_resources(next_wanted_robot, my_resources, robot_prices)
        print(f" * we have the following resources: ore={my_resources[ore]}, clay={my_resources[clay]}, obsidian={my_resources[obsidian]}, geode={my_resources[geode]}.")
        print(f" * we want robot {resource_names[next_wanted_robot]}. Missing resources: {', '.join(str(f) for f in resources_missing)} (for: {', '.join(resource_names)})")
        resource_gain_per_round = _harvest_resources(None, my_robots, return_only_new=True)
        print(f" * Resource gain per round: {', '.join(str(f) for f in resource_gain_per_round)}")
        urgency = [0.0, 0.0, 0.0, 0.0]
        most_urgent_robot = None
        for idx in range(3):
            if resources_missing[idx] > 0:
                if resource_gain_per_round[idx] == 0:  # avoid div by zero. also we cannot afford the robot without getting another one first that harvests the required resource, so do that.
                    # in this case, we definitely need the other robot first, or we are not gonna get the resources.
                    # (TODO: we may have already ordered one that was not delivered yet?)
                    print(f" * resource {resource_names[idx]} is missing ({resources_missing[idx]} missing) and we earn none per round. setting robot {idx} as new next wanted (was {next_wanted_robot}). ")
                    most_urgent_robot = idx
                    break
                else:
                    urgency[idx] = resources_missing[idx] / resource_gain_per_round[idx]
        if most_urgent_robot is None:
            next_wanted_robot = np.argmax(urgency)  # Get the robot that produces the resource we need most urgently.
            print(f" * we earn all resources, but most urgent is: {next_wanted_robot}. getting that robot.")
            # NOTE: this is not neccessarily the best strategy: maybe we only need to wait 1 more round
            #       to afford the better one without buying another one first. but buying another one will
            #       still be better in the long term (unless there are not many rounds left.)
            #       We should compute how much waiting time we save by buying versus not buying the other robot first,
            #       and also consider simply waiting.
        else:
            next_wanted_robot = most_urgent_robot
        if next_wanted_robot in feasible:
            return next_wanted_robot
        elif next_wanted_robot == 0:
            return 4  # we want robot 0 and it is not feasible, all we can do is wait.
        else:
            return _get_best_step_towards_robot(next_wanted_robot, feasible, my_robots, my_resources, robot_prices, round_idx)

def run_strategy(robot_prices, start_resources, start_robots, num_rounds, strategy=stategy_towards_next_robot):
    my_resources = start_resources
    my_robots = start_robots
    num_choices_per_round = []
    for round_idx in range(num_rounds):
        print(f"At start of round {round_idx}, we have the following robots: ore={my_robots[ore]}, clay={my_robots[clay]}, obsidian={my_robots[obsidian]}, geode={my_robots[geode]}.")
        print(f"At start of round {round_idx}, we have the following resources: ore={my_resources[ore]}, clay={my_resources[clay]}, obsidian={my_resources[obsidian]}, geode={my_resources[geode]}.")
        feasible = _feasible_moves(my_resources, robot_prices)
        num_choices_per_round.append(len(feasible))
        move = strategy(feasible, my_robots, my_resources, robot_prices, round_idx)
        print(f"At round {round_idx}, performing move {_name_move(move)} ({len(feasible)} feasible moves: {', '.join(_name_move(f) for f in feasible)}).")
        print(f"At round {round_idx}, the following number of robots are working: ore={my_robots[ore]}, clay={my_robots[clay]}, obsidian={my_robots[obsidian]}, geode={my_robots[geode]}.")
        my_resources = _pay_for_move(my_resources, move, robot_prices)
        my_resources = _harvest_resources(my_resources, my_robots)
        my_robots = _get_next_rounds_robots(my_robots, move)
    return my_resources, my_robots, num_choices_per_round


def _get_missing_resources(wanted_robot, my_resources, robot_prices):
    costs = robot_prices[wanted_robot]
    miss = [0, 0, 0, 0]
    for res in range(3):
        if costs[res] > my_resources[res]:
            miss[res] = costs[res] - my_resources[res]
    return miss


def _name_move(move_int):
    assert move_int >= 0 and move_int <= 4, f"Move int must be between 0 and 4, received {move_int}."
    if move_int == 4:
        return "'Wait and save.'"
    else:
        return f"'Buy {resource_names[move_int]} robot.'"

def _pay_for_move(my_resources, move, robot_prices):
    if move == 4:
        return my_resources
    else:
        my_resources[0] -= robot_prices[move][0]
        my_resources[1] -= robot_prices[move][1]
        my_resources[2] -= robot_prices[move][2]
        my_resources[3] -= robot_prices[move][3] # No robot costs geodes, so no-op.
    for res_idx in range(3):
        if my_resources[res_idx] < 0:
            raise ValueError(f"After paying for move {_name_move(move)}, you have negative resources: infeasible move executed. ore={my_resources[ore]}, clay={my_resources[clay]}, obsidian={my_resources[obsidian]}, geode={my_resources[geode]}")
    return my_resources



def _get_next_rounds_robots(my_robots, move):
    if move == 4:
        return my_robots
    else:
        my_robots[move] += 1
        return my_robots

def _feasible_moves(my_resources, robot_prices):
    """Moves. 0..3 = buy respective robot. 4=wait (save up resources)"""
    feasible = [4]
    cbr = _can_buy_robots(my_resources, robot_prices)
    print(f" * Feasible moves: can buy robots: ore={cbr[ore]}, clay={cbr[clay]}, obsidian={cbr[obsidian]}, geode={cbr[geode]}")
    for idx, can in enumerate(cbr):
        if can:
            feasible.append(idx)
    return feasible

def _can_buy_robots(my_resources, robot_prices):
    """Which robots can be bought this round."""
    can_afford_robot = [False, False, False, False]
    for robot_idx, robot_price in enumerate(robot_prices):
        if my_resources[0] >= robot_price[0] and my_resources[1] >= robot_price[1] and my_resources[2] >= robot_price[2] and my_resources[3] >= robot_price[3]:
            can_afford_robot[robot_idx] = True
    return can_afford_robot


def _harvest_resources(current_resources, my_robots, return_only_new=False):
    """Compute what player earns in this round."""
    if return_only_new:
        return my_robots
    return [sum(x) for x in zip(current_resources, my_robots)]


if __name__ == "__main__":
    # outer array are the robots, inner arrays their respective mineral costs, both in following
    # order: ["ore", "clay", "obsidian", "geode"].
    blueprint1_robot_prices = [[4,0,0,0], [2,0,0,0], [3,14,0,0], [2,0,7,0]]
    blueprint2_robot_prices = [[2,0,0,0], [3,0,0,0], [3,8,0,0], [3,0,12,0]]
    start_resources = [0,0,0,0]
    start_robots = [1,0,0,0]
    num_rounds = 24
    aoc19(blueprint1_robot_prices, start_resources, start_robots, num_rounds)