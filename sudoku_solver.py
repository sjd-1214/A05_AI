import sys

class SudokuCSP:
    def __init__(self, board):
        self.variables = [(r, c) for r in range(9) for c in range(9)]
        self.domains = {}
        for r in range(9):
            for c in range(9):
                if board[r][c] != 0:
                    self.domains[(r, c)] = [board[r][c]]
                else:
                    self.domains[(r, c)] = list(range(1, 10))
        
        self.neighbors = {v: self._get_neighbors(v) for v in self.variables}
        self.backtrack_calls = 0
        self.failures = 0

    def _get_neighbors(self, var):
        r, c = var
        neighbors = set()
        for i in range(9):
            if i != c: neighbors.add((r, i))
            if i != r: neighbors.add((i, c))
        br, bc = (r // 3) * 3, (c // 3) * 3
        for i in range(br, br + 3):
            for j in range(bc, bc + 3):
                if (i, j) != (r, c):
                    neighbors.add((i, j))
        return neighbors

    def ac3(self, queue=None):
        if queue is None:
            queue = [(xi, xj) for xi in self.variables for xj in self.neighbors[xi]]
        
        # Use a set for faster lookup in queue
        q_set = set(queue)
        # Use a list for the actual queue to maintain order (though order isn't strictly necessary)
        # But we'll use a simple list for simplicity.
        idx = 0
        while idx < len(queue):
            (xi, xj) = queue[idx]
            idx += 1
            q_set.remove((xi, xj))
            if self.revise(xi, xj):
                if not self.domains[xi]:
                    return False
                for xk in self.neighbors[xi]:
                    if xk != xj:
                        if (xk, xi) not in q_set:
                            queue.append((xk, xi))
                            q_set.add((xk, xi))
        return True

    def revise(self, xi, xj):
        revised = False
        # In Sudoku, xi != xj
        # x is removed from D(xi) if there's no y in D(xj) such that x != y.
        # This only happens if D(xj) has only one element {x}.
        if len(self.domains[xj]) == 1:
            val = self.domains[xj][0]
            if val in self.domains[xi]:
                self.domains[xi] = [v for v in self.domains[xi] if v != val]
                revised = True
        return revised

    def solve(self):
        if not self.ac3():
            return None
        return self.backtrack()

    def backtrack(self):
        self.backtrack_calls += 1
        
        # Check if complete
        unassigned = [v for v in self.variables if len(self.domains[v]) > 1]
        if not unassigned:
            # Check if any domain is empty (shouldn't happen if AC3 returns True)
            if any(not self.domains[v] for v in self.variables):
                return None
            return {v: self.domains[v][0] for v in self.variables}
        
        # MRV
        var = min(unassigned, key=lambda v: len(self.domains[v]))
        
        # Try values
        original_domains = {v: list(self.domains[v]) for v in self.variables}
        
        for val in sorted(original_domains[var]):
            self.domains[var] = [val]
            
            # Save state before propagation
            # AC-3 propagation
            queue = [(n, var) for n in self.neighbors[var]]
            if self.ac3(list(queue)):
                result = self.backtrack()
                if result:
                    return result
            
            # Backtrack / Restore
            for v in self.variables:
                self.domains[v] = list(original_domains[v])
                
        self.failures += 1
        return None

def print_board(assignment):
    for r in range(9):
        print("".join(str(assignment[(r, c)]) for c in range(9)))

def load_board(filename):
    with open(filename, 'r') as f:
        return [[int(c) for c in line.strip()] for line in f if line.strip()]

if __name__ == "__main__":
    for f in ["easy.txt", "medium.txt", "hard.txt", "veryhard.txt"]:
        print(f"\nProcessing {f}...")
        try:
            csp = SudokuCSP(load_board(f))
            sol = csp.solve()
            if sol:
                print("Solution:")
                print_board(sol)
                print(f"BACKTRACK calls: {csp.backtrack_calls}")
                print(f"BACKTRACK failures: {csp.failures}")
            else:
                print("No solution found.")
        except Exception as e:
            print(f"Error: {e}")
