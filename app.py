from flask import Flask, render_template, request, jsonify
app = Flask(__name__)

def record_step(steps, array_snapshot, highlight_indices=None):
    steps.append({
        "arr": array_snapshot.copy(),
        "highlight": ([] if highlight_indices is None else list(highlight_indices))
    })

def bubble_sort_steps(arr):
    working = arr.copy()
    steps = []
    record_step(steps, working)
    n = len(working)
    for i in range(n):
        for j in range(n - i - 1):
            record_step(steps, working, (j, j + 1))
            if working[j] > working[j + 1]:
                working[j], working[j + 1] = working[j + 1], working[j]
                record_step(steps, working, (j, j + 1))
    record_step(steps, working)
    return steps

def insertion_sort_steps(arr):
    working = arr.copy()
    steps = []
    record_step(steps, working)
    for i in range(1, len(working)):
        key = working[i]
        j = i - 1
        record_step(steps, working, (j, i))
        while j >= 0 and working[j] > key:
            working[j + 1] = working[j]
            record_step(steps, working, (j, j + 1))
            j -= 1
        working[j + 1] = key
        record_step(steps, working, (j + 1,))
    record_step(steps, working)
    return steps

def selection_sort_steps(arr):
    working = arr.copy()
    steps = []
    record_step(steps, working)
    n = len(working)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            record_step(steps, working, (min_idx, j))
            if working[j] < working[min_idx]:
                min_idx = j
                record_step(steps, working, (min_idx, i))
        if min_idx != i:
            working[i], working[min_idx] = working[min_idx], working[i]
            record_step(steps, working, (i, min_idx))
    record_step(steps, working)
    return steps

def merge_sort_steps(arr):
    working = arr.copy()
    steps = []
    record_step(steps, working)

    def merge(left, right, start_index):
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            li, rj = left[i], right[j]
            # highlight comparing elements in their global positions
            record_step(steps, working, (start_index + i, start_index + len(left) + j))
            if li <= rj:
                merged.append(li)
                i += 1
            else:
                merged.append(rj)
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        # write back
        for k, val in enumerate(merged):
            working[start_index + k] = val
            record_step(steps, working, (start_index + k,))

    def sort_range(start, end):  # inclusive start, exclusive end
        length = end - start
        if length <= 1:
            return
        mid = start + length // 2
        sort_range(start, mid)
        sort_range(mid, end)
        left = working[start:mid]
        right = working[mid:end]
        merge(left, right, start)

    sort_range(0, len(working))
    record_step(steps, working)
    return steps

def quick_sort_steps(arr):
    working = arr.copy()
    steps = []
    record_step(steps, working)

    def partition(low, high):
        pivot = working[high]
        i = low - 1
        for j in range(low, high):
            # highlight pivot and current j
            record_step(steps, working, (j, high))
            if working[j] <= pivot:
                i += 1
                working[i], working[j] = working[j], working[i]
                record_step(steps, working, (i, j))
        if i + 1 != high:
            working[i + 1], working[high] = working[high], working[i + 1]
            record_step(steps, working, (i + 1, high))
        return i + 1

    def quicksort(low, high):
        if low < high:
            pi = partition(low, high)
            quicksort(low, pi - 1)
            quicksort(pi + 1, high)

    if len(working) > 0:
        quicksort(0, len(working) - 1)
    record_step(steps, working)
    return steps

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/sort', methods=['POST'])
def sort():
    data = request.get_json()
    arr = data['array']
    method = data['method']

    if method == 'bubble':
        steps = bubble_sort_steps(arr)
    elif method == 'insertion':
        steps = insertion_sort_steps(arr)
    elif method == 'selection':
        steps = selection_sort_steps(arr)
    elif method == 'merge':
        steps = merge_sort_steps(arr)
    elif method == 'quick':
        steps = quick_sort_steps(arr)
    else:
        steps = [{"arr": arr, "highlight": []}]

    return jsonify(steps)

if __name__ == '__main__':
    app.run(debug=True)