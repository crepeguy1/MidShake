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
    print(Value(Number(env.get("a").num.value + env.get("b").num.value)));
    return Value::from_double(0);
}

Value repeat(Environment& env, const std::vector<Value>& args) {
    env.set("count", args[0]);
    env.set("message", args[1]);
    env.set("i", Value::from_double(0));
    while (Value(Number((env.get("i").num.value < env.get("count").num.value) ? 1 : 0)).num.value != 0) {
        env.set("i", Value(Number(env.get("i").num.value + Value::from_double(1).num.value)));
    }
    return Value::from_double(0);
}

/*
int main() {
    Environment env;
    return 0;
}*/