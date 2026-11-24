#include "midshake_runtime.hpp"
using namespace ms;

int main() {
    Environment env;
    env.set("x", Value::from_double(10));
    env.set("light", Value::from_string("on"));
    print(env.get("x"));
    print(env.get("light"));
    if (Value(Number((env.get("x").num.value > Value::from_double(5).num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("light"));
    }
    else {
        return 0;
    }
    return 0;
}