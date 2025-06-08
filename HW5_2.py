def binary_search_with_upper_bound(arr, target):
    left, right = 0, len(arr) - 1
    iterations = 0
    upper_bound = None

    while left <= right:
        iterations += 1
        mid = (left + right) // 2
        if arr[mid] < target:
            left = mid + 1
        else:
            # arr[mid] >= target, верхня межа
            upper_bound = arr[mid]
            right = mid - 1

    return (iterations, upper_bound)

arr = [0.5, 1.1, 2.3, 3.3, 4.7, 5.9, 7.2, 9.8]
target = 5.0

result = binary_search_with_upper_bound(arr, target)
print(result)  