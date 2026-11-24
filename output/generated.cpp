#include "midshake_runtime.hpp"
using namespace ms;

int main() {
    Environment env;
    env.set("x", Value::from_double(10));
    env.set("light", Value::from_string("on"));
    print(env.get("x"));
    print(env.get("light"));
    if ((env.get("x").num.value > Value::from_double(5).num.value)) {
        print(env.get("light"));
    }
    return Value::from_double(0);
    return 0;
}