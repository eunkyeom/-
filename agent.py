# agent.py

import numpy as np


class QLearningAgent:
    def __init__(self, learning_rate=0.1, discount_factor=0.9, exploration_prob=0.2):
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_prob = exploration_prob
        self.q_values = {}

    def get_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) > 0:
            # Choose a random action among all possible actions
            chosen_action = possible_actions[np.random.choice(len(possible_actions))]
            print(f"Chosen action: {chosen_action}")
            return chosen_action
        else:
            # No possible actions, return None or handle this case as needed
            return None

    def get_possible_actions(self, state):
        # Flatten the state representation and find indices of empty positions
        empty_positions = [index for index, value in enumerate(state) if value == 0]

        # Convert the flattened indices to (row, col) format
        possible_actions = [(index // int(np.sqrt(len(state))), index % int(np.sqrt(len(state)))) for index in
                            empty_positions]

        # Return as a 1-dimensional NumPy array
        return np.array(possible_actions)

    def get_q_value(self, state, action):
        action_tuple = tuple(action)
        return self.q_values.get((state, action_tuple), 0.0)

    def update_q_values(self, state, action, reward):
        # Update Q-values based on the observed state, action, and reward
        current_q_value = self.get_q_value(state, action)

        # Estimate the best possible future value
        max_future_value = max(
            [self.get_q_value(state, next_action) for next_action in self.get_possible_actions(state)])

        # Q-value update using the Bellman equation
        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (
                    reward + self.discount_factor * max_future_value)

        # Update the Q-value table
        action_tuple = tuple(action)
        self.q_values[(state, action_tuple)] = new_q_value