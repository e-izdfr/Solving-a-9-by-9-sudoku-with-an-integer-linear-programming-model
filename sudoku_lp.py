import pulp

def solve_sudoku(m):
    indices = [str(i) for i in range(1, 10)]
    rows = indices
    columns = indices
    values = indices
    choices = pulp.LpVariable.dicts(name='Choice', indices=(values, rows, columns), cat='Binary')
    problem = pulp.LpProblem(name='Sudoku_Problem', sense=pulp.const.LpMinimize)
    problem += 0

    for r in rows:
        for c in columns:
            problem += pulp.lpSum([choices[v][r][c] for v in values]) == 1

    for v in values:
        for r in rows:
            problem += pulp.lpSum([choices[v][r][c] for c in columns]) == 1

    for v in values:
        for c in columns:
            problem += pulp.lpSum([choices[v][r][c] for r in rows]) == 1

    squares = []
    for i in range(3):
        for j in range(3):
            squares += [[(rows[3 * i + k], columns[3 * j + p]) for k in range(3) for p in range(3)]]

    for v in values:
        for b in squares:
            problem += pulp.lpSum([choices[v][r][c] for (r, c) in b]) == 1

    for num in m:
        problem += choices[str(num[0])][str(num[1])][str(num[2])] == 1

    problem.solve()
    print('Status:', pulp.LpStatus[problem.status])
    display = open('display_sudoku.txt', 'w')
    if pulp.LpStatus[problem.status] != 'Infeasible':
        display = open('display_sudoku.txt', 'w')
        for r in rows:
            if r == '1' or r == '4' or r == '7':
                display.write('+-------+-------+-------+\n')
            for c in columns:
                for v in values:
                    if pulp.value(choices[v][r][c]) == 1:
                        if c == '1' or c == '4' or c == '7':
                            display.write('| ')
                        display.write(v + ' ')
                        if c == '9':
                            display.write('|\n')
        display.write('+-------+-------+-------+')
        display.close()

solve_sudoku([
    [2, 1, 5],
    [7, 1, 8],
    [4, 2, 1],
    [1, 2, 5],
    [8, 2, 6],
    [5, 2, 9],
    [7, 3, 2],
    [3, 3, 3],
    [9, 3, 9],
    [7, 4, 7],
    [8, 5, 5],
    [1, 5, 8],
    [9, 6, 6],
    [3, 6, 9],
    [9, 7, 2],
    [5, 7, 6],
    [8, 8, 1],
    [6, 8, 4],
    [1, 8, 6],
    [3, 8, 8],
    [2, 9, 3],
    [4, 9, 7]
])