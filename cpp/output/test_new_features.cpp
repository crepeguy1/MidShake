#include "midshake_runtime.hpp"
using namespace ms;

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("isTrue", Value::from_double(1));
    env.set("isFalse", Value::from_double(0));
    print(env.get("isTrue"));
    print(env.get("isFalse"));
    env.set("fruits", Value::from_list({Value::from_string("apple"), Value::from_string("banana"), Value::from_string("cherry")}));
    print(Value::from_string("--- For loop ---"));
    for (const auto& fruit : env.get("fruits").lst) {
        env.set("fruit", fruit);
        print(env.get("fruit"));
    }
    env.set("i", Value::from_double(0));
    env.set("count", Value::from_double(10));
    print(Value::from_string("--- Break test ---"));
    while (Value(Number((env.get("i").num.value < env.get("count").num.value) ? 1 : 0)).num.value != 0) {
        if (Value(Number(value_equals(env.get("i"), Value::from_double(5)) ? 1 : 0)).num.value != 0) {
            break;
        }
        print(env.get("i"));
        env.set("i", (env.get("i") + Value::from_double(1)));
    }
    print(Value::from_string("--- Continue test ---"));
    env.set("j", Value::from_double(0));
    while (Value(Number((env.get("j").num.value < Value::from_double(5).num.value) ? 1 : 0)).num.value != 0) {
        env.set("j", (env.get("j") + Value::from_double(1)));
        if (Value(Number(value_equals(env.get("j"), Value::from_double(3)) ? 1 : 0)).num.value != 0) {
            continue;
        }
        print(env.get("j"));
    }
    env.set("myMap", Value::from_map({{Value::from_string("name").to_string(), Value::from_string("Alice")}, {Value::from_string("age").to_string(), Value::from_double(30)}}));
    env.set("myMap", map_set(env.get("myMap"), Value::from_string("city"), Value::from_string("New York")));
    print(Value::from_string("--- Map set test ---"));
    print(map_get(env.get("myMap"), Value::from_string("name")));
    print(map_get(env.get("myMap"), Value::from_string("city")));
    print(Value::from_string("--- Break in for loop ---"));
    for (const auto& num : Value::from_list({Value::from_double(1), Value::from_double(2), Value::from_double(3), Value::from_double(4), Value::from_double(5), Value::from_double(6), Value::from_double(7), Value::from_double(8), Value::from_double(9), Value::from_double(10)}).lst) {
        env.set("num", num);
        if (Value(Number(value_equals(env.get("num"), Value::from_double(6)) ? 1 : 0)).num.value != 0) {
            break;
        }
        print(env.get("num"));
    }
    print(Value::from_string("--- Continue in for loop ---"));
    for (const auto& item : Value::from_list({Value::from_string("one"), Value::from_string("two"), Value::from_string("skip"), Value::from_string("four"), Value::from_string("skip"), Value::from_string("six")}).lst) {
        env.set("item", item);
        if (Value(Number(value_equals(env.get("item"), Value::from_string("skip")) ? 1 : 0)).num.value != 0) {
            continue;
        }
        print(env.get("item"));
    }
    print(Value::from_string("All tests passed!"));
    return 0;
}