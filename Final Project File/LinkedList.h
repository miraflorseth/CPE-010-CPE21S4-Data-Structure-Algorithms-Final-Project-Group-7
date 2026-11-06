#pragma once
#include <vector>

template <typename T>
class LinkedList {
    struct Node { T data; Node* next; };
    Node* head = nullptr;
    Node* tail = nullptr;
    int count = 0;

public:
    LinkedList() = default;
    LinkedList(const LinkedList&) = delete;
    LinkedList& operator=(const LinkedList&) = delete;
    ~LinkedList() { while (head) { Node* n = head; head = head->next; delete n; } }

    int size() const { return count; }

    void insertFront(const T& v) {
        Node* n = new Node{v, head};
        head = n;
        if (!tail) tail = n;
        ++count;
    }

    void insertBack(const T& v) {
        Node* n = new Node{v, nullptr};
        if (tail) tail->next = n; else head = n;
        tail = n;
        ++count;
    }

    template <typename P>
    T* find(P pred) {
        for (Node* n = head; n; n = n->next) if (pred(n->data)) return &n->data;
        return nullptr;
    }

    template <typename P>
    bool removeIf(P pred) {
        Node* prev = nullptr;
        for (Node* n = head; n; prev = n, n = n->next) {
            if (pred(n->data)) {
                if (prev) prev->next = n->next; else head = n->next;
                if (n == tail) tail = prev;
                delete n;
                --count;
                return true;
            }
        }
        return false;
    }

    std::vector<T> toVector() const {
        std::vector<T> out;
        for (Node* n = head; n; n = n->next) out.push_back(n->data);
        return out;
    }
};
