#pragma once
#include <utility>
#include <vector>


template <typename T, typename Less>
void bubbleSort(std::vector<T>& a, Less less) {
    size_t n = a.size();
    for (size_t i = 0; i + 1 < n; ++i) {
        bool swapped = false;
        for (size_t j = 0; j + 1 < n - i; ++j) {
            if (less(a[j + 1], a[j])) {
                std::swap(a[j], a[j + 1]);
                swapped = true;
            }
        }
        if (!swapped) break;
    }
}


template <typename T, typename Key>
int binarySearch(const std::vector<T>& a, int target, Key key) {
    int lo = 0, hi = static_cast<int>(a.size()) - 1;
    while (lo <= hi) {
        int mid = lo + (hi - lo) / 2;
        int k = key(a[mid]);
        if (k == target) return mid;
        if (k < target) lo = mid + 1; else hi = mid - 1;
    }
    return -1;
}
