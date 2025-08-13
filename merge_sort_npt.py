def merge_sort(arr: list[int]) -> tuple[list[int], int]:
    def merge(left, right):
        merged = []
        i = j = 0

        ##### Write your code here #######
        while i < len(left) and j < len(right):

            if left[i] < right[j]:
                merged.append(left[i])
                i += 1

            else:
                merged.append(right[j])
                j += 1

        merged.extend(right[j:])
        merged.extend(left[i:])

        return merged

    def recursive_sort(sub_arr):
        nonlocal merge_count
        if len(sub_arr) <= 1:
            return sub_arr

        mid = len(sub_arr) // 2
        left = recursive_sort(sub_arr[:mid])
        right = recursive_sort(sub_arr[mid:])

        merge_count += 1  # Count each merge operation
        print ((sub_arr, merge_count))
        return merge(left, right)

    merge_count = 0
    sorted_arr = recursive_sort(arr)
    return sorted_arr, merge_count


print("Final Results: ", merge_sort([5, 100, 80, 23, 94, 1, 4, 2, 8]))

