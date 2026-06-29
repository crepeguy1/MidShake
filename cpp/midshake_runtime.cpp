#include "midshake_runtime.hpp"

namespace ms {

    // -------------------------
    // print
    // -------------------------
    void print(const Value& v) {
        switch (v.kind) {
        case ValueKind::Number:
            std::cout << v.num.value;
            break;
        case ValueKind::String:
            std::cout << v.str.value;
            break;
        }
        std::cout << std::endl;
    }

    // -------------------------
    // inquire_number
    // -------------------------
    Value inquire_number(const std::string& question) {
        std::cout << question << " ";
        double d;
        std::cin >> d;
        return Value::from_double(d);
    }

    // -------------------------
    // inquire_string
    // -------------------------
    Value inquire_string(const std::string& question) {
        std::cout << question << " ";
        std::string s;
        std::getline(std::cin >> std::ws, s);
        return Value::from_string(s);
    }

}
