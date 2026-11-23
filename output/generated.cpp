#include "midshake_runtime.hpp"
using namespace ms;

int main() {
    Environment env;
    env.set("text", Value::from_string("HellofromMidShake!"));
    file_write("output.txt", env.get("text"));
    print(Value::from_string("Done."));
    return 0;
}