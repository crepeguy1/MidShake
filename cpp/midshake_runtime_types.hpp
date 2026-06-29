#pragma once
#include <string>
#include <iostream>
#include <unordered_map>
#include <vector>

namespace ms {

    // -------------------------
    // ValueKind
    // -------------------------
    enum class ValueKind { Number, String };

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
    // Value (union)
    // -------------------------
    class Value {
    public:
        ValueKind kind;
        Number num;
        String str;

        Value() : kind(ValueKind::Number), num(0) {}
        Value(const Number& n) : kind(ValueKind::Number), num(n) {}
        Value(const String& s) : kind(ValueKind::String), str(s) {}

        static Value from_double(double d) { return Value(Number(d)); }
        static Value from_string(const std::string& s) { return Value(String(s)); }
    };

}
