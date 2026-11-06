#pragma once

template <typename T>
class Queue {
    struct Node { T data; Node* next; };
    Node* head = nullptr;
    Node* tail = nullptr;
    int count = 0;

public:
    Queue() = default;
    Queue(const Queue&) = delete;
    Queue& operator=(const Queue&) = delete;
    ~Queue() { T tmp; while (dequeue(tmp)) {} }

    bool isEmpty() const { return head == nullptr; }
    int size() const { return count; }

    void enqueue(const T& value) {
        Node* n = new Node{value, nullptr};
        if (tail) tail->next = n; else head = n;
        tail = n;
        ++count;
    }

    bool dequeue(T& out) {
        if (!head) return false;
        Node* n = head;
        out = n->data;
        head = n->next;
        if (!head) tail = nullptr;
        delete n;
        --count;
        return true;
    }

    const T* peek() const { return head ? &head->data : nullptr; }

    template <typename F>
    void forEach(F f) const { for (Node* n = head; n; n = n->next) f(n->data); }
};
