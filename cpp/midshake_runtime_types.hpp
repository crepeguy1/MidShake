#pragma once
#include <string>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <variant>

namespace ms {

    // -------------------------
    // ValueKind
    // -------------------------
    enum class ValueKind { Number, String, List, Map };

    // -------------------------
    // Number
    // -------------------------
    class Number {
    public:
        double value;

        Number() : value(0) {}
        Number(double v) : value(v) {}

        Number operator+(const Number& other) const { return Number(value + other.value); }
        Number operator-(const Number& other) const { return Number(value - other.value); }
        Number operator*(const Number& other) const { return Number(value * other.value); }
        Number operator/(const Number& other) const { return Number(value / other.value); }

        bool operator<(const Number& other) const { return value < other.value; }
        bool operator>(const Number& other) const { return value > other.value; }
        bool operator<=(const Number& other) const { return value <= other.value; }
        bool operator>=(const Number& other) const { return value >= other.value; }
        bool operator==(const Number& other) const { return value == other.value; }
        bool operator!=(const Number& other) const { return value != other.value; }
    };

    // -------------------------
    // String
    // -------------------------
    class String {
    public:
        std::string value;

        String() = default;
        String(const std::string& v) : value(v) {}
        String(const char* v) : value(v) {}

        String operator+(const String& other) const {
            return String(value + other.value);
        }
    };

    // -------------------------
    // Forward declaration for Value
    // -------------------------
    class Value;

    // -------------------------
    // List (vector of Values)
    // -------------------------
    using List = std::vector<Value>;

    // -------------------------
    // Map (unordered_map of string to Value)
    // -------------------------
    using Map = std::unordered_map<std::string, Value>;

    // -------------------------
    // Value (union)
    // -------------------------
    class Value {
    public:
        ValueKind kind;
        Number num;
        String str;
        List lst;
        Map mp;

        Value() : kind(ValueKind::Number), num(0) {}
        Value(const Number& n) : kind(ValueKind::Number), num(n) {}
        Value(const String& s) : kind(ValueKind::String), str(s) {}
        Value(const List& l) : kind(ValueKind::List), lst(l) {}
        Value(const Map& m) : kind(ValueKind::Map), mp(m) {}

        static Value from_double(double d) { return Value(Number(d)); }
        static Value from_string(const std::string& s) { return Value(String(s)); }
        static Value from_list(const List& l) { return Value(l); }
        static Value from_map(const Map& m) { return Value(m); }

        // Helper: convert value to string for printing
        std::string to_string() const {
            switch (kind) {
                case ValueKind::Number:
                    return std::to_string(num.value);
                case ValueKind::String:
                    return str.value;
                case ValueKind::List: {
                    std::string result = "[";
                    for (size_t i = 0; i < lst.size(); i++) {
                        if (i > 0) result += ", ";
                        result += lst[i].to_string();
                    }
                    result += "]";
                    return result;
                }
                case ValueKind::Map: {
                    std::string result = "{";
                    bool first = true;
                    for (const auto& pair : mp) {
                        if (!first) result += ", ";
                        result += pair.first + ": " + pair.second.to_string();
                        first = false;
                    }
                    result += "}";
                    return result;
                }
            }
            return "";
        }
    };

}
