#pragma once
#include "midshake_runtime_types.hpp"

namespace ms {

    // -------------------------
    // Environment (variables)
    // -------------------------
    class Environment {
    public:
        std::unordered_map<std::string, Value> vars;

        void set(const std::string& name, const Value& v) {
            vars[name] = v;
        }

        const Value& get(const std::string& name) const {
            auto it = vars.find(name);
            if (it == vars.end()) {
                throw std::runtime_error("Variable not defined: " + name);
            }
            return it->second;
        }
    };

    // -------------------------
    // Function pointer type
    // -------------------------
    using MSFunc = void(*)(Environment&, const std::vector<Value>&);

    // -------------------------
    // Standard library
    // -------------------------
    void print(const Value& v);

    Value inquire_number(const std::string& question);
    Value inquire_string(const std::string& question);

}
