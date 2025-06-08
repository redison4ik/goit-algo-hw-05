import timeit
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

def kmp_search(text, pattern):
    def build_lps(pattern):
        lps = [0] * len(pattern)
        length = 0
        i = 1
        while i < len(pattern):
            if pattern[i] == pattern[length]:
                length += 1
                lps[i] = length
                i += 1
            else:
                if length != 0:
                    length = lps[length - 1]
                else:
                    lps[i] = 0
                    i += 1
        return lps

    lps = build_lps(pattern)
    i = j = 0
    while i < len(text):
        if pattern[j] == text[i]:
            i += 1
            j += 1
        if j == len(pattern):
            return True
        elif i < len(text) and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False

def boyer_moore_search(text, pattern):
    def build_bad_char_table(pattern):
        table = {}
        for i in range(len(pattern)):
            table[pattern[i]] = i
        return table

    bad_char = build_bad_char_table(pattern)
    m = len(pattern)
    n = len(text)
    i = 0

    while i <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[i + j]:
            j -= 1
        if j < 0:
            return True
        else:
            skip = j - bad_char.get(text[i + j], -1)
            i += max(1, skip)
    return False

def rabin_karp_search(text, pattern):
    d = 256
    q = 101
    m = len(pattern)
    n = len(text)
    h = pow(d, m - 1) % q
    p = 0
    t = 0

    for i in range(m):
        p = (d * p + ord(pattern[i])) % q
        t = (d * t + ord(text[i])) % q

    for s in range(n - m + 1):
        if p == t and text[s:s + m] == pattern:
            return True
        if s < n - m:
            t = (t - h * ord(text[s])) % q
            t = (t * d + ord(text[s + m])) % q
            t = (t + q) % q
    return False

def measure_search_time(algorithm, text, pattern):
    return timeit.timeit(lambda: algorithm(text, pattern), number=1)

def main():
    text1 = Path("стаття 1.txt").read_text(encoding='utf-8', errors='ignore')
    text2 = Path("стаття 2.txt").read_text(encoding='utf-8', errors='ignore')

    existing_substring = "алгоритм пошуку"
    non_existing_substring = "слово, якого немає"

    results = {
        "KMP": {
            "стаття 1 (існує)": measure_search_time(kmp_search, text1, existing_substring),
            "стаття 1 (не існує)": measure_search_time(kmp_search, text1, non_existing_substring),
            "стаття 2 (існує)": measure_search_time(kmp_search, text2, existing_substring),
            "стаття 2 (не існує)": measure_search_time(kmp_search, text2, non_existing_substring),
        },
        "Boyer-Moore": {
            "стаття 1 (існує)": measure_search_time(boyer_moore_search, text1, existing_substring),
            "стаття 1 (не існує)": measure_search_time(boyer_moore_search, text1, non_existing_substring),
            "стаття 2 (існує)": measure_search_time(boyer_moore_search, text2, existing_substring),
            "стаття 2 (не існує)": measure_search_time(boyer_moore_search, text2, non_existing_substring),
        },
        "Rabin-Karp": {
            "стаття 1 (існує)": measure_search_time(rabin_karp_search, text1, existing_substring),
            "стаття 1 (не існує)": measure_search_time(rabin_karp_search, text1, non_existing_substring),
            "стаття 2 (існує)": measure_search_time(rabin_karp_search, text2, existing_substring),
            "стаття 2 (не існує)": measure_search_time(rabin_karp_search, text2, non_existing_substring),
        }
    }

    df = pd.DataFrame(results).T
    df.to_csv("comparison.csv", index=True)
    #print("\nРезультати збережено у 'search_comparison_results.csv'\n")
    print(df)

    df.T.plot(kind='bar', figsize=(12, 6), title='Порівняння алгоритмів')
    plt.ylabel("Час виконання (секунди)")
    plt.tight_layout()
    plt.savefig("comparison.png")
    plt.show()

if __name__ == "__main__":
    main()
