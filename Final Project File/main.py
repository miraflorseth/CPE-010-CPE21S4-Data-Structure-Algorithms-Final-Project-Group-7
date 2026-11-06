#include <algorithm>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

#include "Algorithms.h"
#include "LinkedList.h"
#include "Models.h"
#include "Queue.h"

using namespace std;

const int NUM_TABLES = 6;
const double HOURLY_RATE = 120.0;   

enum class Status { Available, Reserved, Occupied };
struct Table { int no; Status status; int customerId; };

Table tables[NUM_TABLES];               
LinkedList<Reservation> reservations;   
LinkedList<Transaction> transactions;   
Queue<Customer> waiting;                
int nextCustomerId = 1001;
int nextTxnId = 1;

// ---------- input helpers (all input is validated) ----------
int readInt(const string& prompt, int lo, int hi) {
    while (true) {
        cout << prompt;
        string line;
        if (!getline(cin, line)) exit(0);
        try {
            size_t pos;
            int v = stoi(line, &pos);
            if (pos == line.size() && v >= lo && v <= hi) return v;
        } catch (...) {}
        cout << "  Invalid input. Enter a number from " << lo << " to " << hi << ".\n";
    }
}

string readName(const string& prompt) {
    while (true) {
        cout << prompt;
        string s;
        if (!getline(cin, s)) exit(0);
        s.erase(0, s.find_first_not_of(" \t"));
        s.erase(s.find_last_not_of(" \t") + 1);
        if (!s.empty() && s.size() <= 30) return s;
        cout << "  Name cannot be empty (maximum 30 characters).\n";
    }
}

int readTime(const string& prompt) {
    while (true) {
        cout << prompt << " (HH:MM, 24-hour): ";
        string s;
        if (!getline(cin, s)) exit(0);
        int h, m;
        if (sscanf(s.c_str(), "%d:%d", &h, &m) == 2 && h >= 0 && h < 24 && m >= 0 && m < 60)
            return h * 60 + m;
        cout << "  Invalid time. Example: 14:30\n";
    }
}

string fmtTime(int minutes) {
    char buf[16];
    snprintf(buf, sizeof(buf), "%02d:%02d", minutes / 60, minutes % 60);
    return buf;
}

// ---------- tables ----------
void initTables() {
    for (int i = 0; i < NUM_TABLES; ++i) tables[i] = {i + 1, Status::Available, 0};
}

int freeTable() {
    for (int i = 0; i < NUM_TABLES; ++i)
        if (tables[i].status == Status::Available) return i;
    return -1;
}

const char* statusName(Status s) {
    switch (s) {
        case Status::Available: return "Available";
        case Status::Reserved:  return "Reserved";
        default:                return "Occupied";
    }
}

void showTables() {
    cout << "\n Table | Status     | Customer ID\n";
    cout << "-------+------------+------------\n";
    for (int i = 0; i < NUM_TABLES; ++i) {
        cout << "   " << tables[i].no << "   | " << left << setw(10) << statusName(tables[i].status) << " | ";
        if (tables[i].customerId) cout << tables[i].customerId;
        else cout << "-";
        cout << "\n";
    }
}

void assignTable(int idx, const Customer& c) {
    tables[idx].status = Status::Reserved;
    tables[idx].customerId = c.id;
    reservations.insertBack({c.id, c.name, tables[idx].no, -1, false});
}

// When a table frees up, the customer at the front of the queue gets it.
void promoteFromQueue(int idx) {
    Customer next;
    if (waiting.dequeue(next)) {
        assignTable(idx, next);
        cout << "  " << next.name << " (ID " << next.id << ") moved from the queue to Table "
             << tables[idx].no << ".\n";
    }
}

Reservation* findReservation(int id) {
    return reservations.find([id](const Reservation& r) { return r.customerId == id; });
}

// ---------- operations ----------
void reserveTable() {
    Customer c{nextCustomerId++, readName("Customer name: ")};
    int idx = freeTable();
    if (idx >= 0) {
        assignTable(idx, c);
        cout << "  Reserved Table " << tables[idx].no << " for " << c.name
             << ". Customer ID: " << c.id << "\n";
    } else {
        waiting.enqueue(c);
        cout << "  All tables are taken. " << c.name << " (ID " << c.id
             << ") joined the queue at position " << waiting.size() << ".\n";
    }
}

void checkIn() {
    int id = readInt("Customer ID: ", 1, 999999);
    Reservation* r = findReservation(id);
    if (!r) { cout << "  No active reservation with that ID.\n"; return; }
    if (r->playing) { cout << "  This customer is already playing.\n"; return; }
    r->startMin = readTime("Start time");
    r->playing = true;
    tables[r->tableNo - 1].status = Status::Occupied;
    cout << "  " << r->name << " started on Table " << r->tableNo << " at " << fmtTime(r->startMin) << ".\n";
}

