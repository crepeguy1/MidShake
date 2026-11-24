#pragma once
#include "midshake_runtime_types.hpp"

namespace ms {

    // -------------------------
    // Environment (variables)
    // -------------------------
    class Environment {
    public:
        std::unordered_map<std::string, Value> vars;

        Environment() {
            // Initialize RESPONSE to empty string by default
            vars["RESPONSE"] = Value::from_string("");
        }

        // Initialize environment with command-line arguments
        Environment(int argc, char* argv[]) {
            vars["RESPONSE"] = Value::from_string("");
            // Store command-line arguments in a list accessible from MidShake
            List argList;
            for (int i = 1; i < argc; i++) {
                argList.push_back(Value::from_string(argv[i]));
            }
            vars["ARGV"] = Value::from_list(argList);
        }

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

    // -------------------------
    // String functions
    // -------------------------
    Value string_length(const Value& s);
    Value substring(const Value& s, const Value& start, const Value& end);
    Value char_at(const Value& s, const Value& index);
    Value string_split(const Value& s, const Value& delimiter);
    Value string_trim(const Value& s);
    Value string_join(const Value& lst, const Value& delimiter);

    // -------------------------
    // List functions
    // -------------------------
    Value list_length(const Value& lst);
    Value list_append(const Value& lst, const Value& element);
    Value list_index(const Value& lst, const Value& index);

    // -------------------------
    // Map functions
    // -------------------------
    Value map_get(const Value& mp, const Value& key);
    Value map_set(const Value& mp, const Value& key, const Value& value);

    // -------------------------
    // Math functions
    // -------------------------
    Value math_min(const Value& a, const Value& b);
    Value math_max(const Value& a, const Value& b);
    Value math_abs(const Value& a);
    Value math_round(const Value& a);

    // -------------------------
    // String utility functions
    // -------------------------
    Value string_toupper(const Value& s);
    Value string_tolower(const Value& s);
    Value string_startswith(const Value& s, const Value& prefix);
    Value string_endswith(const Value& s, const Value& suffix);
    Value string_isdigit(const Value& s);
    Value string_isletter(const Value& s);
    Value string_iswhitespace(const Value& s);
    Value string_replace(const Value& s, const Value& old, const Value& new_);
    Value string_indexof(const Value& s, const Value& substr);
    bool value_equals(const Value& a, const Value& b);

    // -------------------------
    // File I/O functions
    // -------------------------
    Value file_read(const std::string& path);
    void file_write(const std::string& path, const Value& value);

}
