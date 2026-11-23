#include "midshake_runtime.hpp"
#include <sstream>
#include <algorithm>
#include <cctype>
#include <cmath>
#include <fstream>

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
            throw std::runtime_error("Key not found in map: " + keyStr);
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

}
