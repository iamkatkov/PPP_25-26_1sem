def find_cycles(adj_matrix):
    n = len(adj_matrix)
    cycles = []
    all_paths = []

    def dfs(start, current, visited, path):
        visited[current] = True
        path.append(current)
        all_paths.append(path.copy())

        for neighbor in range(n):
            if adj_matrix[current][neighbor]:
                if not visited[neighbor]:
                    dfs(start, neighbor, visited, path)
                elif neighbor == start and len(path) > 2:
                    cycles.append(path.copy())

        path.pop()
        visited[current] = False

    for i in range(n):
        dfs(i, i, [False] * n, [])

    unique_cycles = []
    for c in cycles:
        normalized = min(c[i:] + c[:i] for i in range(len(c)))
        if normalized not in unique_cycles:
            unique_cycles.append(normalized)

    return all_paths, unique_cycles

n = int(input("Введите количество вершин графа: "))
print("Введите таблицу смежности (по строкам, через пробел):")

adj_matrix = []
for i in range(n):
    row = list(map(int, input(f"Строка {i + 1}: ").split()))
    adj_matrix.append(row)

print("\nТаблица смежности:")
for row in adj_matrix:
    print(row)

paths, cycles = find_cycles(adj_matrix)

print("Все маршруты (для каждого шага):")
for p in paths:
    print(p)

print("Все найденные циклы:")
if cycles:
    for c in cycles:
        print(" -> ".join(map(str, c + [c[0]])))  
else:
    print("Циклы не найдены.")
