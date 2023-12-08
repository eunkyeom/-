# create_and_train_gibo.py

import numpy as np
from agent import QLearningAgent

def create_and_train_gibo():
    agent = QLearningAgent()
    game_states = []

    for _ in range(1000):

        # 게임이 끝난 후 현재의 게임 상태를 game_states 추가
        current_state = agent.get_state_representation(np.zeros((15, 15)))
        game_states.append(current_state)

    # 학습을 위해 수집한 게임 상태들을 사용하여 에이전트 업데이트
    for state in game_states:
        action = agent.get_action(state)
        reward = 0.5  # 적절한 보상 값을 설정하세요.
        agent.update_q_values(state, action, reward)

    # 학습된 Q-values를 파일로 저장
    agent.save_q_values("q_values.npy")

if __name__ == "__main__":
    create_and_train_gibo()
