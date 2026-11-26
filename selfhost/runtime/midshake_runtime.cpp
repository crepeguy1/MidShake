#include "midshake_runtime.hpp"
#include <sstream>
#include <algorithm>
#include <cctype>
#include <cmath>
#include <fstream>
#include <stdexcept>
#include <unordered_map>

namespace ms {

namespace {
    struct ClassFieldInfo {
        AccessLevel access;
        ClassFieldInitializer initializer;
    };

    struct ClassMethodInfo {
        AccessLevel access;
        size_t arity;
        ClassMethodFunction function;
    };

    struct ClassInfo {
        std::string base_name;
        std::unordered_map<std::string, ClassFieldInfo> fields;
        std::unordered_map<std::string, ClassMethodInfo> methods;
    };

    std::unordered_map<std::string, ClassInfo>& class_registry() {
        static std::unordered_map<std::string, ClassInfo> registry;
        return registry;
    }

    std::vector<std::string> class_chain(const std::string& class_name) {
        std::vector<std::string> chain;
        std::unordered_map<std::string, bool> seen;
        std::string current = class_name;
        while (!current.empty()) {
            if (seen[current]) {
                throw std::runtime_error("Class inheritance cycle involving: " + current);
            }
            seen[current] = true;
            auto class_it = class_registry().find(current);
            if (class_it == class_registry().end()) {
                throw std::runtime_error("Class not defined: " + current);
            }
            chain.push_back(current);
            current = class_it->second.base_name;
        }
        return chain;
    }

    bool is_subclass(const std::string& class_name, const std::string& base_name) {
        if (class_name.empty()) return false;
        const auto chain = class_chain(class_name);
        return std::find(chain.begin(), chain.end(), base_name) != chain.end();
    }

    void require_access(AccessLevel access, const std::string& owner,
                        const std::string& member, const std::string& caller) {
        if (access == AccessLevel::Public) return;
        if (access == AccessLevel::Private && caller == owner) return;
        if (access == AccessLevel::Protected && is_subclass(caller, owner)) return;
        const char* level = access == AccessLevel::Private ? "Private" : "Protected";
        throw std::runtime_error(std::string(level) + " member cannot be accessed: " + owner + "." + member);
    }

    std::pair<std::string, ClassFieldInfo> find_field(const std::string& class_name,
                                                       const std::string& field_name) {
        for (const auto& current : class_chain(class_name)) {
            const auto& fields = class_registry().at(current).fields;
            auto field = fields.find(field_name);
            if (field != fields.end()) return {current, field->second};
        }
        throw std::runtime_error("Field not defined: " + class_name + "." + field_name);
    }

    std::pair<std::string, ClassMethodInfo> find_method(const std::string& class_name,
                                                         const std::string& method_name) {
        for (const auto& current : class_chain(class_name)) {
            const auto& methods = class_registry().at(current).methods;
            auto method = methods.find(method_name);
            if (method != methods.end()) return {current, method->second};
        }
        throw std::runtime_error("Method not defined: " + class_name + "." + method_name);
    }

