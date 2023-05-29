import random

a_batas_atas = 30
b_batas_atas = 10
c_batas_atas = 10
d_batas_atas = 10

jumlah_populasi = 6

NUM_GENERATIONS = 50

CROSSOVER_PROBABILITY = 0.8
MUTATION_PROBABILITY = 0.1

NUM_ELITES = 5

def evaluasi_kromosom(kromosom):
    a, b, c, d = kromosom
    return abs((a + 4*b + 2*c + 3*d) - 30)  

def inisialisasi_populasi():
    populasi = []
    for _ in range(jumlah_populasi):
        kromosom = [random.randint(0, a_batas_atas),
                      random.randint(0, b_batas_atas),
                      random.randint(0, c_batas_atas),
                      random.randint(0, d_batas_atas)]
        populasi.append(kromosom)
    return populasi

def select_parents(populasi):
    total_fitness = sum(1 / (1 + evaluasi_kromosom(kromosom)) for kromosom in populasi)
    probabilities = [(1 / (1 + evaluasi_kromosom(kromosom))) / total_fitness for kromosom in populasi]
    
    parents = []
    for _ in range(jumlah_populasi):
        parent = random.choices(populasi, probabilities)[0]
        parents.append(parent)
    return parents


def crossover(parent1, parent2):
    if random.random() < CROSSOVER_PROBABILITY:
        crossover_point = random.randint(1, len(parent1) - 1)
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        return child1, child2
    else:
        return parent1, parent2

def mutate(kromosom):
    mutated_kromosom = kromosom.copy()
    for i in range(len(mutated_kromosom)):
        if random.random() < MUTATION_PROBABILITY:
            mutated_kromosom[i] = random.randint(0, [a_batas_atas, b_batas_atas, c_batas_atas, d_batas_atas][i])
    return mutated_kromosom

def select_new_generation(populasi, parents, elites):
    new_generation = elites.copy()
    while len(new_generation) < jumlah_populasi:
        parent1, parent2 = random.sample(parents, 2)
        child1, child2 = crossover(parent1, parent2)
        new_generation.extend([mutate(child1), mutate(child2)])
    return new_generation[:jumlah_populasi]

populasi = inisialisasi_populasi()

evaluasi_populasi = [(kromosom, evaluasi_kromosom(kromosom)) for kromosom in populasi]

for _ in range(NUM_GENERATIONS):
    evaluasi_populasi.sort(key=lambda x: x[1])
    elites = [kromosom for kromosom, _ in evaluasi_populasi[:NUM_ELITES]]
    parents = select_parents([kromosom for kromosom, _ in evaluasi_populasi])
    populasi = select_new_generation(populasi, parents, elites)
    evaluasi_populasi = [(kromosom, evaluasi_kromosom(kromosom)) for kromosom in populasi]

best_kromosom, best_fitness = min(evaluasi_populasi, key=lambda x: x[1])
print("Solusi terbaik:")
print("Nilai a =", best_kromosom[0])
print("Nilai b =", best_kromosom[1])
print("Nilai c =", best_kromosom[2])
print("Nilai d =", best_kromosom[3])
print("Fitness terbaik:", best_fitness)
