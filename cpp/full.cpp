#include "midshake_runtime.hpp"
#include "stdlib.hpp"
using namespace ms;

int main() {
    Environment env;
    env.set("name", Value::from_string("example name"));
    {
        std::vector<Value> args;
        args.push_back(env.get("name"));
        greet(env, args);
    }
    env.set("RESPONSE", inquire_number("How many times should I say hi?"));
    env.set("times", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("times"));
        args.push_back(Value::from_string("Hi from MidShake!"));
        repeat(env, args);
    }
    env.set("RESPONSE", inquire_number("Give me a number:"));
    env.set("x", env.get("RESPONSE"));
    env.set("RESPONSE", inquire_number("Give me another number:"));
    env.set("y", env.get("RESPONSE"));
    print(Value::from_string("The sum of your numbers is:"));
    {
        std::vector<Value> args;
        args.push_back(env.get("x"));
        args.push_back(env.get("y"));
        add_and_print(env, args);
    }
    print(Value::from_string("All done. Goodbye!"));
    return 0;
}