void endPlayAndPay() {
    int id = readInt("Customer ID: ", 1, 999999);
    Reservation* r = findReservation(id);
    if (!r) { cout << "  No active reservation with that ID.\n"; return; }
    if (!r->playing) { cout << "  This customer has not started playing. Use Check-in first.\n"; return; }

    int end = readTime("End time");
    if (end <= r->startMin) {
        cout << "  End time must be after the start time (" << fmtTime(r->startMin) << ").\n";
        return;
    }
    int minutes = end - r->startMin;
    int blocks = max(1, (minutes + 14) / 15);
    double fee = blocks * HOURLY_RATE / 4.0;

    Transaction t{nextTxnId++, r->customerId, r->name, r->tableNo, minutes, fee};
    transactions.insertBack(t);
    ofstream("sales.txt", ios::app) << t.id << "," << t.customerId << "," << t.name << ","
                                    << t.tableNo << "," << t.minutes << "," << fixed << setprecision(2) << t.amount << "\n";

    int tableIdx = t.tableNo - 1;
    reservations.removeIf([&](const Reservation& x) { return x.customerId == t.customerId; });
    tables[tableIdx].status = Status::Available;
    tables[tableIdx].customerId = 0;

    cout << fixed << setprecision(2);
    cout << "  Receipt #" << t.id << ": " << t.name << ", Table " << t.tableNo << ", "
         << minutes << " min -> PHP " << fee << "\n";
    promoteFromQueue(tableIdx);
}

void cancelReservation() {
    int id = readInt("Customer ID: ", 1, 999999);
    Reservation* r = findReservation(id);
    if (!r) { cout << "  No active reservation with that ID.\n"; return; }
    if (r->playing) { cout << "  This customer is playing. Use End play and pay instead.\n"; return; }
    int tableIdx = r->tableNo - 1;
    reservations.removeIf([id](const Reservation& x) { return x.customerId == id; });
    tables[tableIdx].status = Status::Available;
    tables[tableIdx].customerId = 0;
    cout << "  Reservation cancelled.\n";
    promoteFromQueue(tableIdx);
}

void showQueue() {
    if (waiting.isEmpty()) { cout << "  The waiting queue is empty.\n"; return; }
    cout << "\n Position | Customer ID | Name\n";
    int pos = 1;
    waiting.forEach([&](const Customer& c) {
        cout << "    " << pos++ << "     |    " << c.id << "     | " << c.name << "\n";
    });
}

void searchReservation() {
    // Binary search needs sorted data, so sort by customer ID first.
    vector<Reservation> v = reservations.toVector();
    bubbleSort(v, [](const Reservation& a, const Reservation& b) { return a.customerId < b.customerId; });
    int id = readInt("Customer ID to search: ", 1, 999999);
    int pos = binarySearch(v, id, [](const Reservation& r) { return r.customerId; });
    if (pos >= 0) {
        const Reservation& r = v[pos];
        cout << "  Found: ID " << r.customerId << ", " << r.name << ", Table " << r.tableNo << ", ";
        if (r.playing) cout << "playing since " << fmtTime(r.startMin) << "\n";
        else cout << "reserved (not started)\n";
        return;
    }
    int qpos = 0, found = 0;
    waiting.forEach([&](const Customer& c) { ++qpos; if (c.id == id) found = qpos; });
    if (found) cout << "  Customer " << id << " is in the waiting queue at position " << found << ".\n";
    else cout << "  No reservation or queue entry found for ID " << id << ".\n";
}

void salesReport() {
    if (transactions.size() == 0) { cout << "  No transactions yet.\n"; return; }
    int order = readInt("Sort by amount: 1) lowest first  2) highest first: ", 1, 2);
    vector<Transaction> v = transactions.toVector();
    bubbleSort(v, [order](const Transaction& a, const Transaction& b) {
        return order == 1 ? a.amount < b.amount : a.amount > b.amount;
    });
    double total = 0;
    cout << right << fixed << setprecision(2);
    cout << "\n Txn | Customer | Name                 | Table | Minutes | Amount (PHP)\n";
    for (const Transaction& t : v) {
        cout << " " << setw(3) << t.id << " | " << setw(8) << t.customerId << " | " << left << setw(20)
             << t.name << right << " | " << setw(5) << t.tableNo << " | " << setw(7) << t.minutes
             << " | " << setw(10) << t.amount << "\n";
        total += t.amount;
    }
    cout << "\n Transactions: " << v.size() << "   Total daily income: PHP " << total << "\n";
}

int main() {
    initTables();
    while (true) {
        cout << "\n===== Billiards Hall Reservation System =====\n"
             << " 1. View tables\n 2. Reserve a table\n 3. Check-in (start playing)\n"
             << " 4. End play and pay\n 5. Cancel reservation\n 6. View waiting queue\n"
             << " 7. Search reservation by customer ID\n 8. Daily sales report\n 0. Exit\n";
        int choice = readInt("Choose: ", 0, 8);
        switch (choice) {
            case 1: showTables(); break;
            case 2: reserveTable(); break;
            case 3: checkIn(); break;
            case 4: endPlayAndPay(); break;
            case 5: cancelReservation(); break;
            case 6: showQueue(); break;
            case 7: searchReservation(); break;
            case 8: salesReport(); break;
            case 0: cout << "Goodbye.\n"; return 0;
        }
    }
}
