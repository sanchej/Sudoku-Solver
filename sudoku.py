import sys
row = [0] * 9
notes = row * 9


def grid_print(grid):
    for i in range(0, 81, 9):
        temp = grid[i:i+9]
        print(temp)


# grid = list(
#     '000760900740029000006000050079235106514870309000004508650300090000002700087000430')
# grid = list(
#     '070004500080000000200000780000009020000500004906000001003020000012040000000875000')
# grid = list(
#     '000153000072090000080070000700000510005009300001000000000300009640080002000006070')
# grid = list(
#     '600900700000078000010005300000300000080700003040000650109000007304106800000000000')

# grid = list(
#     '001620057000000009040100000000060400030007065005000900000000600800003000004070021')

# grid = list(
#     '000000001905300600003100040002080000000000106700000580000003000870026004040000700')
grid = list(
    '900000005060070000002008490000000010009004380200900000003000001700080530000005002')


def translate(grid):
    grid = [int(x) for x in grid]
    rows = []
    cols = []
    for i in range(0, 81, 9):
        rows.append(list(range(i, i+9)))
    for i in range(9):
        cols.append(list(range(i, 81, 9)))
    cells = [[], [], [], [], [], [], [], [], []]
    for x in range(len(grid)):
        if x % 9 in range(0, 3):
            if x < 21:
                cells[0].append(x)
            elif x < 48:
                cells[3].append(x)
            elif x < 75:
                cells[6].append(x)
        if x % 9 in range(3, 6):
            if x < 24:
                cells[1].append(x)
            elif x < 51:
                cells[4].append(x)
            elif x < 78:
                cells[7].append(x)
        if x % 9 in range(6, 9):
            if x < 27:
                cells[2].append(x)
            elif x < 54:
                cells[5].append(x)
            elif x < 81:
                cells[8].append(x)
    return grid, rows, cols, cells


def newnotes(grid, cells):
    notes = [[] for _ in range(81)]
    for x in range(len(grid)):
        if grid[x] == 0:
            rownum = x//9 * 9
            temp = grid[rownum:rownum+9]
            temp2 = grid[x % 9::9]
            temp3 = []
            for y in cells:
                if x in y:
                    temp3 = y
                    break
            temp3 = [grid[y] for y in temp3]
            temp = set(temp + temp2 + temp3)
            notes[x] = list({1, 2, 3, 4, 5, 6, 7, 8, 9} - temp)
        else:
            notes[x] = [grid[x]]
    return notes


def newnotes2(notes, rows, cols, cells):
    o = [cells, rows, cols]
    for p in o:
        for j in p:
            temp4 = [notes[y] for y in j]
            for y in range(len(temp4)):
                t = temp4[y]
                if len(temp4[y]) == 2:
                    for z in range(len(temp4)):
                        a = set(temp4[z]) - set(temp4[y])
                        if z != y and len(a) == 0:
                            for k in range(len(temp4)):
                                if k != z and k != y:
                                    notes[j[k]] = list(
                                        set(notes[j[k]]) - set(t))
    return notes


def newnotes3(notes, rows, cols, cells):
    o = [cells, rows, cols]
    for p in o:
        for j in p:
            temp4 = [notes[y] for y in j]
            temp5 = [[] for _ in range(9)]
            for i in range(1, 10):
                for ind, d in enumerate(temp4):
                    if i in d:
                        temp5[i-1].append(ind)
            for d in range(len(temp5)-1):
                if len(temp5[d]) == 2:
                    tempo = j[temp5[d][0]] % 9
                    if tempo == j[temp5[d][1]] % 9:
                        for h in cols[tempo]:
                            if h != j[temp5[d][0]] and h != j[temp5[d][1]]:
                                notes[h] = list(set(notes[h]) - set([d+1]))
                    tempo = j[temp5[d][0]] // 9
                    if tempo == j[temp5[d][1]] // 9:
                        for h in rows[tempo]:
                            if h != j[temp5[d][0]] and h != j[temp5[d][1]]:
                                notes[h] = list(set(notes[h]) - set([d+1]))

            for d in range(len(temp5)-2):
                k = d + 1
                while k < len(temp5)-1:
                    k += 1
                    if len(temp5[d]) == 2 and temp5[d] == temp5[k]:
                        for s in temp5[d]:
                            notes[j[s]] = [d+1, k+1]
    return notes


def newnotes4(notes, rows, cols):
    z = [rows, cols]
    for l in z:
        for p in l:
            for j in range(0, 9, 3):
                t = [p[j], p[j+1], p[j+2]]
                t = [notes[x] for x in t]
                t = list(set(t[0] + t[1] + t[2]))
                if len(t) == 3:
                    for o in range(j+3, j+9):
                        notes[p[o % 9]] = list(set(notes[p[o % 9]]) - set(t))
        return notes


def newgrid(grid, notes, rows, cols, cells):
    o = [cells, rows, cols]
    for p in o:
        for j in p:
            temp4 = [notes[y] for y in j]
            for y in range(len(temp4)):
                t = temp4[y]
                t2 = set()
                if len(temp4[y]) > 1:
                    for z in range(len(temp4)):
                        if z != y:
                            for i in temp4[z]:
                                t2.add(i)
                    t = list(set(t) - set(t2))
                    if len(t) == 1:
                        grid[j[y]] = t[0]
                else:
                    grid[j[y]] = t[0]
        return grid


# grid_print(grid)
# print(" ")
def solve(grid):
    grid, rows, cols, cells = translate(grid)
    notes = []
    rgrid = list(grid)
    rnotes = list(notes)
    testnum = 0
    mind = 0
    while 0 in grid:
        sgrid = list(grid)
        notes = newnotes(grid, cells)
        notes = newnotes2(notes, rows, cols, cells)
        notes = newnotes3(notes, rows, cols, cells)
        notes = newnotes4(notes, rows, cols)
        if [] in notes:
            testnum += 1

            grid = list(rgrid)
            notes = list(rnotes)

        grid = newgrid(grid, notes, rows, cols, cells)

        if sgrid == grid:
            # print("BP")
            rgrid = list(grid)
            rnotes = list(notes)
            m = [i for i, n in enumerate(grid) if n == 0][mind]
            if len(notes[m]) - 1 < testnum:
                testnum = 0
                mind += 1
                m = [i for i, n in enumerate(grid) if n == 0][mind]
            grid[m] = notes[m][testnum]
        # print(" ")
        # grid_print(grid)
    return grid


# print(solve(grid))
