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

        # Load the Q-values from a file
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
                            self.agent.update_q_values(state, action, self.calculate_reward(player))
                            self.make_computer_move()
                            if self.check_win(row, col, player):
                                game_over = True
                                winner = "컴퓨터" if player == self.BLACK else "흰 돌"
                                self.show_alert(f"{winner}이 승리하였습니다.")
                            elif self.check_draw():
                                game_over = True
                                self.show_alert("무승부입니다.")

            pygame.display.update()
            clock.tick(60)

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
        return tuple(np.array(self.board).flatten())

    def check_draw(self):
        for i in range(self.BOARD_SIZE):
            for j in range(self.BOARD_SIZE):
                if self.board[i][j] == self.EMPTY:
                    return False
        return True

    def show_alert(self, message):
        root = tk.Tk()
        root.withdraw()  # Hide the default window
        messagebox.showinfo("축하합니다!", message)

# Create an instance of the Q-learning agent
q_learning_agent = QLearningAgent()

# Create an instance of the game with RL integration
game_rl = OmokRL(q_learning_agent)
game_rl.play_game_with_rl()
