# agent.py

import numpy as np

class QLearningAgent:
    def __init__(self, board_size=15):
        self.q_values = {}
        self.learning_rate = 0.1
        self.discount_factor = 0.9
        self.epsilon = 0.1
        self.BOARD_SIZE = board_size

    def get_action(self, state):
        possible_actions = self.get_possible_actions(state)

        if len(possible_actions) > 0:
            # 가능한 모든 액션 중에서 무작위로 액션 선택
            chosen_action = possible_actions[np.random.choice(len(possible_actions))]
            return chosen_action
        else:
            # 가능한 액션이 없으면 None을 반환하거나 필요한 경우 이 상황을 처리
            return None

    def get_possible_actions(self, state):
        state_2d = np.array(state).reshape((self.BOARD_SIZE, self.BOARD_SIZE))
        empty_positions = [(i, j) for i in range(self.BOARD_SIZE) for j in range(self.BOARD_SIZE) if state_2d[i, j] == 0]
        return empty_positions

    def get_q_value(self, state, action):
        state_str = str(state)
        action_tuple = tuple(action)
        return self.q_values.get((state_str, action_tuple), 0.0)

    def update_q_values(self, state, action, reward):
        current_q_value = self.get_q_value(state, action)
        max_future_value = max(
            [self.get_q_value(state, next_action) for next_action in self.get_possible_actions(state)])

        new_q_value = (1 - self.learning_rate) * current_q_value + self.learning_rate * (
                reward + self.discount_factor * max_future_value)

        state_str = str(state)
        action_tuple = tuple(action)
        self.q_values[(state_str, action_tuple)] = new_q_value
        print(f"Updated Q-value for state: {state}, action: {action}, new Q-value: {new_q_value}")

    def get_state_representation(self, state):
        return tuple(map(int, state))

    def load_q_values(self, file_path):
        try:
            self.q_values = np.load(file_path, allow_pickle=True).item()
            print("Q-values 로드 성공.")
        except Exception as e:
            print(f"Q-values 로드 중 오류 발생: {e}")

    def save_q_values(self, file_path):
        try:
            np.save(file_path, self.q_values)
            print("Q-values 저장 성공.")
        except Exception as e:
            print(f"Q-values 저장 중 오류 발생: {e}")
