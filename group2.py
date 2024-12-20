from copy import deepcopy

#Heuristic function to evaluate a given board
def evaluate(self, board):
    score = 0
    num = 0
    center_control_bonus = 2

    for i in range(8):
        for j in range(8):
            squarePiece = board.getSquare(i, j).squarePiece
            if squarePiece is not None:
                num += 1
                value = 0

                #8 points for king, 4 for normal
                if squarePiece.king:
                    value = 8
                else:
                    value = 4

                #incentive to move forward(if not king)
                if squarePiece.color == self.eval_color:
                    value += (7 - j) if not squarePiece.king else 0
                else:
                    value -= (7 - j) if not squarePiece.king else 0

                #extra points for centre
                if 2 <= i <= 5 and 2 <= j <= 5:
                    value += center_control_bonus if squarePiece.color == self.eval_color else -center_control_bonus

                score += value if squarePiece.color == self.eval_color else -value

    #adjust inflaton
    if num > 0:
        score /= num

    #repeat penalty
    board_hash = hash(str(board))
    if hasattr(self, "move_history") and board_hash in self.move_history:
        score -= 50  # Apply a penalty for revisiting a previous state

    return score


def minimax(self, board, depth, max_player, alpha, beta):
    if depth == 0 or self.game.endGame:
        return evaluate(self, board)

    possible_moves = self.getPossibleMoves(board)

    if not possible_moves:
        return evaluate(self, board)

    if max_player:
        max_eval = float('-inf')
        for move in possible_moves:
            current = (move[0], move[1])
            for choice in move[2]:
                new_board = deepcopy(board)
                self.move(current, choice, new_board)
                eval_value = minimax(self, new_board, depth - 1, False, alpha, beta)
                max_eval = max(max_eval, eval_value)
                alpha = max(alpha, eval_value)
                if beta <= alpha:
                    break  #beta cutoff
        return max_eval
    else:
        min_eval = float('inf')
        for move in possible_moves:
            current = (move[0], move[1])
            for choice in move[2]:
                new_board = deepcopy(board)
                self.move(current, choice, new_board)
                eval_value = minimax(self, new_board, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval_value)
                beta = min(beta, eval_value)
                if beta <= alpha:
                    break  #alpha cutoff
        return min_eval



def group2(self, board):
    if not hasattr(self, "move_history"):
        self.move_history = []

    if self.game.endGame:
        return (0, 0), (0, 0)

    best_value = float('-inf')
    best_move = None
    best_choice = None

    possible_moves = self.getPossibleMoves(board)

    if not possible_moves:
        self.game.end_turn()
        return (0, 0), (0, 0)

    for move in possible_moves:
        current = (move[0], move[1])
        for choice in move[2]:
            new_board = deepcopy(board)
            self.move(current, choice, new_board)

            move_value = minimax(self, new_board, self.depth, False, float('-inf'), float('inf'))

            if move_value > best_value:
                best_value = move_value
                best_move = current
                best_choice = choice

    board_hash = hash(str(board))
    self.move_history.append(board_hash)
    if len(self.move_history) > 10:
        self.move_history.pop(0)

    return best_move, best_choice
