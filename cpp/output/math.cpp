#include "midshake_runtime.hpp"
using namespace ms;

int main() {
    Environment env;
    env.set("minval", math_min(Value::from_double(5), Value::from_double(10)));
    print(env.get("minval"));
    env.set("minval2", math_min(Value::from_double(-3), Value::from_double(7)));
    print(env.get("minval2"));
    env.set("maxval", math_max(Value::from_double(5), Value::from_double(10)));
    print(env.get("maxval"));
    env.set("maxval2", math_max(Value::from_double(-3), Value::from_double(7)));
    print(env.get("maxval2"));
    env.set("absval", math_abs(Value::from_double(-42)));
    print(env.get("absval"));
    env.set("absval2", math_abs(Value::from_double(42)));
    print(env.get("absval2"));
    env.set("rounded", math_round(Value::from_double(3.7)));
    print(env.get("rounded"));
    env.set("rounded2", math_round(Value::from_double(2.3)));
    print(env.get("rounded2"));
    env.set("a", Value::from_double(15));
    env.set("b", Value::from_double(25));
    env.set("result", math_max(env.get("a"), env.get("b")));
    print(env.get("result"));
    return 0;
}