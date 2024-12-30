import random 
import timeit
import tracemalloc
import pandas as pd  # Import pandas untuk manipulasi data dan ekspor ke Excel

# Generate random dataset
def generate_data(n, max_weight, max_value):
    weights = [random.randint(1, max_weight) for _ in range(n)]
    values = [random.randint(1, max_value) for _ in range(n)]
    capacity = sum(weights) // 2  # Simulated capacity
    return values, weights, capacity

# Dynamic Programming
def knapsack_dp(values, weights, capacity):
    n = len(values)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    for i in range(1, n + 1):
        for w in range(1, capacity + 1):
            if weights[i - 1] <= w:
                dp[i][w] = max(dp[i - 1][w], values[i - 1] + dp[i - 1][w - weights[i - 1]])
            else:
                dp[i][w] = dp[i - 1][w]
    return dp[n][capacity]

# Brute Force
def knapsack_brute(values, weights, capacity, n):
    if n == 0 or capacity == 0:
        return 0
    if weights[n - 1] > capacity:
        return knapsack_brute(values, weights, capacity, n - 1)
    include = values[n - 1] + knapsack_brute(values, weights, capacity - weights[n - 1], n - 1)
    exclude = knapsack_brute(values, weights, capacity, n - 1)
    return max(include, exclude)

# Greedy Algorithm
def knapsack_greedy(values, weights, capacity):
    n = len(values)
    items = [(values[i] / weights[i], weights[i], values[i]) for i in range(n)]
    items.sort(reverse=True, key=lambda x: x[0])  # Sort by value-to-weight ratio
    total_value = 0
    for ratio, weight, value in items:
        if capacity >= weight:
            capacity -= weight
            total_value += value
        else:
            total_value += ratio * capacity
            break
    return total_value

# Backtracking
def knapsack_backtracking(values, weights, capacity, index=0, current_value=0):
    if index == len(values) or capacity == 0:
        return current_value
    if weights[index] > capacity:
        return knapsack_backtracking(values, weights, capacity, index + 1, current_value)
    include = knapsack_backtracking(values, weights, capacity - weights[index], index + 1, current_value + values[index])
    exclude = knapsack_backtracking(values, weights, capacity, index + 1, current_value)
    return max(include, exclude)

# Divide and Conquer
def knapsack_divide_and_conquer(values, weights, capacity, n):
    if n == 0 or capacity == 0:
        return 0
    if weights[n - 1] > capacity:
        return knapsack_divide_and_conquer(values, weights, capacity, n - 1)
    include = values[n - 1] + knapsack_divide_and_conquer(values, weights, capacity - weights[n - 1], n - 1)
    exclude = knapsack_divide_and_conquer(values, weights, capacity, n - 1)
    return max(include, exclude)

# Measure execution time for each algorithm
def measure_time(algorithm, values, weights, capacity):
    if "divide_and_conquer" in algorithm.__name__ or "brute" in algorithm.__name__:
        # Untuk algoritma yang memerlukan parameter tambahan
        return timeit.timeit(lambda: algorithm(values, weights, capacity, len(values)), number=10)
    else:
        return timeit.timeit(lambda: algorithm(values, weights, capacity), number=10)

# Main function to execute and compare algorithms
def main():
    n = 100  # Number of items
    max_weight = 50
    max_value = 100
    values, weights, capacity = generate_data(n, max_weight, max_value)

    # Tampilkan data yang dihasilkan (opsional)
    print(f"Values: {values}")
    print(f"Weights: {weights}")
    print(f"Capacity: {capacity}\n")

    # Compare algorithms
    algorithms = [
        ("Dynamic Programming", knapsack_dp),
        ("Brute Force", knapsack_brute),
        ("Greedy Algorithm", knapsack_greedy),
        ("Backtracking", knapsack_backtracking),
        ("Divide and Conquer", knapsack_divide_and_conquer),
    ]

    results = []  # List untuk menyimpan hasil

    for name, algorithm in algorithms:
        tracemalloc.start()
        time_taken = measure_time(algorithm, values, weights, capacity)
        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        
        # Jalankan algoritma sekali lagi untuk mendapatkan hasil optimalnya
        if "divide_and_conquer" in algorithm.__name__ or "brute" in algorithm.__name__:
            optimal_value = algorithm(values, weights, capacity, len(values))
        elif "backtracking" in algorithm.__name__:
            optimal_value = algorithm(values, weights, capacity)
        else:
            optimal_value = algorithm(values, weights, capacity)
        
        # Tambahkan hasil ke daftar
        results.append({
            "Algoritma": name,
            "Waktu (detik)": round(time_taken, 6),
            "Memori (KB)": round(current / 1024, 2),
            "Memori Puncak (KB)": round(peak / 1024, 2),
            "Nilai Optimal": optimal_value
        })
        
        print(f"{name}:")
        print(f"  Time Taken: {time_taken:.6f} seconds")
        print(f"  Memory Used: {current / 1024:.2f} KB (Peak: {peak / 1024:.2f} KB)")
        print(f"  Nilai Optimal: {optimal_value}\n")

    # Buat DataFrame dari hasil
    df = pd.DataFrame(results)
    
    # Simpan ke file Excel
    excel_file = "knapsack_results.xlsx"
    df.to_excel(excel_file, index=False)
    print(f"Hasil telah disimpan ke dalam file '{excel_file}'.")

if __name__ == "__main__":
    main()