    void invoke_constructor(Environment& env, const std::shared_ptr<MSObject>& object,
                             const std::string& owner, const std::vector<Value>& args) {
        const auto& methods = class_registry().at(owner).methods;
        auto constructor = methods.find("constructor");
        if (constructor == methods.end()) {
            if (!args.empty()) {
                throw std::runtime_error(
                    "Class '" + owner + "' has no constructor that accepts arguments."
                );
            }
            return;
        }
        if (args.size() != constructor->second.arity) {
            throw std::runtime_error(
                "Constructor '" + owner + "' expects " +
                std::to_string(constructor->second.arity) + " argument(s) but got " +
                std::to_string(args.size()) + "."
            );
        }
        std::vector<Value> method_args{Value::from_object(object)};
        method_args.insert(method_args.end(), args.begin(), args.end());
        constructor->second.function(env, method_args);
    }
}

void register_class(const std::string& name, const std::string& base_name) {
    class_registry()[name].base_name = base_name;
}

void register_class_field(const std::string& class_name, const std::string& field_name,
                          AccessLevel access, ClassFieldInitializer initializer) {
    class_registry()[class_name].fields[field_name] = {access, initializer};
}

void register_class_method(const std::string& class_name, const std::string& method_name,
                           AccessLevel access, size_t arity, ClassMethodFunction method) {
    class_registry()[class_name].methods[method_name] = {access, arity, method};
}

Value create_object(Environment& env, const std::string& class_name,
                    const std::vector<Value>& args) {
    const auto chain = class_chain(class_name);
    auto object = std::make_shared<MSObject>();
    object->class_name = class_name;

    for (auto class_it = chain.rbegin(); class_it != chain.rend(); ++class_it) {
        for (const auto& field : class_registry().at(*class_it).fields) {
            object->fields[field.first] = field.second.initializer(env);
        }
    }
    for (auto class_it = chain.rbegin(); class_it != chain.rend(); ++class_it) {
        const std::vector<Value> no_args;
        invoke_constructor(env, object, *class_it, *class_it == class_name ? args : no_args);
    }
    return Value::from_object(object);
}

Value object_get_member(const Value& object, const std::string& member_name,
                        const std::string& caller_class) {
    if (object.kind != ValueKind::Object || !object.object) {
        throw std::runtime_error("Member access requires a class instance.");
    }
    const auto found = find_field(object.object->class_name, member_name);
    require_access(found.second.access, found.first, member_name, caller_class);
    return object.object->fields.at(member_name);
}

void object_set_member(const Value& object, const std::string& member_name,
                       const Value& value, const std::string& caller_class) {
    if (object.kind != ValueKind::Object || !object.object) {
        throw std::runtime_error("Member assignment requires a class instance.");
    }
    const auto found = find_field(object.object->class_name, member_name);
    require_access(found.second.access, found.first, member_name, caller_class);
    object.object->fields[member_name] = value;
}

Value call_object_method(Environment& env, const Value& object, const std::string& method_name,
                         const std::vector<Value>& args, const std::string& caller_class) {
    if (object.kind != ValueKind::Object || !object.object) {
        throw std::runtime_error("Method call requires a class instance.");
    }
    const auto found = find_method(object.object->class_name, method_name);
    require_access(found.second.access, found.first, method_name, caller_class);
    if (args.size() != found.second.arity) {
        throw std::runtime_error(
            "Method '" + method_name + "' expects " +
            std::to_string(found.second.arity) + " argument(s) but got " +
            std::to_string(args.size()) + "."
        );
    }
    std::vector<Value> method_args;
    method_args.reserve(args.size() + 1);
    method_args.push_back(object);
    method_args.insert(method_args.end(), args.begin(), args.end());
    return found.second.function(env, method_args);
}

    // -------------------------
    // print
    // -------------------------
    void print(const Value& v) {
        std::cout << v.to_string() << std::endl;
    }

    Value cpp_unescape_string(Environment&, const std::vector<Value>& args) {
        const std::string input = args.empty() ? std::string() : args[0].to_string();
        std::string decoded;
        decoded.reserve(input.size());
        for (size_t i = 0; i < input.size(); ++i) {
            if (input[i] != '\\' || i + 1 >= input.size()) {
                decoded += input[i];
                continue;
            }
            switch (input[++i]) {
                case 'n': decoded += '\n'; break;
                case 'r': decoded += '\r'; break;
                case 't': decoded += '\t'; break;
                case '\\': decoded += '\\'; break;
                case '"': decoded += '"'; break;
                default:
                    decoded += '\\';
                    decoded += input[i];
                    break;
            }
        }
        return Value::from_string(decoded);
    }

