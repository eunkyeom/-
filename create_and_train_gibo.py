# create_and_train_gibo.py

import numpy as np
from agent import QLearningAgent

def create_and_train_gibo():
    # 명시적으로 오목 게임판 크기를 지정하여 Q-learning 에이전트 초기화
    agent = QLearningAgent(board_size=15)
    game_states = []

    for _ in range(100):
        current_state = generate_random_board().flatten()  # 상태를 펼치기
        game_states.append(current_state)

    game_states_array = np.array(game_states)

    file_path = "game_states.npy"
    np.save(file_path, game_states_array)

    loaded_game_states = np.load(file_path)

    # 게임 상태 데이터 출력
    with np.printoptions(threshold=np.inf):
        print("로드된 게임 상태:")
        print(loaded_game_states)

    for state in game_states:
        action = agent.get_action(state)
        reward = 0.5  # reward를 적절한 값으로 설정해야 합니다.
        if action is not None:  # 액션이 None이 아닌 경우에만 업데이트
            agent.update_q_values(state, action, reward)  # reward 전달 추가

    agent.save_q_values("q_values.npy")

def generate_random_board():
    return np.random.choice([-1, 0, 1], size=(15, 15), p=[0.3, 0.4, 0.3])

if __name__ == "__main__":
    create_and_train_gibo()
