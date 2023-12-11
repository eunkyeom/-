# main.py

from rule import Rule
import pygame
import draw
import tkinter as tk
from tkinter import messagebox
from agent import QLearningAgent
import numpy as np

class OmokRL(Rule):
    def __init__(self, agent):
        super().__init__()
        self.agent = agent
        self.last_move = None

    def play_game_with_rl(self):
        pygame.init()
        clock = pygame.time.Clock()

        draw.init_board(self.BOARD_SIZE)

        player = self.BLACK
        game_over = False

        # Q-values 파일에서 Q-values 로드
        self.agent.load_q_values("q_values.npy")

        while not game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    x, y = pygame.mouse.get_pos()
                    row, col = draw.get_clicked_position(x, y)
                    if row is not None and col is not None and self.board[row][col] == self.EMPTY:
                        self.board[row][col] = player
                        draw.draw_stone(row, col, player)
                        self.last_move = (row, col)
                        if self.check_win(row, col, player):
                            game_over = True
                            winner = "검은 돌" if player == self.BLACK else "흰 돌"
                            self.show_alert(f"{winner}이 승리하였습니다.")
                        elif self.check_draw():
                            game_over = True
                            self.show_alert("무승부입니다.")
                        else:
                            state = self.get_state_representation()
                            action = self.agent.get_action(state)
                            reward = self.calculate_reward(player)
                            self.make_computer_move()
                            if self.check_win(row, col, player):
                                game_over = True
                                winner = "컴퓨터" if player == self.BLACK else "흰 돌"
                                self.show_alert(f"{winner}이 승리하였습니다.")
                            elif self.check_draw():
                                game_over = True
                                self.show_alert("무승부입니다.")
                            self.agent.update_q_values(state, action, reward)

            pygame.display.update()
            clock.tick(60)

        # 게임이 종료된 후, Q-values 출력
        self.print_q_values()
        # 게임이 종료된 후, Q-values 저장
        self.agent.save_q_values("q_values.npy")

        pygame.quit()

    def calculate_reward(self, player):
        if self.check_win(*self.last_move, player):
            return 1.0
        elif self.check_draw():
            return 0.5
        else:
            return 0.0

    def make_computer_move(self):
        state = self.get_state_representation()
        action = self.agent.get_action(state)

        if isinstance(action, tuple):
            row, col = int(action[0]), int(action[1])
        elif isinstance(action, np.ndarray) and action.size == 2:
            row, col = int(action[0]), int(action[1])
        else:
            raise ValueError(f"잘못된 액션: {action}")

        if self.board[row][col] == self.EMPTY:
            self.board[row][col] = self.WHITE
            draw.draw_stone(row, col, self.WHITE)

    def get_state_representation(self):
        # 튜플을 NumPy 배열로 변환
        return np.array(self.board).flatten()

    def check_draw(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.EMPTY:
                    return False
        return True

    def show_alert(self, message):
        root = tk.Tk()
        root.withdraw()  # 기본 창 숨기기
        messagebox.showinfo("축하합니다!", message)

    def print_q_values(self):
        print("게임 종료 후 Q-values:")
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                state = self.get_state_representation()
                action = (i, j)
                q_value = self.agent.get_q_value(state, action)
                print(f"위치 ({i}, {j})의 Q-value: {q_value}")

# Q-learning 에이전트의 인스턴스 생성
q_learning_agent = QLearningAgent()

# RL 통합 게임의 인스턴스 생성
game_rl = OmokRL(q_learning_agent)
game_rl.play_game_with_rl()
