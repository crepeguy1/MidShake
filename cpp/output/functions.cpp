#include "midshake_runtime.hpp"
using namespace ms;

Value greet(Environment& env, const std::vector<Value>& args) {
    env.set("name", args[0]);
    print(Value::from_string("Hello, "));
    print(env.get("name"));
    return Value::from_double(0);
}

int main() {
    Environment env;
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("adam"));
        env.set("RESPONSE", greet(env, args));
    }
    return 0;
}