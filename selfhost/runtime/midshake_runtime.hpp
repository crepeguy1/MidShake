#pragma once
#include "midshake_runtime_types.hpp"

namespace ms {

    // -------------------------
    // Environment (variables)
    // -------------------------
    class Environment {
    public:
        std::unordered_map<std::string, Value> vars;
        Environment* parent;

        Environment() : parent(nullptr) {
            // Initialize RESPONSE to empty string by default
            vars["RESPONSE"] = Value::from_string("");
        }

        // Initialize environment with command-line arguments
        Environment(int argc, char* argv[]) : parent(nullptr) {
            vars["RESPONSE"] = Value::from_string("");
            // Store command-line arguments in a list accessible from MidShake
            List argList;
            for (int i = 1; i < argc; i++) {
                argList.push_back(Value::from_string(argv[i]));
            }
            vars["ARGV"] = Value::from_list(argList);
        }

        explicit Environment(Environment& enclosing) : parent(&enclosing) {}

        void set(const std::string& name, const Value& v) {
            vars[name] = v;
        }

        void set_global(const std::string& name, const Value& v) {
            Environment* root = this;
            while (root->parent != nullptr) {
                root = root->parent;
            }
            root->vars[name] = v;
        }

        const Value& get(const std::string& name) const {
            auto it = vars.find(name);
            if (it != vars.end()) {
                return it->second;
            }
            if (parent != nullptr) {
                return parent->get(name);
            }
            throw std::runtime_error("Variable not defined: " + name);
        }
    };

    // -------------------------
    // Function pointer type
    // -------------------------
    using MSFunc = void(*)(Environment&, const std::vector<Value>&);
    enum class AccessLevel { Public, Private, Protected };
    using ClassMethodFunction = Value(*)(Environment&, const std::vector<Value>&);
    using ClassFieldInitializer = Value(*)(Environment&);

    void register_class(const std::string& name, const std::string& base_name);
    void register_class_field(const std::string& class_name, const std::string& field_name,
                              AccessLevel access, ClassFieldInitializer initializer);
    void register_class_method(const std::string& class_name, const std::string& method_name,
                               AccessLevel access, size_t arity, bool calls_base_constructor,
                               ClassMethodFunction method);
    Value create_object(Environment& env, const std::string& class_name,
                        const std::vector<Value>& args = std::vector<Value>{});
    void call_base_constructor(Environment& env, const Value& object,
                               const std::string& class_name, const std::vector<Value>& args);
    Value deny_private_access(const std::string& message);
    Value object_get_member(const Value& object, const std::string& member_name,
                            const std::string& caller_class);
    void object_set_member(const Value& object, const std::string& member_name,
                           const Value& value, const std::string& caller_class);
    Value call_object_method(Environment& env, const Value& object, const std::string& method_name,
                             const std::vector<Value>& args, const std::string& caller_class);

    // -------------------------
    // Standard library
    // -------------------------
    void print(const Value& v);
    Value cpp_unescape_string(Environment& env, const std::vector<Value>& args);
    Value cpp_escape_string(Environment& env, const std::vector<Value>& args);
    Value ms_std_println(Environment& env, const std::vector<Value>& args);
    Value ms_std_greet(Environment& env, const std::vector<Value>& args);
    Value ms_std_add_and_print(Environment& env, const std::vector<Value>& args);
    Value ms_std_repeat(Environment& env, const std::vector<Value>& args);
    Value ms_std_min(Environment& env, const std::vector<Value>& args);
    Value ms_std_max(Environment& env, const std::vector<Value>& args);
    Value ms_std_abs(Environment& env, const std::vector<Value>& args);
    Value ms_std_round(Environment& env, const std::vector<Value>& args);
    Value ms_std_toupper(Environment& env, const std::vector<Value>& args);
    Value ms_std_tolower(Environment& env, const std::vector<Value>& args);
    Value ms_std_startsWith(Environment& env, const std::vector<Value>& args);
    Value ms_std_endsWith(Environment& env, const std::vector<Value>& args);
    Value ms_std_isDigit(Environment& env, const std::vector<Value>& args);
    Value ms_std_isLetter(Environment& env, const std::vector<Value>& args);
    Value ms_std_isWhitespace(Environment& env, const std::vector<Value>& args);
    Value ms_std_readFile(Environment& env, const std::vector<Value>& args);
    Value ms_std_length(Environment& env, const std::vector<Value>& args);
    Value ms_std_charAt(Environment& env, const std::vector<Value>& args);
    Value ms_std_substring(Environment& env, const std::vector<Value>& args);
    Value ms_std_split(Environment& env, const std::vector<Value>& args);
    Value ms_std_join(Environment& env, const std::vector<Value>& args);
    Value ms_std_trim(Environment& env, const std::vector<Value>& args);
    Value ms_std_replace(Environment& env, const std::vector<Value>& args);
    Value ms_std_size(Environment& env, const std::vector<Value>& args);
    Value ms_std_append(Environment& env, const std::vector<Value>& args);
    Value ms_std_getItem(Environment& env, const std::vector<Value>& args);
    Value ms_std_mapSet(Environment& env, const std::vector<Value>& args);
    Value ms_std_mapGet(Environment& env, const std::vector<Value>& args);
    Value ms_std_indexOf(Environment& env, const std::vector<Value>& args);

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
