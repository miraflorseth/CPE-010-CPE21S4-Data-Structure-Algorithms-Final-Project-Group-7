#include <chrono>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

#include "Algorithms.h"
#include "Models.h"
#include "Queue.h"

using namespace std;
using Clock = chrono::steady_clock;

double elapsedMs(Clock::time_point a, Clock::time_point b) {
    return chrono::duration<double, milli>(b - a).count();
}

int main() {
    mt19937 rng(42);
    const int sizes[] = {100, 1000, 10000, 100000};
    cout << fixed << setprecision(3);
    cout << "n, enqueue_ms, binary_search_100k_lookups_ms, bubble_sort_ms\n";

    for (int n : sizes) {
        int reps = (n <= 10000) ? 5 : 1;   
        double tq = 0, ts = 0, tb = 0;

        for (int r = 0; r < reps; ++r) {
            {   
                Queue<Customer> q;
                auto a = Clock::now();
                for (int i = 0; i < n; ++i) q.enqueue({i, "x"});
                auto b = Clock::now();
                tq += elapsedMs(a, b);
            }
            {  
                vector<Reservation> v;
                for (int i = 0; i < n; ++i) v.push_back({i + 1, "x", 1, -1, false});
                volatile int sink = 0; (void)sink;
                auto a = Clock::now();
                for (int k = 0; k < 100000; ++k)
                    sink = binarySearch(v, (k * 7919) % n + 1, [](const Reservation& x) { return x.customerId; });
                auto b = Clock::now();
                ts += elapsedMs(a, b);
            }
            {   
                vector<Transaction> v;
                for (int i = 0; i < n; ++i) v.push_back({i, i, "x", 1, 60, (double)(rng() % 100000)});
                auto a = Clock::now();
                bubbleSort(v, [](const Transaction& x, const Transaction& y) { return x.amount < y.amount; });
                auto b = Clock::now();
                tb += elapsedMs(a, b);
            }
        }
        cout << n << ", " << tq / reps << ", " << ts / reps << ", " << tb / reps << endl;
    }
}
