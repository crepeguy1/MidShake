#include "midshake_runtime.hpp"
using namespace ms;

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("mylist", Value::from_list({Value::from_double(1), Value::from_double(2), Value::from_double(3)}));
    print(env.get("mylist"));
    env.set("first", list_index(env.get("mylist"), Value::from_double(0)));
    print(env.get("first"));
    env.set("size", list_length(env.get("mylist")));
    print(env.get("size"));
    env.set("extended", list_append(env.get("mylist"), Value::from_double(4)));
    print(env.get("extended"));
    env.set("mymap", Value::from_map({{Value::from_string("name").to_string(), Value::from_string("Alice")}, {Value::from_string("age").to_string(), Value::from_double(30)}}));
    print(env.get("mymap"));
    env.set("name", map_get(env.get("mymap"), Value::from_string("name")));
    print(env.get("name"));
    env.set("age", map_get(env.get("mymap"), Value::from_string("age")));
    print(env.get("age"));
    env.set("greeting", Value::from_string("Hello, World!"));
    env.set("len", string_length(env.get("greeting")));
    print(env.get("len"));
    env.set("sub", substring(env.get("greeting"), Value::from_double(0), Value::from_double(5)));
    print(env.get("sub"));
    env.set("ch", char_at(env.get("greeting"), Value::from_double(7)));
    print(env.get("ch"));
    env.set("trimmed", string_trim(Value::from_string("  hello  ")));
    print(env.get("trimmed"));
    env.set("words", string_split(Value::from_string("one,two,three"), Value::from_string(",")));
    print(env.get("words"));
    env.set("joined", string_join(env.get("words"), Value::from_string(" - ")));
    print(env.get("joined"));
    env.set("fruits", Value::from_list({Value::from_string("apple"), Value::from_string("banana"), Value::from_string("cherry")}));
    print(env.get("fruits"));
    env.set("fruitCount", list_length(env.get("fruits")));
    print(env.get("fruitCount"));
    env.set("firstFruit", list_index(env.get("fruits"), Value::from_double(0)));
    print(env.get("firstFruit"));
    env.set("moreFruits", list_append(env.get("fruits"), Value::from_string("date")));
    print(env.get("moreFruits"));
    print(Value::from_string("All tests passed!"));
    return 0;
}