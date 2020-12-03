import random

class State:
    all_states = []  # For keeping track of states as they're initialized.

    def __init__(self, name, payoff, choices=None):
        self.name = name
        self.payoff = payoff
        self.choices = choices
        self.value = 0
        self.all_states.append(self)

    def is_terminal_state(self):
        return self.choices == None

class Choice:
    def __init__(self, out_state, weight=1):
        self.out_state = out_state
        self.weight = weight

def run_baseline(start_state, cost_per_step):

    payoff_total = 0
    steps_taken = 0
    curr_state = start_state

    while not curr_state.is_terminal_state():

        # Pick a choice based on their weights. If all choices have the same,
        # weight, assume the choice is being made by the defender and pick the
        # choice with the highest payoff instead.
        choices = curr_state.choices
        weights = [final_choice.weight for final_choice in choices]
        all_weights_equal = all(w == weights[0] for w in weights)
        if all_weights_equal:
            final_choice = choices[0]
            for choice in choices:
                if choice.out_state.payoff >= final_choice.out_state.payoff:
                    final_choice = choice
        else:
            final_choice = random.choices(choices, weights)[0]
        next_state = final_choice.out_state

        payoff = next_state.payoff
        payoff_total += payoff
        steps_taken += 1
        curr_state = next_state

    cost_for_steps = cost_per_step * steps_taken
    payoff_total += cost_for_steps

    return payoff_total


def run_episode(start_state, cost_per_step):

    payoff_total = 0
    steps_taken = 0
    curr_state = start_state
    states_visited = {curr_state}

    while not curr_state.is_terminal_state():

        # Pick a choice based on their weights. If all choices have the same,
        # weight, the choice is random.
        choices = curr_state.choices
        weights = [final_choice.weight for final_choice in choices]
        final_choice = random.choices(choices, weights)[0]
        next_state = final_choice.out_state

        payoff = next_state.payoff
        payoff_total += payoff
        states_visited.add(next_state)
        steps_taken += 1
        curr_state = next_state

    cost_for_steps = cost_per_step * steps_taken
    payoff_total += cost_for_steps

    return payoff_total, states_visited


if __name__ == "__main__":

    revenue = 1000
    ransom = revenue * 0.03

    cost_attack = -revenue * 0.005
    cost_attack_after_investigation = -revenue * 0.001
    cost_disagree = -revenue * 0.002
    cost_expose_data_collaborate = -revenue * 0.006
    cost_expose_data_not_collaborate = -revenue * 0.008
    cost_kill_service = -revenue * 0.02
    cost_launch_investigation = -revenue * 0.01
    cost_not_pay = -revenue * 0.03
    cost_not_preparing = -revenue * 0.025
    cost_pay_25 = -ransom * 0.25
    cost_pay_50 = -ransom * 0.50
    cost_pay_75 = -ransom * 0.75
    cost_pay_full = -revenue * 0.03
    cost_preparing = -revenue * 0.015
    cost_replace_hardware = -revenue * 0.05
    cost_wait = -revenue * 0.008

    d39 = State("d39: pay 75%", cost_pay_75)
    d38 = State("d38: pay 50%", cost_pay_50)
    d37 = State("d37: ask 75%", 0, [Choice(d39)])
    d36 = State("d36: ask 50%", 0, [Choice(d38)])
    d35 = State("d35: negotiate", 0, [Choice(d36, 0.60), Choice(d37, 0.40)])
    d34 = State("d34: pay full amount", cost_pay_full)
    d33 = State("d33: kill service", cost_kill_service)
    d32 = State("d32: pay 75%", cost_pay_75)
    d31 = State("d31: pay 50%", cost_pay_50)
    d30 = State("d30: pay 50%", cost_pay_50)
    d29 = State("d29: pay 25%", cost_pay_25)
    d28 = State("d28: pay 75%", cost_pay_75)
    d27 = State("d27: pay 50%", cost_pay_50)
    d26 = State("d26: expose sensitive data not expecting negotiation", cost_expose_data_not_collaborate, [Choice(d33), Choice(d34), Choice(d35)])
    d25 = State("d25: negotiate", 0, [Choice(d31), Choice(d32)])
    d24 = State("d24: negotiate", 0, [Choice(d29), Choice(d30)])
    d23 = State("d23: lost control", 0)
    d22 = State("d22: ask 75%", 0, [Choice(d28)])
    d21 = State("d21: ask 50%", 0, [Choice(d27)])
    d20 = State("d20: prepare", cost_preparing)
    d19 = State("d19: not prepare", cost_not_preparing)
    d18 = State("d18: disagree", cost_disagree, [Choice(d25, 0.30), Choice(d26, 0.70)])
    d17 = State("d17: pay full amount", cost_pay_full)
    d16 = State("d16: wait", cost_wait, [Choice(d23, 0.10), Choice(d24, 0.90)])
    d15 = State("d15: negotiate", 0, [Choice(d21, 0.25), Choice(d22, 0.75)])
    d14 = State("d14: pay full amount", cost_pay_full)
    d13 = State("d13: kill service", cost_kill_service)
    d12 = State("d12: pay 75%", cost_pay_75)
    d11 = State("d11: pay 50%", cost_pay_50)
    d10 = State("d10: not attacked", 0, [Choice(d19), Choice(d20)])
    d9 = State("d9: attacked", cost_attack_after_investigation, [Choice(d16), Choice(d17), Choice(d18)])
    d8 = State("d8: expose sensitive data expecting negotiation", cost_expose_data_collaborate, [Choice(d13), Choice(d14), Choice(d15)])
    d7 = State("d7: negotiate", 0, [Choice(d11), Choice(d12)])
    d6 = State("d6: launch investigation", cost_launch_investigation, [Choice(d9, 0.55), Choice(d10, 0.45)])
    d5 = State("d5: replace hardware", cost_replace_hardware)
    d4 = State("d4: pay full amount", cost_pay_full)
    d3 = State("d3: not pay", cost_not_pay, [Choice(d7, 0.3), Choice(d8, 0.7)])
    d2 = State("d2: attack did not happen", 0, [Choice(d5), Choice(d6)])
    d1 = State("d1: attack happened", cost_attack, [Choice(d3), Choice(d4)])
    d0 = State("d0: vulnerability found", 0, [Choice(d1, 0.8), Choice(d2, 0.2)])

    LEARNING_RATE = 0.1
    N_EPISODES = 10000
    START_STATE = d0
    STEP_COST = -1

    # Run baseline.
    total_payoff = 0
    for i in range(N_EPISODES):
        total_payoff += run_baseline(START_STATE, STEP_COST)
    expected_payoff = total_payoff / N_EPISODES
    print(f"Baseline expected payoff = {expected_payoff}")

    # Run simulations.
    for i in range(N_EPISODES):
        episode_payoff, states_visited = run_episode(START_STATE, STEP_COST)
        for state in states_visited:
            state.value = state.value + LEARNING_RATE * (episode_payoff - state.value)

    # Print simulation parameters and terminal states' values.
    print(f"N_EPISODES={N_EPISODES}, LEARNING_RATE={LEARNING_RATE}, START_STATE=\"{START_STATE.name}\", STEP_COST={STEP_COST}")
    print("[state_id: state_name] = value (terminal states indicated with >)")
    print("*" * 25, "TERMINAL STATES")
    for state in State.all_states:
        if state.is_terminal_state():
            print(f"[{state.name}] = {float(state.value):.5}")
    print("*" * 25, "NON-TERMINAL STATES")
    for state in State.all_states:
        if not state.is_terminal_state():
            print(f"[{state.name}] = {float(state.value):.5}")    