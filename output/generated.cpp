    env.set("g_lines", env.get("[]"));
    env.set("g_pos", Value::from_double(0));
    env.set("g_lineCount", Value::from_double(0));
    env.set("g_out", env.get("[]"));
    env.set("g_indent", Value::from_double(0));
    env.set("g_funcs", env.get("[]"));
    env.set("g_idx", Value::from_double(0));
    env.set("g_compiled", env.get(""""));
void wrapQuote(Environment& env) {
}
void emit(Environment& env) {
}
void compileVal(Environment& env) {
}
void extractLetName(Environment& env) {
}
    env.set("g_name", env.get(""""));
void compileStmt(Environment& env) {
}
    env.set("argCount", env.get("the size of ARGV"));
    env.set("filePath", env.get(""selfhost/minicodegen.mish""));
    getI(env);
    env.set("source", env.get("the content of the file the value of filePath"));
    sp(env);
    env.set("sourceLines", env.get("the RESPONSE"));
    compileS(env);
    e(env);
    e(env);
    e(env);
    e(env);
    e(env);
    env.set("cppOutput", env.get(""""));
    env.set("outCount", env.get("the size of g_out"));
    getI(env);
    env.set("outLine", env.get("the RESPONSE"));
    e(env);
    e(env);
    env.set("finalOut", env.get(""""));
    env.set("outCount2", env.get("the size of g_out"));
    getI(env);
    env.set("line", env.get("the RESPONSE"));
    print(Value::from_string("Compilation complete! Generated "));
    print(env.get("the size of g_out"));
    print(Value::from_string(" lines of C++."));
#include "midshake_runtime.hpp"
using namespace ms;

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    return 0;
}