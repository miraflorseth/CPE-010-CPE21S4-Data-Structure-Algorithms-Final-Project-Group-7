#pragma once
#include <string>

struct Customer {
    int id;
    std::string name;
};

struct Reservation {
    int customerId;
    std::string name;
    int tableNo;
    int startMin;   
    bool playing;
};

struct Transaction {
    int id;
    int customerId;
    std::string name;
    int tableNo;
    int minutes;
    double amount;
};
