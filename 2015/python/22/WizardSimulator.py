from dataclasses import dataclass, replace


@dataclass
class State:
    player_hp: int
    player_mana: int

    boss_hp: int
    boss_dmg: int

    mana_spent: int = 0
    is_valid: bool = True
    player_won: bool = False

    shield_rounds_left: int = 0
    poison_rounds_left: int = 0
    recharge_rounds_left: int = 0
    
    SHIELD_ARMOR: int = 7
    POISON_DMG: int = 3
    RECHARGE_MANA: int = 101

    #
    # Spells
    #     
    def magic_missile(self):
        self.spend_mana(53)
        self.change_boss_hp(-4)

    def drain(self):
        self.spend_mana(73)
        self.change_boss_hp(-2)
        self.change_player_hp(2)

    def shield(self):
        self.spend_mana(113)
        self.shield_rounds_left = 7

    def poison(self):
        self.spend_mana(173)
        self.poison_rounds_left = 6

    def recharge(self):
        self.spend_mana(223)
        self.recharge_rounds_left = 5

    #
    # Helpers
    #
    def __str__(self):
        # string = f"(HP{self.player_hp}, M{self.player_mana} - S{self.shield_rounds_left}, R{self.recharge_rounds_left}), "
        # string += f"(HP{self.boss_hp} - P{self.poison_rounds_left}), "
        # string += "active" if self.is_valid else ("Player won!" if self.player_won else "Boss won!")
        # return string
        return str((self.player_hp, self.player_mana, self.boss_hp, self.shield_rounds_left, self.poison_rounds_left, self.recharge_rounds_left))

    def __hash__(self):
        return hash((self.player_hp, self.player_mana, self.boss_hp, self.shield_rounds_left, self.poison_rounds_left, self.recharge_rounds_left))

    def spend_mana(self, mana):
        self.player_mana -= mana
        self.mana_spent += mana

    def change_player_hp(self, amount):
        self.player_hp += amount
        
        if self.player_hp <= 0:
            self.is_valid = False
            self.player_won = False

    def change_boss_hp(self, amount):
        self.boss_hp += amount

        if self.boss_hp <= 0:
            self.is_valid = False
            self.player_won = True

    #
    # Turns
    #
    def passive_turn(self):
        if self.poison_rounds_left > 0:
            self.change_boss_hp(-self.POISON_DMG)
            self.poison_rounds_left -= 1

        if self.shield_rounds_left > 0:
            self.shield_rounds_left -= 0

        if self.recharge_rounds_left > 0:
            self.player_mana += 101
            self.recharge_rounds_left -= 1

    def boss_turn(self):
        self.passive_turn()
        
        armor = 7 if self.shield_rounds_left > 0 else 0
        self.change_player_hp(-(self.boss_dmg - armor))

def round(state):
    state.passive_turn()
    if not state.is_valid:
        return [state]
    
    states = list()
    actions = [(53, State.magic_missile), (73, State.drain), (113, State.shield), (173, State.poison), (229, State.recharge)]
    for mana_cost, action in actions:
        if state.player_mana >= mana_cost:
            new_state = replace(state)
            action(new_state)
            states.append(new_state)

    for new_state in states:
        if new_state.is_valid:
            new_state.boss_turn()

    return states


def get_best_equivalent_state(states):
    return sorted(states, key=lambda item: item.mana_spent)[0]


def get_best_states(states):    
    equivalent_states = dict()
    for state in states:
        if state in equivalent_states:
            equivalent_states[state].append(state)

        else:
            equivalent_states[state] = [state]

    best_states = [get_best_equivalent_state(states) for states in equivalent_states.values()]

    return best_states


def game(initial_state):
    states = [initial_state]

    best_player_won_state = State(0, 0, 0, 0, 1e9)
    while states:
        new_states = list()
        for state in states:
            new_states += round(state)

        next_states = get_best_states([state for state in new_states if state.is_valid])


        player_won_states = [state for state in new_states if (not state.is_valid and state.player_won)]
        if player_won_states:
            best_new_player_won_state = sorted(player_won_states, key=lambda item: item.mana_spent)[0]
            best_player_won_state = best_new_player_won_state if best_new_player_won_state.mana_spent < best_player_won_state.mana_spent else best_player_won_state

        min_active_state_mana = min([state.mana_spent for state in next_states])
        if min_active_state_mana > best_player_won_state.mana_spent:
            break

        print(len(states), len(new_states), len(next_states))
        print(best_player_won_state.mana_spent)
        
        states = next_states

    print(best_player_won_state, best_player_won_state.mana_spent)


def part_one():
    # state = State(10, 250, 13, 8)
    state = State(50, 500, 55, 8)
    game(state)


def part_two():
    pass


if __name__ == "__main__":
    part_one()
    part_two()
    