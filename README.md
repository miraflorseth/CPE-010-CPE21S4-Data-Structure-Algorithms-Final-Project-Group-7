# CPE-010-CPE21S4-Data-Structure-And-Algorithms-Final-Project-Group-7
**Data Structure &amp; Algorithms Final Project Group 7**

# 🎱 Billiards Hall Management and Table Reservation System

Console program in C++ (CPE 010, Data Structures and Algorithms).

## Files
| File | Purpose |
|------|---------|
| main.cpp | Menu, table array, reservations, payments, reports |
| Queue.h | Linked-list queue (FIFO) for customers waiting for a table |
| LinkedList.h | Singly linked list for reservations and transactions |
| Algorithms.h | Bubble sort and binary search |
| Models.h | Customer, Reservation and Transaction structs |
| benchmark.cpp | Timing code for the experimental analysis |

## Compile and run
```
g++ -std=c++17 -O2 main.cpp -o billiards
./billiards
```
On Windows use `billiards.exe`.

## Benchmark
```
g++ -std=c++17 -O2 benchmark.cpp -o benchmark
./benchmark
```
The last row (n = 100,000) runs bubble sort once and can take a few minutes.

## Data structures and algorithms
- Array: the 6 tables and their status
- Queue (linked list): waiting customers, first come first served
- Linked list: active reservations and paid transactions
- Binary search: find a reservation by customer ID (records sorted first)
- Bubble sort: sort sales by amount

Paid sessions are also appended to sales.txt. Fees are PHP 120 per hour, billed in 15-minute blocks.


# 👥 Team Members
- **Miraflor, Seth Carlo T.**
- **Macaraeg, Bien**
- **Olmoguez, Zyd P.**
- **Lacsamana, Timothy** 

# 📝 Project Description
- **This is a Billiards Hall Management and Table Reservation System Project. This project is intended to help manage the daily operations of a billiards hall. It helps to arrange table reservations, check table
  availability, record customers, monitor play time and handle payments.
  Our project aims to make billiards hall management easier, faster and more organized. It also shows the use of data structures and algorithms in solving real world problems.***

# 🎯 Objectives
- **To Manage Billiards Table Reservation Efficiently**
- **To Check Table Availability**
- **To Organize Customers and Reservation records**
- **To Keep Track Of Play Time And Payments**

# ⚙️ Features
- **Customer Management**
- **Table Availability Checking**
- **Table Reservation Management**
- **Play Time Monitoring**
- **Payment Recording**

# 💻 Technologies We Used
- **Programming Language: C++**
- **Tools: Github, Google Docs**
- **Application: Visual Studio Code**
