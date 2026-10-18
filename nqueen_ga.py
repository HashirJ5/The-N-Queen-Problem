import random

random.seed(1)

def conflicts(state):
    """Number of attacking pairs (same row or same diagonal). Index = column, value = row."""
    c = 0
    n = len(state)
    for i in range(n):
        for j in range(i + 1, n):
            if state[i] == state[j] or abs(state[i] - state[j]) == j - i:
                c += 1
    return c

MAX_PAIRS = 6  # C(4,2)

def selection_fitness(state):
    # conflicts: lower is better, so selection weight = non-attacking pairs
    return MAX_PAIRS - conflicts(state)

def roulette(pop):
    weights = [selection_fitness(s) for s in pop]
    total = sum(weights)
    r = random.random()
    cum = 0
    for s, w in zip(pop, weights):
        cum += w / total
        if r <= cum:
            return s, r
    return pop[-1], r

def crossover(p1, p2):
    return p1[:2] + p2[2:], p2[:2] + p1[2:]

population = [[2, 4, 3, 1], [1, 2, 3, 4], [2, 1, 3, 2], [4, 3, 1, 1]]

for gen in range(0, 3):
    print(f"\n=== Generation {gen} ===")
    weights = [selection_fitness(s) for s in population]
    total = sum(weights)
    for i, s in enumerate(population, 1):
        print(f"State-{i} {s}  conflicts={conflicts(s)}  weight={selection_fitness(s)}  prob={selection_fitness(s)/total:.2f}")
    print("Total conflicts =", sum(conflicts(s) for s in population))
    if gen == 2:
        break
    new_pop = []
    for pair in range(2):
        p1, r1 = roulette(population)
        p2, r2 = roulette(population)
        c1, c2 = crossover(p1, p2)
        print(f"Pair {pair+1}: r1={r1:.3f} -> {p1}, r2={r2:.3f} -> {p2}")
        print(f"   children: {c1} , {c2}")
        new_pop += [c1, c2]
    population = new_pop
