#include "midshake_runtime.hpp"
using namespace ms;

int main() {
    Environment env;
    file_write("tests/output_test.txt", Value::from_string("Hello from MidShake!"));
    env.set("contents", file_read("tests/output_test.txt"));
    print(env.get("contents"));
    env.set("data", file_read("tests/test_fileio_data.txt"));
    print(env.get("data"));
    env.set("number", Value::from_double(42));
    file_write("tests/number_output.txt", env.get("number"));
    env.set("numback", file_read("tests/number_output.txt"));
    print(env.get("numback"));
    file_write("tests/combined_test.txt", Value::from_string("Line oneLine two"));
    env.set("combined", file_read("tests/combined_test.txt"));
    print(env.get("combined"));
    env.set("filedata", file_read("tests/test_fileio_data.txt"));
    env.set("filelen", string_length(env.get("filedata")));
    print(env.get("filelen"));
    return 0;
}