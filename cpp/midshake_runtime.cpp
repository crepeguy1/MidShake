#include "midshake_runtime.hpp"
#include <sstream>
#include <algorithm>
#include <cctype>
#include <cmath>

namespace ms {

    // -------------------------
    // print
    // -------------------------
    void print(const Value& v) {
        std::cout << v.to_string() << std::endl;
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
            throw std::runtime_error("Character index out of range");
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
            throw std::runtime_error("List index out of range");
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
            throw std::runtime_error("Key not found in map: " + keyStr);
        }
        return it->second;
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

}
