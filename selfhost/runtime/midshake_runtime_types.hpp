#pragma once
#include <string>
#include <iostream>
#include <unordered_map>
#include <vector>
#include <variant>
#include <memory>

namespace ms {

    // -------------------------
    // ValueKind
    // -------------------------
    enum class ValueKind { Number, String, List, Map, Object };

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
    struct MSObject;

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
        std::shared_ptr<MSObject> object;

        Value() : kind(ValueKind::Number), num(0) {}
        Value(const Number& n) : kind(ValueKind::Number), num(n) {}
        Value(const String& s) : kind(ValueKind::String), str(s) {}
        Value(const List& l) : kind(ValueKind::List), lst(l) {}
        Value(const Map& m) : kind(ValueKind::Map), mp(m) {}
        Value(const std::shared_ptr<MSObject>& o) : kind(ValueKind::Object), object(o) {}

        static Value from_double(double d) { return Value(Number(d)); }
        static Value from_string(const std::string& s) { return Value(String(s)); }
        static Value from_list(const List& l) { return Value(l); }
        static Value from_map(const Map& m) { return Value(m); }
        static Value from_object(const std::shared_ptr<MSObject>& o) { return Value(o); }

        // Helper: add two values (string concat or numeric add)
        Value operator+(const Value& other) const {
            if (kind == ValueKind::String || other.kind == ValueKind::String) {
                return Value::from_string(to_string() + other.to_string());
            }
            return Value::from_double(num.value + other.num.value);
        }

        // Helper: equality comparison
        bool operator==(const Value& other) const {
            if (kind != other.kind) return false;
            if (kind == ValueKind::Number) return num.value == other.num.value;
            if (kind == ValueKind::String) return str.value == other.str.value;
            return false;
        }

        bool operator!=(const Value& other) const {
            return !(*this == other);
        }

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
                case ValueKind::Object:
                    return "<object>";
            }
            return "";
        }
    };

    struct MSObject {
        std::string class_name;
        Map fields;
    };

}
