#include "midshake_runtime.hpp"
using namespace ms;

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("x", Value::from_double(3));
    if (Value(Number((env.get("x").num.value > Value::from_double(5).num.value) ? 1 : 0)).num.value != 0) {
        print(Value::from_string("big"));
    }
    else {
        print(Value::from_string("small"));
    }
    return 0;
}