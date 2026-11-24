#include "midshake_runtime.hpp"
using namespace ms;

Value println(Environment& env, const std::vector<Value>& args) {
    env.set("x", args[0]);
    print(env.get("x"));
    return Value::from_double(0);
}

Value greet(Environment& env, const std::vector<Value>& args) {
    env.set("name", args[0]);
    print(Value::from_string("Hello, "));
    print(env.get("name"));
    return Value::from_double(0);
}

Value add_and_print(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("b", args[1]);
    print((env.get("a") + env.get("b")));
    return Value::from_double(0);
}

Value repeat(Environment& env, const std::vector<Value>& args) {
    env.set("count", args[0]);
    env.set("message", args[1]);
    env.set("i", Value::from_double(0));
    while (Value(Number((env.get("i").num.value < env.get("count").num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("message"));
        env.set("i", (env.get("i") + Value::from_double(1)));
    }
    return Value::from_double(0);
}

Value min(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("b", args[1]);
    env.set("result", math_min(env.get("a"), env.get("b")));
    return env.get("result");
    return Value::from_double(0);
}

Value max(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("b", args[1]);
    env.set("result", math_max(env.get("a"), env.get("b")));
    return env.get("result");
    return Value::from_double(0);
}

Value abs(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("result", math_abs(env.get("a")));
    return env.get("result");
    return Value::from_double(0);
}

Value round(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("result", math_round(env.get("a")));
    return env.get("result");
    return Value::from_double(0);
}

Value toupper(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_toupper(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value tolower(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_tolower(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value startsWith(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("prefix", args[1]);
    env.set("result", string_startswith(env.get("s"), env.get("prefix")));
    return env.get("result");
    return Value::from_double(0);
}

Value endsWith(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("suffix", args[1]);
    env.set("result", string_endswith(env.get("s"), env.get("suffix")));
    return env.get("result");
    return Value::from_double(0);
}

Value isDigit(Environment& env, const std::vector<Value>& args) {
    env.set("c", args[0]);
    env.set("result", string_isdigit(env.get("c")));
    return env.get("result");
    return Value::from_double(0);
}

Value isLetter(Environment& env, const std::vector<Value>& args) {
    env.set("c", args[0]);
    env.set("result", string_isletter(env.get("c")));
    return env.get("result");
    return Value::from_double(0);
}

Value isWhitespace(Environment& env, const std::vector<Value>& args) {
    env.set("c", args[0]);
    env.set("result", string_iswhitespace(env.get("c")));
    return env.get("result");
    return Value::from_double(0);
}

Value readFile(Environment& env, const std::vector<Value>& args) {
    env.set("path", args[0]);
    env.set("result", file_read(env.get("path").to_string()));
    return env.get("result");
    return Value::from_double(0);
}

Value length(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_length(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value charAt(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("index", args[1]);
    env.set("result", char_at(env.get("s"), env.get("index")));
    return env.get("result");
    return Value::from_double(0);
}

Value substring(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("start", args[1]);
    env.set("end", args[2]);
    env.set("result", substring(env.get("s"), env.get("start"), env.get("end")));
    return env.get("result");
    return Value::from_double(0);
}

Value split(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("delimiter", args[1]);
    env.set("result", string_split(env.get("s"), env.get("delimiter")));
    return env.get("result");
    return Value::from_double(0);
}

Value join(Environment& env, const std::vector<Value>& args) {
    env.set("list", args[0]);
    env.set("delimiter", args[1]);
    env.set("result", string_join(env.get("list"), env.get("delimiter")));
    return env.get("result");
    return Value::from_double(0);
}

Value trim(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_trim(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value replace(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("old", args[1]);
    env.set("new", args[2]);
    env.set("result", string_replace(env.get("s"), env.get("old"), env.get("new")));
    return env.get("result");
    return Value::from_double(0);
}

Value size(Environment& env, const std::vector<Value>& args) {
    env.set("list", args[0]);
    env.set("result", list_length(env.get("list")));
    return env.get("result");
    return Value::from_double(0);
}

Value append(Environment& env, const std::vector<Value>& args) {
    env.set("element", args[0]);
    env.set("list", args[1]);
    env.set("result", list_append(env.get("list"), env.get("element")));
    return env.get("result");
    return Value::from_double(0);
}

Value getItem(Environment& env, const std::vector<Value>& args) {
    env.set("index", args[0]);
    env.set("list", args[1]);
    env.set("result", list_index(env.get("list"), env.get("index")));
    return env.get("result");
    return Value::from_double(0);
}

Value mapSet(Environment& env, const std::vector<Value>& args) {
    env.set("map", args[0]);
    env.set("key", args[1]);
    env.set("value", args[2]);
    env.set("the value of map", map_set(env.get("the value of map"), env.get("key"), env.get("value")));
    return env.get("map");
    return Value::from_double(0);
}

Value mapGet(Environment& env, const std::vector<Value>& args) {
    env.set("key", args[0]);
    env.set("map", args[1]);
    env.set("result", map_get(env.get("map"), env.get("key")));
    return env.get("result");
    return Value::from_double(0);
}

Value indexOf(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("substr", args[1]);
    env.set("result", string_indexof(env.get("s"), env.get("substr")));
    return env.get("result");
    return Value::from_double(0);
}

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("testStr", Value::from_string("the string Done."));
    print(Value::from_string("Testing startsWith:"));
    {
        std::vector<Value> args;
        args.push_back(env.get("testStr"));
        args.push_back(Value::from_string("the string"));
        env.set("RESPONSE", startsWith(env, args));
    }
    print(env.get("RESPONSE"));
    env.set("testStr2", Value::from_string("the string Done."));
    print(Value::from_string("Testing startsWith 2:"));
    {
        std::vector<Value> args;
        args.push_back(env.get("testStr2"));
        args.push_back(Value::from_string("the string"));
        env.set("RESPONSE", startsWith(env, args));
    }
    print(env.get("RESPONSE"));
    return 0;
}