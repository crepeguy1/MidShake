#include "midshake_runtime.hpp"
using namespace ms;

Value increment(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    env.set("counter", (env.get("counter") + Value::from_double(1)));
    return Value::from_double(0);
}

Value addItem(Environment& env, const std::vector<Value>& args) {
    env.set("item", args[0]);
    env.set("items", list_append(env.get("items"), env.get("item")));
    return Value::from_double(0);
}

Value addUp(Environment& env, const std::vector<Value>& args) {
    env.set("x", args[0]);
    if (Value(Number((env.get("x").num.value <= Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        return Value::from_double(0);
    }
    env.set("sum", (env.get("sum") + env.get("x")));
    {
        std::vector<Value> args;
        args.push_back(Value(Number(env.get("x").num.value - Value::from_double(1).num.value)));
        env.set("RESPONSE", addUp(env, args));
    }
    return Value::from_double(0);
}

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("counter", Value::from_double(0));
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", increment(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", increment(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", increment(env, args));
    }
    print(Value::from_string("Counter after 3 increments:"));
    print(env.get("counter"));
    env.set("items", Value::from_list({}));
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("apple"));
        env.set("RESPONSE", addItem(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("banana"));
        env.set("RESPONSE", addItem(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("cherry"));
        env.set("RESPONSE", addItem(env, args));
    }
    print(Value::from_string("Items:"));
    print(env.get("items"));
    print(Value::from_string("Item count:"));
    print(list_length(env.get("items")));
    env.set("sum", Value::from_double(0));
    env.set("n", Value::from_double(5));
    {
        std::vector<Value> args;
        args.push_back(env.get("n"));
        env.set("RESPONSE", addUp(env, args));
    }
    print(Value::from_string("Sum 1 to 5:"));
    print(env.get("sum"));
    return 0;
}