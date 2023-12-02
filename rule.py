class Rule():
    def __init__(self):
        self.BOARD_SIZE = 15
        self.EMPTY = 0
        self.BLACK = 1
        self.WHITE = 2
        self.board = [[self.EMPTY] * self.BOARD_SIZE for _ in range(self.BOARD_SIZE)]
        self.directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    def check_win(self, x, y, player):
        print(player)  # 디버깅용 출력

        for dx, dy in self.directions:
            count = 1

            # 현재 위치를 기준으로 양 방향으로 이동
            for direction in [1, -1]:
                nx, ny = x, y

                # 양 방향으로 이동하면서 연속된 돌의 개수 확인
                while True:
                    nx += dx * direction
                    ny += dy * direction
                    if 0 <= nx < self.BOARD_SIZE and 0 <= ny < self.BOARD_SIZE and self.board[nx][ny] == player:
                        count += 1
                    else:
                        break

            # 연속된 돌이 5개면 승리
            if count >= 5:
                return True

        return False
