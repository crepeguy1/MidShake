#include "midshake_runtime.hpp"
using namespace ms;

Value println(Environment& env, const std::vector<Value>& args) {
    env.set("x", args[0]);
    print(env.get("x"));
    return Value::from_double(0);
}

Value greet(Environment& env, const std::vector<Value>& args) {
    env.set("name", args[0]);
    print(Value::from_string("Hello, "));
    print(env.get("name"));
    return Value::from_double(0);
}

Value add_and_print(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("b", args[1]);
    print((env.get("a") + env.get("b")));
    return Value::from_double(0);
}

Value repeat(Environment& env, const std::vector<Value>& args) {
    env.set("count", args[0]);
    env.set("message", args[1]);
    env.set("i", Value::from_double(0));
    while (Value(Number((env.get("i").num.value < env.get("count").num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("message"));
        env.set("i", (env.get("i") + Value::from_double(1)));
    }
    return Value::from_double(0);
}

Value min(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("b", args[1]);
    env.set("result", math_min(env.get("a"), env.get("b")));
    return env.get("result");
    return Value::from_double(0);
}

Value max(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("b", args[1]);
    env.set("result", math_max(env.get("a"), env.get("b")));
    return env.get("result");
    return Value::from_double(0);
}

Value abs(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("result", math_abs(env.get("a")));
    return env.get("result");
    return Value::from_double(0);
}

Value round(Environment& env, const std::vector<Value>& args) {
    env.set("a", args[0]);
    env.set("result", math_round(env.get("a")));
    return env.get("result");
    return Value::from_double(0);
}

Value toupper(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_toupper(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value tolower(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_tolower(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value startsWith(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("prefix", args[1]);
    env.set("result", string_startswith(env.get("s"), env.get("prefix")));
    return env.get("result");
    return Value::from_double(0);
}

Value endsWith(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("suffix", args[1]);
    env.set("result", string_endswith(env.get("s"), env.get("suffix")));
    return env.get("result");
    return Value::from_double(0);
}

Value isDigit(Environment& env, const std::vector<Value>& args) {
    env.set("c", args[0]);
    env.set("result", string_isdigit(env.get("c")));
    return env.get("result");
    return Value::from_double(0);
}

Value isLetter(Environment& env, const std::vector<Value>& args) {
    env.set("c", args[0]);
    env.set("result", string_isletter(env.get("c")));
    return env.get("result");
    return Value::from_double(0);
}

Value isWhitespace(Environment& env, const std::vector<Value>& args) {
    env.set("c", args[0]);
    env.set("result", string_iswhitespace(env.get("c")));
    return env.get("result");
    return Value::from_double(0);
}

Value readFile(Environment& env, const std::vector<Value>& args) {
    env.set("path", args[0]);
    env.set("result", file_read(env.get("path").to_string()));
    return env.get("result");
    return Value::from_double(0);
}

Value length(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_length(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value charAt(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("index", args[1]);
    env.set("result", char_at(env.get("s"), env.get("index")));
    return env.get("result");
    return Value::from_double(0);
}

Value substring(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("start", args[1]);
    env.set("end", args[2]);
    env.set("result", substring(env.get("s"), env.get("start"), env.get("end")));
    return env.get("result");
    return Value::from_double(0);
}

Value split(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("delimiter", args[1]);
    env.set("result", string_split(env.get("s"), env.get("delimiter")));
    return env.get("result");
    return Value::from_double(0);
}

Value join(Environment& env, const std::vector<Value>& args) {
    env.set("list", args[0]);
    env.set("delimiter", args[1]);
    env.set("result", string_join(env.get("list"), env.get("delimiter")));
    return env.get("result");
    return Value::from_double(0);
}

Value trim(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("result", string_trim(env.get("s")));
    return env.get("result");
    return Value::from_double(0);
}

Value replace(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("old", args[1]);
    env.set("new", args[2]);
    env.set("result", string_replace(env.get("s"), env.get("old"), env.get("new")));
    return env.get("result");
    return Value::from_double(0);
}

Value size(Environment& env, const std::vector<Value>& args) {
    env.set("list", args[0]);
    env.set("result", list_length(env.get("list")));
    return env.get("result");
    return Value::from_double(0);
}

Value append(Environment& env, const std::vector<Value>& args) {
    env.set("element", args[0]);
    env.set("list", args[1]);
    env.set("result", list_append(env.get("list"), env.get("element")));
    return env.get("result");
    return Value::from_double(0);
}

Value getItem(Environment& env, const std::vector<Value>& args) {
    env.set("index", args[0]);
    env.set("list", args[1]);
    env.set("result", list_index(env.get("list"), env.get("index")));
    return env.get("result");
    return Value::from_double(0);
}

Value mapSet(Environment& env, const std::vector<Value>& args) {
    env.set("map", args[0]);
    env.set("key", args[1]);
    env.set("value", args[2]);
    env.set("the value of map", map_set(env.get("the value of map"), env.get("key"), env.get("value")));
    return env.get("map");
    return Value::from_double(0);
}

Value mapGet(Environment& env, const std::vector<Value>& args) {
    env.set("key", args[0]);
    env.set("map", args[1]);
    env.set("result", map_get(env.get("map"), env.get("key")));
    return env.get("result");
    return Value::from_double(0);
}

Value indexOf(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("substr", args[1]);
    env.set("result", string_indexof(env.get("s"), env.get("substr")));
    return env.get("result");
    return Value::from_double(0);
}

Value wrapQuote(Environment& env, const std::vector<Value>& args) {
    env.set("s", args[0]);
    env.set("q", Value::from_string("\""));
    env.set("result", ((env.get("q") + env.get("s")) + env.get("q")));
    return env.get("result");
    return Value::from_double(0);
}

Value emit(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(env.get("g_out"));
        env.set("RESPONSE", append(env, args));
    }
    env.set("updated", env.get("RESPONSE"));
    env.set("g_out", env.get("updated"));
    return Value::from_double(1);
    return Value::from_double(0);
}

Value compileVal(Environment& env, const std::vector<Value>& args) {
    env.set("expr", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("expr"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("e", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("e"));
        args.push_back(Value::from_string("the string"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isStr", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isStr"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("e"));
            args.push_back(Value::from_double(10));
            args.push_back(string_length(env.get("e")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("s", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("s"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("s", env.get("RESPONSE"));
        env.set("g_compiled", ((Value::from_string("Value::from_string(") + env.get("s")) + Value::from_string(")")));
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("e"));
        args.push_back(Value::from_string("the number"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isNum", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isNum"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("e"));
            args.push_back(Value::from_double(10));
            args.push_back(string_length(env.get("e")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("n", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("n"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("n", env.get("RESPONSE"));
        env.set("g_compiled", ((Value::from_string("Value::from_double(") + env.get("n")) + Value::from_string(")")));
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("e"));
        args.push_back(Value::from_string("the value of"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isVal", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isVal"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("e"));
            args.push_back(Value::from_double(11));
            args.push_back(string_length(env.get("e")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("v", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("v"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("v", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("v"));
            env.set("RESPONSE", wrapQuote(env, args));
        }
        env.set("qv", env.get("RESPONSE"));
        env.set("g_compiled", ((Value::from_string("env.get(") + env.get("qv")) + Value::from_string(")")));
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("e"));
        env.set("RESPONSE", isDigit(env, args));
    }
    env.set("isDigit", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isDigit"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        env.set("g_compiled", ((Value::from_string("Value::from_double(") + env.get("e")) + Value::from_string(")")));
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("e"));
        env.set("RESPONSE", wrapQuote(env, args));
    }
    env.set("qe", env.get("RESPONSE"));
    env.set("g_compiled", ((Value::from_string("env.get(") + env.get("qe")) + Value::from_string(")")));
    return Value::from_double(1);
    return Value::from_double(0);
}

Value extractLetName(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("name", Value::from_string(""));
    env.set("found", Value::from_double(0));
    env.set("wi", Value::from_double(0));
    env.set("wc", list_length(env.get("words")));
    while (Value(Number((env.get("wi").num.value < env.get("wc").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("wi"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("w", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            env.set("name", env.get("w"));
            break;
        }
        if (Value(Number(value_equals(env.get("w"), Value::from_string("variable")) ? 1 : 0)).num.value != 0) {
            env.set("found", Value::from_double(1));
        }
        env.set("wi", (env.get("wi") + Value::from_double(1)));
    }
    env.set("g_name", env.get("name"));
    return Value::from_double(1);
    return Value::from_double(0);
}

Value compileStmt(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("g_pos"));
        args.push_back(env.get("g_lines"));
        env.set("RESPONSE", getItem(env, args));
    }
    env.set("line", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("t", env.get("RESPONSE"));
    if (Value(Number(value_equals(string_length(env.get("t")), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        return Value::from_double(0);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("t"));
        args.push_back(Value::from_string("LET"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isLet", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isLet"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("t"));
            env.set("RESPONSE", extractLetName(env, args));
        }
        env.set("name", env.get("g_name"));
        {
            std::vector<Value> args;
            args.push_back(env.get("t"));
            args.push_back(Value::from_string("BE"));
            env.set("RESPONSE", indexOf(env, args));
        }
        env.set("bePos", env.get("RESPONSE"));
        if (Value(Number((env.get("bePos").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("t"));
                args.push_back((env.get("bePos") + Value::from_double(2)));
                args.push_back(string_length(env.get("t")));
                env.set("RESPONSE", substring(env, args));
            }
            env.set("valStr", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("valStr"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("valStr", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("valStr"));
                args.push_back(Value::from_string(";"));
                env.set("RESPONSE", endsWith(env, args));
            }
            env.set("hasSemi", env.get("RESPONSE"));
            if (Value(Number(value_equals(env.get("hasSemi"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("valStr"));
                    args.push_back(Value::from_double(0));
                    args.push_back(Value(Number(string_length(env.get("valStr")).num.value - Value::from_double(1).num.value)));
                    env.set("RESPONSE", substring(env, args));
                }
                env.set("valStr", env.get("RESPONSE"));
            }
            {
                std::vector<Value> args;
                args.push_back(env.get("valStr"));
                env.set("RESPONSE", compileVal(env, args));
            }
            env.set("cv", env.get("g_compiled"));
            {
                std::vector<Value> args;
                args.push_back(env.get("name"));
                env.set("RESPONSE", wrapQuote(env, args));
            }
            env.set("qn", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(((((Value::from_string("    env.set(") + env.get("qn")) + Value::from_string(", ")) + env.get("cv")) + Value::from_string(");")));
                env.set("RESPONSE", emit(env, args));
            }
        }
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("t"));
        args.push_back(Value::from_string("PROCLAIM"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isProclaim", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isProclaim"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("t"));
            args.push_back(Value::from_double(8));
            args.push_back(string_length(env.get("t")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("valStr", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("valStr"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("valStr", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("valStr"));
            args.push_back(Value::from_string(";"));
            env.set("RESPONSE", endsWith(env, args));
        }
        env.set("hasSemi", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("hasSemi"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("valStr"));
                args.push_back(Value::from_double(0));
                args.push_back(Value(Number(string_length(env.get("valStr")).num.value - Value::from_double(1).num.value)));
                env.set("RESPONSE", substring(env, args));
            }
            env.set("valStr", env.get("RESPONSE"));
        }
        {
            std::vector<Value> args;
            args.push_back(env.get("valStr"));
            env.set("RESPONSE", compileVal(env, args));
        }
        env.set("cv", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("    print(") + env.get("cv")) + Value::from_string(");")));
            env.set("RESPONSE", emit(env, args));
        }
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("t"));
        args.push_back(Value::from_string("DEFINE"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isDef", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isDef"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("t"));
            args.push_back(Value::from_string(" "));
            env.set("RESPONSE", split(env, args));
        }
        env.set("words", env.get("RESPONSE"));
        env.set("funcName", Value::from_string(""));
        env.set("found", Value::from_double(0));
        env.set("wi", Value::from_double(0));
        env.set("wc", list_length(env.get("words")));
        while (Value(Number((env.get("wi").num.value < env.get("wc").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("wi"));
                args.push_back(env.get("words"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("w", env.get("RESPONSE"));
            if (Value(Number(value_equals(env.get("found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                env.set("funcName", env.get("w"));
                break;
            }
            if (Value(Number(value_equals(env.get("w"), Value::from_string("function")) ? 1 : 0)).num.value != 0) {
                env.set("found", Value::from_double(1));
            }
            env.set("wi", (env.get("wi") + Value::from_double(1)));
        }
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        env.set("body", Value::from_list({}));
        while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_pos"));
                args.push_back(env.get("g_lines"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("bLine", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("bLine"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("bTrimmed", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("bTrimmed"));
                args.push_back(Value::from_string("END FUNCTION"));
                env.set("RESPONSE", startsWith(env, args));
            }
            env.set("isEnd", env.get("RESPONSE"));
            if (Value(Number(value_equals(env.get("isEnd"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                break;
            }
            {
                std::vector<Value> args;
                args.push_back(env.get("bLine"));
                args.push_back(env.get("body"));
                env.set("RESPONSE", append(env, args));
            }
            env.set("newBody", env.get("RESPONSE"));
            env.set("body", env.get("newBody"));
            env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        }
        {
            std::vector<Value> args;
            args.push_back(env.get("funcName"));
            args.push_back(env.get("g_funcs"));
            env.set("RESPONSE", append(env, args));
        }
        env.set("newFuncs", env.get("RESPONSE"));
        env.set("g_funcs", env.get("newFuncs"));
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("void ") + env.get("funcName")) + Value::from_string("(Environment& env) {")));
            env.set("RESPONSE", emit(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("}"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(1);
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("t"));
        args.push_back(Value::from_string("CALL"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isCall", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isCall"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("t"));
            args.push_back(Value::from_string("WITH"));
            env.set("RESPONSE", indexOf(env, args));
        }
        env.set("withPos", env.get("RESPONSE"));
        env.set("callName", Value::from_string(""));
        if (Value(Number((env.get("withPos").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("t"));
                args.push_back(Value::from_double(4));
                args.push_back(Value(Number(env.get("withPos").num.value - Value::from_double(4).num.value)));
                env.set("RESPONSE", substring(env, args));
            }
            env.set("callName", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("callName"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("callName", env.get("RESPONSE"));
        }
        else {
            {
                std::vector<Value> args;
                args.push_back(env.get("t"));
                args.push_back(Value::from_double(4));
                args.push_back(string_length(env.get("t")));
                env.set("RESPONSE", substring(env, args));
            }
            env.set("callName", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("callName"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("callName", env.get("RESPONSE"));
        }
        {
            std::vector<Value> args;
            args.push_back(env.get("callName"));
            args.push_back(Value::from_string(";"));
            env.set("RESPONSE", endsWith(env, args));
        }
        env.set("hasSemi", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("hasSemi"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("callName"));
                args.push_back(Value::from_double(0));
                args.push_back(Value(Number(string_length(env.get("callName")).num.value - Value::from_double(1).num.value)));
                env.set("RESPONSE", substring(env, args));
            }
            env.set("callName", env.get("RESPONSE"));
        }
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("    ") + env.get("callName")) + Value::from_string("(env);")));
            env.set("RESPONSE", emit(env, args));
        }
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        return Value::from_double(1);
    }
    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
    return Value::from_double(0);
    return Value::from_double(0);
}

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("g_lines", Value::from_list({}));
    env.set("g_pos", Value::from_double(0));
    env.set("g_lineCount", Value::from_double(0));
    env.set("g_out", Value::from_list({}));
    env.set("g_indent", Value::from_double(0));
    env.set("g_funcs", Value::from_list({}));
    env.set("g_idx", Value::from_double(0));
    env.set("g_compiled", Value::from_string(""));
    env.set("g_name", Value::from_string(""));
    env.set("argCount", list_length(env.get("ARGV")));
    env.set("filePath", Value::from_string("selfhost/minicodegen.mish"));
    if (Value(Number((env.get("argCount").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("ARGV"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("filePath", env.get("RESPONSE"));
    }
    env.set("source", file_read(env.get("filePath").to_string()));
    {
        std::vector<Value> args;
        args.push_back(env.get("source"));
        args.push_back(Value::from_string("\n"));
        env.set("RESPONSE", split(env, args));
    }
    env.set("sourceLines", env.get("RESPONSE"));
    env.set("g_lines", env.get("sourceLines"));
    env.set("g_pos", Value::from_double(0));
    env.set("g_lineCount", list_length(env.get("g_lines")));
    env.set("g_out", Value::from_list({}));
    env.set("g_funcs", Value::from_list({}));
    while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", compileStmt(env, args));
        }
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("#include \"midshake_runtime.hpp\""));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("using namespace ms;"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string(""));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("int main(int argc, char* argv[]) {"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("    Environment env(argc, argv);"));
        env.set("RESPONSE", emit(env, args));
    }
    env.set("cppOutput", Value::from_string(""));
    env.set("outCount", list_length(env.get("g_out")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("outCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_out"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("outLine", env.get("RESPONSE"));
        if (Value(Number((env.get("g_idx").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            env.set("cppOutput", (env.get("cppOutput") + Value::from_string("\n")));
        }
        env.set("cppOutput", (env.get("cppOutput") + env.get("outLine")));
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("    return 0;"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("}"));
        env.set("RESPONSE", emit(env, args));
    }
    env.set("finalOut", Value::from_string(""));
    env.set("outCount2", list_length(env.get("g_out")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("outCount2").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_out"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("line", env.get("RESPONSE"));
        if (Value(Number((env.get("g_idx").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            env.set("finalOut", (env.get("finalOut") + Value::from_string("\n")));
        }
        env.set("finalOut", (env.get("finalOut") + env.get("line")));
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    file_write("output/generated.cpp", env.get("finalOut"));
    print(Value::from_string("Compilation complete! Generated "));
    print(list_length(env.get("g_out")));
    print(Value::from_string(" lines of C++."));
    return 0;
}