    Value cpp_escape_string(Environment&, const std::vector<Value>& args) {
        const std::string input = args.empty() ? std::string() : args[0].to_string();
        std::string escaped;
        escaped.reserve(input.size());
        for (char character : input) {
            switch (character) {
                case '\\': escaped += "\\\\"; break;
                case '"': escaped += "\\\""; break;
                case '\n': escaped += "\\n"; break;
                case '\r': escaped += "\\r"; break;
                case '\t': escaped += "\\t"; break;
                default: escaped += character; break;
            }
        }
        return Value::from_string(escaped);
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

    // -------------------------
    // String functions
    // -------------------------
    Value string_length(const Value& s) {
        std::string str = s.to_string();
        return Value::from_double(static_cast<double>(str.length()));
    }

    Value substring(const Value& s, const Value& start, const Value& end) {
        std::string str = s.to_string();
        size_t startIdx = static_cast<size_t>(start.num.value);
        size_t endIdx = static_cast<size_t>(end.num.value);
        if (startIdx > str.length()) startIdx = str.length();
        if (endIdx > str.length()) endIdx = str.length();
        return Value::from_string(str.substr(startIdx, endIdx - startIdx));
    }

    Value char_at(const Value& s, const Value& index) {
        std::string str = s.to_string();
        size_t idx = static_cast<size_t>(index.num.value);
        if (idx >= str.length()) {
            // Return empty string instead of throwing - needed for self-hosting loops
            return Value::from_string("");
        }
        return Value::from_string(std::string(1, str[idx]));
    }

    Value string_split(const Value& s, const Value& delimiter) {
        std::string str = s.to_string();
        std::string delim = delimiter.to_string();
        List result;
        if (delim.empty()) {
            result.push_back(s);
            return Value::from_list(result);
        }
        size_t start = 0;
        size_t end = str.find(delim);
        while (end != std::string::npos) {
            result.push_back(Value::from_string(str.substr(start, end - start)));
            start = end + delim.length();
            end = str.find(delim, start);
        }
        result.push_back(Value::from_string(str.substr(start)));
        return Value::from_list(result);
    }

    Value string_trim(const Value& s) {
        std::string str = s.to_string();
        size_t start = str.find_first_not_of(" \t\n\r");
        if (start == std::string::npos) return Value::from_string("");
        size_t end = str.find_last_not_of(" \t\n\r");
        return Value::from_string(str.substr(start, end - start + 1));
    }

    Value string_join(const Value& lst, const Value& delimiter) {
        if (lst.kind != ValueKind::List) {
            throw std::runtime_error("Expected a list for join");
        }
        std::string delim = delimiter.to_string();
        std::string result;
        for (size_t i = 0; i < lst.lst.size(); i++) {
            if (i > 0) result += delim;
            result += lst.lst[i].to_string();
        }
        return Value::from_string(result);
    }

    // -------------------------
    // List functions
    // -------------------------
    Value list_length(const Value& lst) {
        if (lst.kind != ValueKind::List) {
            throw std::runtime_error("Expected a list");
        }
        return Value::from_double(static_cast<double>(lst.lst.size()));
    }

    Value list_append(const Value& lst, const Value& element) {
        if (lst.kind != ValueKind::List) {
            throw std::runtime_error("Expected a list");
        }
        List result = lst.lst;
        result.push_back(element);
        return Value::from_list(result);
    }

    Value list_index(const Value& lst, const Value& index) {
        if (lst.kind != ValueKind::List) {
            throw std::runtime_error("Expected a list");
        }
        size_t idx = static_cast<size_t>(index.num.value);
        if (idx >= lst.lst.size()) {
            // Return empty string instead of throwing - needed for self-hosting loops
            return Value::from_string("");
        }
        return lst.lst[idx];
    }

    // -------------------------
    // Map functions
    // -------------------------
    Value map_get(const Value& mp, const Value& key) {
        if (mp.kind != ValueKind::Map) {
            throw std::runtime_error("Expected a map");
        }
        std::string keyStr = key.to_string();
        auto it = mp.mp.find(keyStr);
        if (it == mp.mp.end()) {
            // Return empty string instead of throwing - needed for self-hosting (optional map keys)
            return Value::from_string("");
        }
        return it->second;
    }

    Value map_set(const Value& mp, const Value& key, const Value& value) {
        if (mp.kind != ValueKind::Map) {
            throw std::runtime_error("Expected a map");
        }
        Map result = mp.mp;
        std::string keyStr = key.to_string();
        result[keyStr] = value;
        return Value::from_map(result);
    }

    // -------------------------
    // Math functions
    // -------------------------
    Value math_min(const Value& a, const Value& b) {
        return Value::from_double(std::min(a.num.value, b.num.value));
    }

    Value math_max(const Value& a, const Value& b) {
        return Value::from_double(std::max(a.num.value, b.num.value));
    }

    Value math_abs(const Value& a) {
        return Value::from_double(std::abs(a.num.value));
    }

    Value math_round(const Value& a) {
        return Value::from_double(std::round(a.num.value));
    }

    // -------------------------
    // String utility functions
    // -------------------------
    Value string_toupper(const Value& s) {
        std::string str = s.to_string();
        std::transform(str.begin(), str.end(), str.begin(), ::toupper);
        return Value::from_string(str);
    }

    Value string_tolower(const Value& s) {
        std::string str = s.to_string();
        std::transform(str.begin(), str.end(), str.begin(), ::tolower);
        return Value::from_string(str);
    }

    Value string_startswith(const Value& s, const Value& prefix) {
        std::string str = s.to_string();
        std::string pref = prefix.to_string();
        bool result = str.rfind(pref, 0) == 0;
        return Value::from_double(result ? 1.0 : 0.0);
    }

    Value string_endswith(const Value& s, const Value& suffix) {
        std::string str = s.to_string();
        std::string suff = suffix.to_string();
        bool result = str.size() >= suff.size() && str.compare(str.size() - suff.size(), suff.size(), suff) == 0;
        return Value::from_double(result ? 1.0 : 0.0);
    }

    Value string_isdigit(const Value& s) {
        std::string str = s.to_string();
        bool result = str.length() == 1 && std::isdigit(static_cast<unsigned char>(str[0]));
        return Value::from_double(result ? 1.0 : 0.0);
    }

    Value string_isletter(const Value& s) {
        std::string str = s.to_string();
        bool result = str.length() == 1 && std::isalpha(static_cast<unsigned char>(str[0]));
        return Value::from_double(result ? 1.0 : 0.0);
    }

    Value string_iswhitespace(const Value& s) {
        std::string str = s.to_string();
        bool result = str.length() == 1 && std::isspace(static_cast<unsigned char>(str[0]));
        return Value::from_double(result ? 1.0 : 0.0);
    }

    Value string_replace(const Value& s, const Value& old, const Value& new_) {
        std::string str = s.to_string();
        std::string oldStr = old.to_string();
        std::string newStr = new_.to_string();
        size_t pos = 0;
        while ((pos = str.find(oldStr, pos)) != std::string::npos) {
            str.replace(pos, oldStr.length(), newStr);
            pos += newStr.length();
        }
        return Value::from_string(str);
    }

    Value string_indexof(const Value& s, const Value& substr) {
        std::string str = s.to_string();
        std::string sub = substr.to_string();
        size_t pos = str.find(sub);
        if (pos == std::string::npos) return Value::from_double(-1.0);
        return Value::from_double(static_cast<double>(pos));
    }

    bool value_equals(const Value& a, const Value& b) {
        if (a.kind == b.kind) {
            if (a.kind == ValueKind::Number) return a.num.value == b.num.value;
            if (a.kind == ValueKind::String) return a.str.value == b.str.value;
            if (a.kind == ValueKind::List) return a.lst == b.lst;
            if (a.kind == ValueKind::Map) return a.mp == b.mp;
        }
        return false;
    }

    // -------------------------
    // File I/O functions
    // -------------------------
    Value file_read(const std::string& path) {
        std::ifstream infile(path);
        if (!infile.is_open()) {
            throw std::runtime_error("Cannot open file for reading: " + path);
        }
        std::stringstream ss;
        ss << infile.rdbuf();
        return Value::from_string(ss.str());
    }

    void file_write(const std::string& path, const Value& value) {
        std::ofstream outfile(path);
        if (!outfile.is_open()) {
            throw std::runtime_error("Cannot open file for writing: " + path);
        }
        outfile << value.to_string();
    }

    Value ms_std_println(Environment&, const std::vector<Value>& args) {
        print(args.at(0));
        return Value::from_double(0);
    }

    Value ms_std_greet(Environment&, const std::vector<Value>& args) {
        print(Value::from_string("Hello, "));
        print(args.at(0));
        return Value::from_double(0);
    }

    Value ms_std_add_and_print(Environment&, const std::vector<Value>& args) {
        print(Value::from_double(args.at(0).num.value + args.at(1).num.value));
        return Value::from_double(0);
    }

    Value ms_std_repeat(Environment&, const std::vector<Value>& args) {
        const int count = std::max(0, static_cast<int>(args.at(0).num.value));
        for (int i = 0; i < count; ++i) {
            print(args.at(1));
        }
        return Value::from_double(0);
    }

    Value ms_std_min(Environment&, const std::vector<Value>& args) {
        return math_min(args.at(0), args.at(1));
    }

    Value ms_std_max(Environment&, const std::vector<Value>& args) {
        return math_max(args.at(0), args.at(1));
    }

    Value ms_std_abs(Environment&, const std::vector<Value>& args) {
        return math_abs(args.at(0));
    }

    Value ms_std_round(Environment&, const std::vector<Value>& args) {
        return math_round(args.at(0));
    }

    Value ms_std_toupper(Environment&, const std::vector<Value>& args) {
        return string_toupper(args.at(0));
    }

    Value ms_std_tolower(Environment&, const std::vector<Value>& args) {
        return string_tolower(args.at(0));
    }

    Value ms_std_startsWith(Environment&, const std::vector<Value>& args) {
        return string_startswith(args.at(0), args.at(1));
    }

    Value ms_std_endsWith(Environment&, const std::vector<Value>& args) {
        return string_endswith(args.at(0), args.at(1));
    }

    Value ms_std_isDigit(Environment&, const std::vector<Value>& args) {
        return string_isdigit(args.at(0));
    }

    Value ms_std_isLetter(Environment&, const std::vector<Value>& args) {
        return string_isletter(args.at(0));
    }

    Value ms_std_isWhitespace(Environment&, const std::vector<Value>& args) {
        return string_iswhitespace(args.at(0));
    }

    Value ms_std_readFile(Environment&, const std::vector<Value>& args) {
        return file_read(args.at(0).to_string());
    }

    Value ms_std_length(Environment&, const std::vector<Value>& args) {
        return string_length(args.at(0));
    }

    Value ms_std_charAt(Environment&, const std::vector<Value>& args) {
        return char_at(args.at(0), args.at(1));
    }

    Value ms_std_substring(Environment&, const std::vector<Value>& args) {
        return ms::substring(args.at(0), args.at(1), args.at(2));
    }

    Value ms_std_split(Environment&, const std::vector<Value>& args) {
        return string_split(args.at(0), args.at(1));
    }

    Value ms_std_join(Environment&, const std::vector<Value>& args) {
        return string_join(args.at(0), args.at(1));
    }

    Value ms_std_trim(Environment&, const std::vector<Value>& args) {
        return string_trim(args.at(0));
    }

    Value ms_std_replace(Environment&, const std::vector<Value>& args) {
        return string_replace(args.at(0), args.at(1), args.at(2));
    }

    Value ms_std_size(Environment&, const std::vector<Value>& args) {
        return list_length(args.at(0));
    }

    Value ms_std_append(Environment&, const std::vector<Value>& args) {
        return list_append(args.at(1), args.at(0));
    }

    Value ms_std_getItem(Environment&, const std::vector<Value>& args) {
        return list_index(args.at(1), args.at(0));
    }

    Value ms_std_mapSet(Environment&, const std::vector<Value>& args) {
        return map_set(args.at(0), args.at(1), args.at(2));
    }

    Value ms_std_mapGet(Environment&, const std::vector<Value>& args) {
        return map_get(args.at(1), args.at(0));
    }

    Value ms_std_indexOf(Environment&, const std::vector<Value>& args) {
        return string_indexof(args.at(0), args.at(1));
    }

}
