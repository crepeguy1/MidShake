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

Value createNode(Environment& env, const std::vector<Value>& args) {
    env.set("nodeType", args[0]);
    env.set("node", Value::from_map({}));
    env.set("node", map_set(env.get("node"), Value::from_string("type"), env.get("nodeType")));
    env.set("node", map_set(env.get("node"), Value::from_string("body"), Value::from_list({})));
    env.set("node", map_set(env.get("node"), Value::from_string("children"), Value::from_list({})));
    return env.get("node");
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
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_name", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            env.set("g_name", env.get("g_word"));
            env.set("g_found", Value::from_double(2));
        }
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("variable")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_name");
    return Value::from_double(0);
}

Value extractSetName(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_name", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            env.set("g_name", env.get("g_word"));
            env.set("g_found", Value::from_double(2));
        }
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("variable")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_name");
    return Value::from_double(0);
}

Value extractFuncName(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_name", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            env.set("g_name", env.get("g_word"));
            env.set("g_found", Value::from_double(2));
        }
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("function")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_name");
    return Value::from_double(0);
}

Value extractFuncParams(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    env.set("params", Value::from_list({}));
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_paramStr", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("variable")) ? 1 : 0)).num.value != 0) {
            if (Value(Number(value_equals(env.get("g_found"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
                env.set("g_found", Value::from_double(1));
            }
        }
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("variables")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            if (Value(Number(value_equals(env.get("g_word"), Value::from_string(";")) ? 1 : 0)).num.value != 0) {
                env.set("g_found", Value::from_double(2));
            }
            else {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_word"));
                    args.push_back(Value::from_string(";"));
                    env.set("RESPONSE", endsWith(env, args));
                }
                env.set("hasSemi", env.get("RESPONSE"));
                env.set("cleanWord", env.get("g_word"));
                if (Value(Number(value_equals(env.get("hasSemi"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("g_word"));
                        env.set("RESPONSE", length(env, args));
                    }
                    env.set("wLen", env.get("RESPONSE"));
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("g_word"));
                        args.push_back(Value::from_double(0));
                        args.push_back(Value(Number(env.get("wLen").num.value - Value::from_double(1).num.value)));
                        env.set("RESPONSE", substring(env, args));
                    }
                    env.set("cleanWord", env.get("RESPONSE"));
                }
                if (Value(Number(!value_equals(env.get("cleanWord"), Value::from_string("variable")) ? 1 : 0)).num.value != 0) {
                    if (Value(Number(!value_equals(env.get("cleanWord"), Value::from_string("variables")) ? 1 : 0)).num.value != 0) {
                        if (Value(Number((string_length(env.get("g_paramStr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
                            env.set("g_paramStr", (env.get("g_paramStr") + Value::from_string(",")));
                        }
                        env.set("g_paramStr", (env.get("g_paramStr") + env.get("cleanWord")));
                    }
                }
            }
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    if (Value(Number((string_length(env.get("g_paramStr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_paramStr"));
            args.push_back(Value::from_string(","));
            env.set("RESPONSE", split(env, args));
        }
        env.set("paramList", env.get("RESPONSE"));
        env.set("pCount", list_length(env.get("paramList")));
        env.set("g_pIdx", Value::from_double(0));
        env.set("g_params", Value::from_list({}));
        while (Value(Number((env.get("g_pIdx").num.value < env.get("pCount").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_pIdx"));
                args.push_back(env.get("paramList"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("param", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("param"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("trimmedParam", env.get("RESPONSE"));
            if (Value(Number((string_length(env.get("trimmedParam")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
                env.set("g_params", list_append(env.get("g_params"), env.get("trimmedParam")));
            }
            env.set("g_pIdx", (env.get("g_pIdx") + Value::from_double(1)));
        }
        return env.get("g_params");
    }
    return Value::from_list({});
    return Value::from_double(0);
}

Value extractCallName(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_name", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            env.set("g_name", env.get("g_word"));
            env.set("g_found", Value::from_double(2));
        }
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("CALL")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_name");
    return Value::from_double(0);
}

Value extractImportPath(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("parts", env.get("RESPONSE"));
    env.set("partCount", list_length(env.get("parts")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_pathStr", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("partCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("parts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("part", env.get("RESPONSE"));
        env.set("g_word", env.get("part"));
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            env.set("g_pathStr", env.get("g_word"));
            break;
        }
        if (Value(Number(value_equals(env.get("g_word"), Value::from_string("file")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_pathStr");
    return Value::from_double(0);
}

Value extractProclaimExpr(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(1));
    env.set("g_exprStr", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number((string_length(env.get("g_exprStr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            env.set("g_exprStr", (env.get("g_exprStr") + Value::from_string(" ")));
        }
        env.set("g_exprStr", (env.get("g_exprStr") + env.get("g_word")));
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_exprStr");
    return Value::from_double(0);
}

Value extractAfterKeyword(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    env.set("keyword", args[1]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(0));
    env.set("g_found", Value::from_double(0));
    env.set("g_resultStr", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_found"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            if (Value(Number((string_length(env.get("g_resultStr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
                env.set("g_resultStr", (env.get("g_resultStr") + Value::from_string(" ")));
            }
            env.set("g_resultStr", (env.get("g_resultStr") + env.get("g_word")));
        }
        if (Value(Number(value_equals(env.get("g_word"), env.get("keyword")) ? 1 : 0)).num.value != 0) {
            env.set("g_found", Value::from_double(1));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_resultStr");
    return Value::from_double(0);
}

Value extractCondition(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    env.set("endKeyword", args[1]);
    {
        std::vector<Value> args;
        args.push_back(env.get("line"));
        args.push_back(Value::from_string(" "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("words", env.get("RESPONSE"));
    env.set("wordCount", list_length(env.get("words")));
    env.set("g_idx", Value::from_double(1));
    env.set("g_conditionStr", Value::from_string(""));
    while (Value(Number((env.get("g_idx").num.value < env.get("wordCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("words"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("word", env.get("RESPONSE"));
        env.set("g_word", env.get("word"));
        if (Value(Number(value_equals(env.get("g_word"), env.get("endKeyword")) ? 1 : 0)).num.value != 0) {
            break;
        }
        if (Value(Number((string_length(env.get("g_conditionStr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            env.set("g_conditionStr", (env.get("g_conditionStr") + Value::from_string(" ")));
        }
        env.set("g_conditionStr", (env.get("g_conditionStr") + env.get("g_word")));
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    return env.get("g_conditionStr");
    return Value::from_double(0);
}

Value parseStatement(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    env.set("node", Value::from_map({}));
    env.set("consumed", Value::from_double(0));
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
    env.set("trimmed", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("trimmed"), Value::from_string("")) ? 1 : 0)).num.value != 0) {
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("Empty"));
            env.set("RESPONSE", createNode(env, args));
        }
        env.set("emptyNode", env.get("RESPONSE"));
        env.set("g_result", env.get("emptyNode"));
        return env.get("emptyNode");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string("^"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isComment", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isComment"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("Comment"));
            env.set("RESPONSE", createNode(env, args));
        }
        env.set("commentNode", env.get("RESPONSE"));
        env.set("commentNode", map_set(env.get("commentNode"), Value::from_string("text"), env.get("trimmed")));
        env.set("g_result", env.get("commentNode"));
        return env.get("commentNode");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string("LET"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isLet", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isLet"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("Let"));
            env.set("RESPONSE", createNode(env, args));
        }
        env.set("letNode", env.get("RESPONSE"));
        env.set("g_node", env.get("letNode"));
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            env.set("RESPONSE", extractLetName(env, args));
        }
        env.set("varName", env.get("RESPONSE"));
        env.set("g_node", map_set(env.get("g_node"), Value::from_string("name"), env.get("varName")));
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("BE"));
            env.set("RESPONSE", extractAfterKeyword(env, args));
        }
        env.set("valueExpr", env.get("RESPONSE"));
        env.set("g_node", map_set(env.get("g_node"), Value::from_string("value"), env.get("valueExpr")));
        env.set("node", env.get("g_node"));
        env.set("consumed", Value::from_double(1));
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("SET"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isSet", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isSet"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Set"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("setNode", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                env.set("RESPONSE", extractSetName(env, args));
            }
            env.set("varName", env.get("RESPONSE"));
            env.set("g_node", map_set(env.get("g_node"), Value::from_string("name"), env.get("varName")));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                args.push_back(Value::from_string("TO"));
                env.set("RESPONSE", extractAfterKeyword(env, args));
            }
            env.set("valueExpr", env.get("RESPONSE"));
            env.set("g_node", map_set(env.get("g_node"), Value::from_string("value"), env.get("valueExpr")));
            env.set("node", env.get("g_node"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("PROCLAIM"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isProclaim", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isProclaim"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Proclaim"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("proclaimNode", env.get("RESPONSE"));
            env.set("g_node", env.get("proclaimNode"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                env.set("RESPONSE", extractProclaimExpr(env, args));
            }
            env.set("expr", env.get("RESPONSE"));
            env.set("g_node", map_set(env.get("g_node"), Value::from_string("value"), env.get("expr")));
            env.set("node", env.get("g_node"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("IF"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isIf", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isIf"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("If"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("ifNode", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                args.push_back(Value::from_string("THEN"));
                env.set("RESPONSE", extractCondition(env, args));
            }
            env.set("condition", env.get("RESPONSE"));
            env.set("ifNode", map_set(env.get("ifNode"), Value::from_string("condition"), env.get("condition")));
            env.set("body", Value::from_list({}));
            env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
            while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_pos"));
                    args.push_back(env.get("g_lines"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("bodyLine", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("bodyLine"));
                    env.set("RESPONSE", trim(env, args));
                }
                env.set("trimmedBody", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("trimmedBody"));
                    args.push_back(Value::from_string("END IF"));
                    env.set("RESPONSE", startsWith(env, args));
                }
                env.set("isEndIf", env.get("RESPONSE"));
                if (Value(Number(value_equals(env.get("isEndIf"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                    break;
                }
                if (Value(Number(value_equals(env.get("trimmedBody"), Value::from_string("ELSE")) ? 1 : 0)).num.value != 0) {
                    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                    break;
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_double(0));
                    env.set("RESPONSE", parseStatement(env, args));
                }
                env.set("childNode", env.get("g_result"));
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("type"));
                    args.push_back(env.get("childNode"));
                    env.set("RESPONSE", mapGet(env, args));
                }
                env.set("childType", env.get("RESPONSE"));
                if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
                    if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                        env.set("body", list_append(env.get("body"), env.get("childNode")));
                    }
                }
            }
            env.set("ifNode", map_set(env.get("ifNode"), Value::from_string("body"), env.get("body")));
            {
                std::vector<Value> args;
                args.push_back(Value(Number(env.get("g_pos").num.value - Value::from_double(1).num.value)));
                args.push_back(env.get("g_lines"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("lastLine", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("lastLine"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("lastTrimmed", env.get("RESPONSE"));
            if (Value(Number(value_equals(env.get("lastTrimmed"), Value::from_string("ELSE")) ? 1 : 0)).num.value != 0) {
                env.set("elseBody", Value::from_list({}));
                while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("g_pos"));
                        args.push_back(env.get("g_lines"));
                        env.set("RESPONSE", getItem(env, args));
                    }
                    env.set("elseLine", env.get("RESPONSE"));
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("elseLine"));
                        env.set("RESPONSE", trim(env, args));
                    }
                    env.set("trimmedElse", env.get("RESPONSE"));
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("trimmedElse"));
                        args.push_back(Value::from_string("END IF"));
                        env.set("RESPONSE", startsWith(env, args));
                    }
                    env.set("isEndIfElse", env.get("RESPONSE"));
                    if (Value(Number(value_equals(env.get("isEndIfElse"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                        env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                        break;
                    }
                    {
                        std::vector<Value> args;
                        args.push_back(Value::from_double(0));
                        env.set("RESPONSE", parseStatement(env, args));
                    }
                    env.set("elseChild", env.get("g_result"));
                    {
                        std::vector<Value> args;
                        args.push_back(Value::from_string("type"));
                        args.push_back(env.get("elseChild"));
                        env.set("RESPONSE", mapGet(env, args));
                    }
                    env.set("elseChildType", env.get("RESPONSE"));
                    if (Value(Number(!value_equals(env.get("elseChildType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
                        if (Value(Number(!value_equals(env.get("elseChildType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                            env.set("elseBody", list_append(env.get("elseBody"), env.get("elseChild")));
                        }
                    }
                }
                env.set("ifNode", map_set(env.get("ifNode"), Value::from_string("elseBody"), env.get("elseBody")));
            }
            env.set("node", env.get("ifNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("WHILST"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isWhile", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isWhile"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("While"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("whileNode", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                args.push_back(Value::from_string("DO"));
                env.set("RESPONSE", extractCondition(env, args));
            }
            env.set("condition", env.get("RESPONSE"));
            env.set("whileNode", map_set(env.get("whileNode"), Value::from_string("condition"), env.get("condition")));
            env.set("body", Value::from_list({}));
            env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
            while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_pos"));
                    args.push_back(env.get("g_lines"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("bodyLine", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("bodyLine"));
                    env.set("RESPONSE", trim(env, args));
                }
                env.set("trimmedBody", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("trimmedBody"));
                    args.push_back(Value::from_string("END WHILST"));
                    env.set("RESPONSE", startsWith(env, args));
                }
                env.set("isEndWhile", env.get("RESPONSE"));
                if (Value(Number(value_equals(env.get("isEndWhile"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                    break;
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_double(0));
                    env.set("RESPONSE", parseStatement(env, args));
                }
                env.set("childNode", env.get("g_result"));
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("type"));
                    args.push_back(env.get("childNode"));
                    env.set("RESPONSE", mapGet(env, args));
                }
                env.set("childType", env.get("RESPONSE"));
                if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
                    if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                        env.set("body", list_append(env.get("body"), env.get("childNode")));
                    }
                }
            }
            env.set("whileNode", map_set(env.get("whileNode"), Value::from_string("body"), env.get("body")));
            env.set("node", env.get("whileNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("DEFINE"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isDefine", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isDefine"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("FunctionDef"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("funcNode", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                env.set("RESPONSE", extractFuncName(env, args));
            }
            env.set("funcName", env.get("RESPONSE"));
            env.set("funcNode", map_set(env.get("funcNode"), Value::from_string("name"), env.get("funcName")));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                env.set("RESPONSE", extractFuncParams(env, args));
            }
            env.set("params", env.get("RESPONSE"));
            env.set("funcNode", map_set(env.get("funcNode"), Value::from_string("params"), env.get("params")));
            env.set("body", Value::from_list({}));
            env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
            while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_pos"));
                    args.push_back(env.get("g_lines"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("bodyLine", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("bodyLine"));
                    env.set("RESPONSE", trim(env, args));
                }
                env.set("trimmedBody", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("trimmedBody"));
                    args.push_back(Value::from_string("END FUNCTION"));
                    env.set("RESPONSE", startsWith(env, args));
                }
                env.set("isEndFunc", env.get("RESPONSE"));
                if (Value(Number(value_equals(env.get("isEndFunc"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                    break;
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_double(0));
                    env.set("RESPONSE", parseStatement(env, args));
                }
                env.set("childNode", env.get("g_result"));
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("type"));
                    args.push_back(env.get("childNode"));
                    env.set("RESPONSE", mapGet(env, args));
                }
                env.set("childType", env.get("RESPONSE"));
                if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
                    if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                        env.set("body", list_append(env.get("body"), env.get("childNode")));
                    }
                }
            }
            env.set("funcNode", map_set(env.get("funcNode"), Value::from_string("body"), env.get("body")));
            env.set("node", env.get("funcNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("FOR"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isFor", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isFor"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("ForIn"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("forNode", env.get("RESPONSE"));
            env.set("forNode", map_set(env.get("forNode"), Value::from_string("header"), env.get("trimmed")));
            env.set("body", Value::from_list({}));
            env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
            while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_pos"));
                    args.push_back(env.get("g_lines"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("bodyLine", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("bodyLine"));
                    env.set("RESPONSE", trim(env, args));
                }
                env.set("trimmedBody", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("trimmedBody"));
                    args.push_back(Value::from_string("END FOR"));
                    env.set("RESPONSE", startsWith(env, args));
                }
                env.set("isEndFor", env.get("RESPONSE"));
                if (Value(Number(value_equals(env.get("isEndFor"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                    break;
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_double(0));
                    env.set("RESPONSE", parseStatement(env, args));
                }
                env.set("childNode", env.get("g_result"));
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("type"));
                    args.push_back(env.get("childNode"));
                    env.set("RESPONSE", mapGet(env, args));
                }
                env.set("childType", env.get("RESPONSE"));
                if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
                    if (Value(Number(!value_equals(env.get("childType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                        env.set("body", list_append(env.get("body"), env.get("childNode")));
                    }
                }
            }
            env.set("forNode", map_set(env.get("forNode"), Value::from_string("body"), env.get("body")));
            env.set("node", env.get("forNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("CALL"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isCall", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isCall"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Call"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("callNode", env.get("RESPONSE"));
            env.set("g_node", env.get("callNode"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                env.set("RESPONSE", extractCallName(env, args));
            }
            env.set("callName", env.get("RESPONSE"));
            env.set("g_node", map_set(env.get("g_node"), Value::from_string("name"), env.get("callName")));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                args.push_back(Value::from_string("WITH"));
                env.set("RESPONSE", extractAfterKeyword(env, args));
            }
            env.set("callArgs", env.get("RESPONSE"));
            env.set("g_node", map_set(env.get("g_node"), Value::from_string("value"), env.get("callArgs")));
            env.set("node", env.get("g_node"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("IMPORT"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isImport", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isImport"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Import"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("importNode", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                env.set("RESPONSE", extractImportPath(env, args));
            }
            env.set("importPath", env.get("RESPONSE"));
            env.set("importNode", map_set(env.get("importNode"), Value::from_string("path"), env.get("importPath")));
            env.set("node", env.get("importNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("RETURN"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isReturn", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isReturn"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Return"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("returnNode", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                args.push_back(Value::from_string("RETURN"));
                env.set("RESPONSE", extractAfterKeyword(env, args));
            }
            env.set("returnExpr", env.get("RESPONSE"));
            env.set("returnNode", map_set(env.get("returnNode"), Value::from_string("value"), env.get("returnExpr")));
            env.set("node", env.get("returnNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("IN the file"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isFileWrite", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isFileWrite"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("FileWrite"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("fileWriteNode", env.get("RESPONSE"));
            env.set("fileWriteNode", map_set(env.get("fileWriteNode"), Value::from_string("value"), env.get("trimmed")));
            env.set("node", env.get("fileWriteNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        if (Value(Number(value_equals(env.get("trimmed"), Value::from_string("BREAK")) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Break"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("breakNode", env.get("RESPONSE"));
            env.set("node", env.get("breakNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        if (Value(Number(value_equals(env.get("trimmed"), Value::from_string("CONTINUE")) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Continue"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("continueNode", env.get("RESPONSE"));
            env.set("node", env.get("continueNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_string("TERMINATE"));
            env.set("RESPONSE", startsWith(env, args));
        }
        env.set("isTerminate", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("isTerminate"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("Terminate"));
                env.set("RESPONSE", createNode(env, args));
            }
            env.set("terminateNode", env.get("RESPONSE"));
            env.set("node", env.get("terminateNode"));
            env.set("consumed", Value::from_double(1));
        }
    }
    if (Value(Number(value_equals(env.get("consumed"), Value::from_double(0)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("Unknown"));
            env.set("RESPONSE", createNode(env, args));
        }
        env.set("unknownNode", env.get("RESPONSE"));
        env.set("unknownNode", map_set(env.get("unknownNode"), Value::from_string("text"), env.get("trimmed")));
        env.set("node", env.get("unknownNode"));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("type"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodeType", env.get("RESPONSE"));
    if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("While")) ? 1 : 0)).num.value != 0) {
        if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("If")) ? 1 : 0)).num.value != 0) {
            if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("FunctionDef")) ? 1 : 0)).num.value != 0) {
                if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("ForIn")) ? 1 : 0)).num.value != 0) {
                    env.set("g_pos", (env.get("g_pos") + Value::from_double(1)));
                }
            }
        }
    }
    env.set("g_result", env.get("node"));
    return env.get("node");
    return Value::from_double(0);
}

Value printNode(Environment& env, const std::vector<Value>& args) {
    env.set("node", args[0]);
    env.set("indent", args[1]);
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("type"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodeType", env.get("RESPONSE"));
    print(env.get("indent"));
    print(Value::from_string("Node: "));
    print(env.get("nodeType"));
    print(Value::from_string(""));
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("name"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodeName", env.get("RESPONSE"));
    if (Value(Number((string_length(env.get("nodeName")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("indent"));
        print(Value::from_string("  Name: "));
        print(env.get("nodeName"));
        print(Value::from_string(""));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("value"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodeValue", env.get("RESPONSE"));
    if (Value(Number((string_length(env.get("nodeValue")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("indent"));
        print(Value::from_string("  Value: "));
        print(env.get("nodeValue"));
        print(Value::from_string(""));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("condition"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodeCondition", env.get("RESPONSE"));
    if (Value(Number((string_length(env.get("nodeCondition")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("indent"));
        print(Value::from_string("  Condition: "));
        print(env.get("nodeCondition"));
        print(Value::from_string(""));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("params"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodeParams", env.get("RESPONSE"));
    if (Value(Number(!value_equals(env.get("nodeParams"), Value::from_string("")) ? 1 : 0)).num.value != 0) {
        print(env.get("indent"));
        print(Value::from_string("  Params: "));
        print(env.get("nodeParams"));
        print(Value::from_string(""));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("path"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("nodePath", env.get("RESPONSE"));
    if (Value(Number((string_length(env.get("nodePath")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        print(env.get("indent"));
        print(Value::from_string("  Path: "));
        print(env.get("nodePath"));
        print(Value::from_string(""));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("body"));
        args.push_back(env.get("node"));
        env.set("RESPONSE", mapGet(env, args));
    }
    env.set("body", env.get("RESPONSE"));
    if (Value(Number(!value_equals(env.get("body"), Value::from_string("")) ? 1 : 0)).num.value != 0) {
        env.set("bodySize", list_length(env.get("body")));
        if (Value(Number((env.get("bodySize").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            print(env.get("indent"));
            print(Value::from_string("  Body ("));
            print(env.get("bodySize"));
            print(Value::from_string(" children):"));
            print(Value::from_string(""));
            env.set("g_bIdx", Value::from_double(0));
            while (Value(Number((env.get("g_bIdx").num.value < env.get("bodySize").num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_bIdx"));
                    args.push_back(env.get("body"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("child", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("child"));
                    args.push_back((env.get("indent") + Value::from_string("    ")));
                    env.set("RESPONSE", printNode(env, args));
                }
                env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
            }
        }
    }
    return Value::from_double(0);
}

Value parseFile(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    env.set("g_ast", Value::from_list({}));
    env.set("g_pos", Value::from_double(0));
    env.set("g_lineCount", list_length(env.get("g_lines")));
    while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", parseStatement(env, args));
        }
        env.set("node", env.get("g_result"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("type"));
            args.push_back(env.get("node"));
            env.set("RESPONSE", mapGet(env, args));
        }
        env.set("nodeType", env.get("RESPONSE"));
        if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
            if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                env.set("g_ast", list_append(env.get("g_ast"), env.get("node")));
            }
        }
    }
    return env.get("g_ast");
    return Value::from_double(0);
}

Value printAst(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    print(Value::from_string("--- AST ---"));
    env.set("astSize", list_length(env.get("g_ast")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("astSize").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_ast"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("node", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("node"));
            args.push_back(Value::from_string(""));
            env.set("RESPONSE", printNode(env, args));
        }
        print(Value::from_string(""));
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    print(Value::from_string(""));
    print(Value::from_string("AST building complete!"));
    print(Value::from_string("Total nodes: "));
    print(env.get("astSize"));
    return Value::from_double(0);
    return Value::from_double(0);
}

Value emit(Environment& env, const std::vector<Value>& args) {
    env.set("line", args[0]);
    env.set("padding", Value::from_string(""));
    env.set("padIdx", Value::from_double(0));
    while (Value(Number((env.get("padIdx").num.value < env.get("g_indent").num.value) ? 1 : 0)).num.value != 0) {
        env.set("padding", (env.get("padding") + Value::from_string("    ")));
        env.set("padIdx", (env.get("padIdx") + Value::from_double(1)));
    }
    env.set("fullLine", (env.get("padding") + env.get("line")));
    {
        std::vector<Value> args;
        args.push_back(env.get("fullLine"));
        args.push_back(env.get("g_output"));
        env.set("RESPONSE", append(env, args));
    }
    env.set("newOutput", env.get("RESPONSE"));
    env.set("g_output", env.get("newOutput"));
    return env.get("g_output");
    return Value::from_double(0);
}

Value indent(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    env.set("g_indent", (env.get("g_indent") + Value::from_double(1)));
    return Value::from_double(0);
    return Value::from_double(0);
}

Value dedent(Environment& env, const std::vector<Value>& args) {
    env.set("dummy", args[0]);
    if (Value(Number((env.get("g_indent").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        env.set("g_indent", Value(Number(env.get("g_indent").num.value - Value::from_double(1).num.value)));
    }
    return Value::from_double(0);
    return Value::from_double(0);
}

Value stripQuotes(Environment& env, const std::vector<Value>& args) {
    env.set("str", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("str"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("trimmed", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        env.set("RESPONSE", length(env, args));
    }
    env.set("len", env.get("RESPONSE"));
    if (Value(Number((env.get("len").num.value >= Value::from_double(2).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", charAt(env, args));
        }
        env.set("first", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmed"));
            args.push_back(Value(Number(env.get("len").num.value - Value::from_double(1).num.value)));
            env.set("RESPONSE", charAt(env, args));
        }
        env.set("last", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("first"), env.get("last")) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmed"));
                args.push_back(Value::from_double(1));
                args.push_back(Value(Number(env.get("len").num.value - Value::from_double(1).num.value)));
                env.set("RESPONSE", substring(env, args));
            }
            env.set("unquoted", env.get("RESPONSE"));
            return env.get("unquoted");
        }
    }
    return env.get("trimmed");
    return Value::from_double(0);
}

Value buildEnvSet(Environment& env, const std::vector<Value>& args) {
    env.set("name", args[0]);
    env.set("value", args[1]);
    env.set("result", ((((((Value::from_string("env.set(") + env.get("QUOTE")) + env.get("name")) + env.get("QUOTE")) + Value::from_string(", ")) + env.get("value")) + Value::from_string(");")));
    return env.get("result");
    return Value::from_double(0);
}

Value buildEnvGet(Environment& env, const std::vector<Value>& args) {
    env.set("name", args[0]);
    env.set("result", ((((Value::from_string("env.get(") + env.get("QUOTE")) + env.get("name")) + env.get("QUOTE")) + Value::from_string(")")));
    return env.get("result");
    return Value::from_double(0);
}

Value buildStringLit(Environment& env, const std::vector<Value>& args) {
    env.set("content", args[0]);
    env.set("result", ((((Value::from_string("Value::from_string(") + env.get("QUOTE")) + env.get("content")) + env.get("QUOTE")) + Value::from_string(")")));
    return env.get("result");
    return Value::from_double(0);
}

Value compileExpr(Environment& env, const std::vector<Value>& args) {
    env.set("expr", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("expr"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("trimmed", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string(";"));
        args.push_back(Value::from_string(""));
        env.set("RESPONSE", replace(env, args));
    }
    env.set("g_compiled", env.get("RESPONSE"));
    env.set("cleaned", env.get("g_compiled"));
    {
        std::vector<Value> args;
        args.push_back(env.get("cleaned"));
        args.push_back(Value::from_string("thestring"));
        args.push_back(Value::from_string("the string"));
        env.set("RESPONSE", replace(env, args));
    }
    env.set("g_compiled", env.get("RESPONSE"));
    env.set("normalized", env.get("g_compiled"));
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the string"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isString", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isString"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("the string"));
            env.set("RESPONSE", length(env, args));
        }
        env.set("prefixLen", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("normalized"));
            args.push_back(env.get("prefixLen"));
            args.push_back(string_length(env.get("normalized")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("strContent", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("strContent"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("trimmedStr", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmedStr"));
            env.set("RESPONSE", stripQuotes(env, args));
        }
        env.set("unquoted", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("unquoted"));
            env.set("RESPONSE", buildStringLit(env, args));
        }
        env.set("result", env.get("RESPONSE"));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the number"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isNumber", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isNumber"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("the number"));
            env.set("RESPONSE", length(env, args));
        }
        env.set("numPrefixLen", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("normalized"));
            args.push_back(env.get("numPrefixLen"));
            args.push_back(string_length(env.get("normalized")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("numStr", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("numStr"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("trimmedNum", env.get("RESPONSE"));
        env.set("result", ((Value::from_string("Value::from_double(") + env.get("trimmedNum")) + Value::from_string(")")));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the value of"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isValueOf", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isValueOf"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("the value of"));
            env.set("RESPONSE", length(env, args));
        }
        env.set("valPrefixLen", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("normalized"));
            args.push_back(env.get("valPrefixLen"));
            args.push_back(string_length(env.get("normalized")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("varName", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("varName"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("trimmedVar", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmedVar"));
            env.set("RESPONSE", buildEnvGet(env, args));
        }
        env.set("result", env.get("RESPONSE"));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the RESPONSE"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isResponse", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isResponse"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("RESPONSE"));
            env.set("RESPONSE", buildEnvGet(env, args));
        }
        env.set("result", env.get("RESPONSE"));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the length of"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isLength", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isLength"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("the length of"));
            env.set("RESPONSE", length(env, args));
        }
        env.set("lenPrefixLen", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("normalized"));
            args.push_back(env.get("lenPrefixLen"));
            args.push_back(string_length(env.get("normalized")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("arg", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("arg"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("trimmedArg", env.get("RESPONSE"));
        env.set("result", ((Value::from_string("string_length(") + env.get("trimmedArg")) + Value::from_string(")")));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the size of"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isSize", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isSize"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("the size of"));
            env.set("RESPONSE", length(env, args));
        }
        env.set("sizePrefixLen", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("normalized"));
            args.push_back(env.get("sizePrefixLen"));
            args.push_back(string_length(env.get("normalized")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("arg", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("arg"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("trimmedArg", env.get("RESPONSE"));
        env.set("result", ((Value::from_string("list_length(") + env.get("trimmedArg")) + Value::from_string(")")));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string("the contents of"));
        env.set("RESPONSE", startsWith(env, args));
    }
    env.set("isFileRead", env.get("RESPONSE"));
    if (Value(Number(value_equals(env.get("isFileRead"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("the contents of"));
            env.set("RESPONSE", length(env, args));
        }
        env.set("filePrefixLen", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("normalized"));
            args.push_back(env.get("filePrefixLen"));
            args.push_back(string_length(env.get("normalized")));
            env.set("RESPONSE", substring(env, args));
        }
        env.set("pathExpr", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("pathExpr"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("trimmedPath", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("trimmedPath"));
            env.set("RESPONSE", stripQuotes(env, args));
        }
        env.set("unquotedPath", env.get("RESPONSE"));
        env.set("result", ((((Value::from_string("file_read(") + env.get("QUOTE")) + env.get("unquotedPath")) + env.get("QUOTE")) + Value::from_string(")")));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    if (Value(Number(value_equals(env.get("normalized"), Value::from_string("true")) ? 1 : 0)).num.value != 0) {
        env.set("g_compiled", Value::from_string("Value::from_double(1)"));
        return Value::from_string("Value::from_double(1)");
    }
    if (Value(Number(value_equals(env.get("normalized"), Value::from_string("false")) ? 1 : 0)).num.value != 0) {
        env.set("g_compiled", Value::from_string("Value::from_double(0)"));
        return Value::from_string("Value::from_double(0)");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string(" plus "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("plusParts", env.get("RESPONSE"));
    env.set("plusCount", list_length(env.get("plusParts")));
    if (Value(Number((env.get("plusCount").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("plusParts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("plusLeft", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("plusLeft"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("plusLeftTrimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("plusLeftTrimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledLeft", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(Value(Number(env.get("plusCount").num.value - Value::from_double(1).num.value)));
            args.push_back(env.get("plusParts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("plusRight", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("plusRight"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("plusRightTrimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("plusRightTrimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledRight", env.get("g_compiled"));
        env.set("result", ((((Value::from_string("(") + env.get("compiledLeft")) + Value::from_string(" + ")) + env.get("compiledRight")) + Value::from_string(")")));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        args.push_back(Value::from_string(" minus "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("minusParts", env.get("RESPONSE"));
    env.set("minusCount", list_length(env.get("minusParts")));
    if (Value(Number((env.get("minusCount").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("minusParts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("minusLeft", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("minusLeft"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("minusLeftTrimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("minusLeftTrimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledLeft", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(Value(Number(env.get("minusCount").num.value - Value::from_double(1).num.value)));
            args.push_back(env.get("minusParts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("minusRight", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("minusRight"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("minusRightTrimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("minusRightTrimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledRight", env.get("g_compiled"));
        env.set("result", ((((Value::from_string("Value(Number(") + env.get("compiledLeft")) + Value::from_string(".num.value - ")) + env.get("compiledRight")) + Value::from_string(".num.value))")));
        env.set("g_compiled", env.get("result"));
        return env.get("result");
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("normalized"));
        env.set("RESPONSE", buildEnvGet(env, args));
    }
    env.set("fallback", env.get("RESPONSE"));
    env.set("g_compiled", env.get("fallback"));
    return env.get("fallback");
    return Value::from_double(0);
}

Value compileCondition(Environment& env, const std::vector<Value>& args) {
    env.set("condition", args[0]);
    {
        std::vector<Value> args;
        args.push_back(env.get("condition"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("trimmed", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string(" THEN"));
        args.push_back(Value::from_string(""));
        env.set("RESPONSE", replace(env, args));
    }
    env.set("g_compiled", env.get("RESPONSE"));
    env.set("cleaned", env.get("g_compiled"));
    {
        std::vector<Value> args;
        args.push_back(env.get("cleaned"));
        args.push_back(Value::from_string(" THEN;"));
        args.push_back(Value::from_string(""));
        env.set("RESPONSE", replace(env, args));
    }
    env.set("g_compiled", env.get("RESPONSE"));
    env.set("cleaned2", env.get("g_compiled"));
    {
        std::vector<Value> args;
        args.push_back(env.get("cleaned2"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("trimmedCond", env.get("RESPONSE"));
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string(" IS equal to "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("parts", env.get("RESPONSE"));
    env.set("count", list_length(env.get("parts")));
    if (Value(Number((env.get("count").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("parts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("left", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("leftTrimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("leftTrimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledLeft", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(1));
            args.push_back(env.get("parts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("right", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("rightTrimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("rightTrimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledRight", env.get("g_compiled"));
        return ((((Value::from_string("(") + env.get("compiledLeft")) + Value::from_string(".num.value == ")) + env.get("compiledRight")) + Value::from_string(".num.value)"));
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string(" IS not equal to "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("parts2", env.get("RESPONSE"));
    env.set("count2", list_length(env.get("parts2")));
    if (Value(Number((env.get("count2").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("parts2"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("left2", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left2"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("left2Trimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left2Trimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledLeft2", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(1));
            args.push_back(env.get("parts2"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("right2", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right2"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("right2Trimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right2Trimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledRight2", env.get("g_compiled"));
        return ((((Value::from_string("(") + env.get("compiledLeft2")) + Value::from_string(".num.value != ")) + env.get("compiledRight2")) + Value::from_string(".num.value)"));
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string(" IS less than "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("parts3", env.get("RESPONSE"));
    env.set("count3", list_length(env.get("parts3")));
    if (Value(Number((env.get("count3").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("parts3"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("left3", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left3"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("left3Trimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left3Trimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledLeft3", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(1));
            args.push_back(env.get("parts3"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("right3", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right3"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("right3Trimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right3Trimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledRight3", env.get("g_compiled"));
        return ((((Value::from_string("(") + env.get("compiledLeft3")) + Value::from_string(".num.value < ")) + env.get("compiledRight3")) + Value::from_string(".num.value)"));
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        args.push_back(Value::from_string(" IS greater than "));
        env.set("RESPONSE", split(env, args));
    }
    env.set("parts4", env.get("RESPONSE"));
    env.set("count4", list_length(env.get("parts4")));
    if (Value(Number((env.get("count4").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("parts4"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("left4", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left4"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("left4Trimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("left4Trimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledLeft4", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(1));
            args.push_back(env.get("parts4"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("right4", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right4"));
            env.set("RESPONSE", trim(env, args));
        }
        env.set("right4Trimmed", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("right4Trimmed"));
            env.set("RESPONSE", compileExpr(env, args));
        }
        env.set("compiledRight4", env.get("g_compiled"));
        return ((((Value::from_string("(") + env.get("compiledLeft4")) + Value::from_string(".num.value > ")) + env.get("compiledRight4")) + Value::from_string(".num.value)"));
    }
    {
        std::vector<Value> args;
        args.push_back(env.get("trimmed"));
        env.set("RESPONSE", compileExpr(env, args));
    }
    env.set("compiledFallback", env.get("g_compiled"));
    return ((Value::from_string("(") + env.get("compiledFallback")) + Value::from_string(".num.value != 0)"));
    return Value::from_double(0);
}

Value compileNode(Environment& env, const std::vector<Value>& args) {
    env.set("node", args[0]);
    env.set("g_node", env.get("node"));
    env.set("nodeType", map_get(env.get("g_node"), Value::from_string("type")));
    {
        std::vector<Value> args;
        args.push_back(env.get("nodeType"));
        env.set("RESPONSE", trim(env, args));
    }
    env.set("trimmedType", env.get("RESPONSE"));
    env.set("nodeType", env.get("trimmedType"));
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Let")) ? 1 : 0)).num.value != 0) {
        env.set("varName", map_get(env.get("g_node"), Value::from_string("name")));
        env.set("valueExpr", map_get(env.get("g_node"), Value::from_string("value")));
        if (Value(Number((string_length(env.get("valueExpr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            print(Value::from_string(""));
            {
                std::vector<Value> args;
                args.push_back(env.get("valueExpr"));
                env.set("RESPONSE", compileExpr(env, args));
            }
        }
        else {
            env.set("g_compiled", Value::from_string(""));
        }
        env.set("compiled", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(env.get("varName"));
            args.push_back(env.get("compiled"));
            env.set("RESPONSE", buildEnvSet(env, args));
        }
        env.set("setLine", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("setLine"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Set")) ? 1 : 0)).num.value != 0) {
        env.set("varName", map_get(env.get("g_node"), Value::from_string("name")));
        env.set("valueExpr", map_get(env.get("g_node"), Value::from_string("value")));
        if (Value(Number((string_length(env.get("valueExpr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            print(Value::from_string(""));
            {
                std::vector<Value> args;
                args.push_back(env.get("valueExpr"));
                env.set("RESPONSE", compileExpr(env, args));
            }
        }
        else {
            env.set("g_compiled", Value::from_string(""));
        }
        env.set("compiled", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(env.get("varName"));
            args.push_back(env.get("compiled"));
            env.set("RESPONSE", buildEnvSet(env, args));
        }
        env.set("setLine", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("setLine"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Proclaim")) ? 1 : 0)).num.value != 0) {
        env.set("valueExpr", map_get(env.get("g_node"), Value::from_string("value")));
        if (Value(Number((string_length(env.get("valueExpr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            print(Value::from_string(""));
            {
                std::vector<Value> args;
                args.push_back(env.get("valueExpr"));
                env.set("RESPONSE", compileExpr(env, args));
            }
        }
        else {
            env.set("g_compiled", Value::from_string(""));
        }
        env.set("compiled", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("print(") + env.get("compiled")) + Value::from_string(");")));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("If")) ? 1 : 0)).num.value != 0) {
        env.set("condition", map_get(env.get("g_node"), Value::from_string("condition")));
        env.set("body", map_get(env.get("g_node"), Value::from_string("body")));
        env.set("condCompiled", Value::from_string(""));
        if (Value(Number((string_length(env.get("condition")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("condition"));
                env.set("RESPONSE", compileCondition(env, args));
            }
            env.set("condResult", env.get("RESPONSE"));
            env.set("condCompiled", env.get("condResult"));
        }
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("if (") + env.get("condCompiled")) + Value::from_string(") {")));
            env.set("RESPONSE", emit(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", indent(env, args));
        }
        env.set("bodySize", list_length(env.get("body")));
        env.set("g_bIdx", Value::from_double(0));
        while (Value(Number((env.get("g_bIdx").num.value < env.get("bodySize").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_bIdx"));
                args.push_back(env.get("body"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("child", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("child"));
                env.set("RESPONSE", compileNode(env, args));
            }
            env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", dedent(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("elseBody"));
            args.push_back(env.get("g_node"));
            env.set("RESPONSE", mapGet(env, args));
        }
        env.set("elseBody", env.get("RESPONSE"));
        if (Value(Number(!value_equals(env.get("elseBody"), Value::from_string("")) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("elseBody"));
                args.push_back(Value::from_string("[]"));
                env.set("RESPONSE", startsWith(env, args));
            }
            env.set("isEmpty", env.get("RESPONSE"));
            if (Value(Number(!value_equals(env.get("isEmpty"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("} else {"));
                    env.set("RESPONSE", emit(env, args));
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_double(0));
                    env.set("RESPONSE", indent(env, args));
                }
                env.set("elseSize", list_length(env.get("elseBody")));
                env.set("g_bIdx", Value::from_double(0));
                while (Value(Number((env.get("g_bIdx").num.value < env.get("elseSize").num.value) ? 1 : 0)).num.value != 0) {
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("g_bIdx"));
                        args.push_back(env.get("elseBody"));
                        env.set("RESPONSE", getItem(env, args));
                    }
                    env.set("elseChild", env.get("RESPONSE"));
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("elseChild"));
                        env.set("RESPONSE", compileNode(env, args));
                    }
                    env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_double(0));
                    env.set("RESPONSE", dedent(env, args));
                }
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("}"));
                    env.set("RESPONSE", emit(env, args));
                }
            }
            else {
                {
                    std::vector<Value> args;
                    args.push_back(Value::from_string("}"));
                    env.set("RESPONSE", emit(env, args));
                }
            }
        }
        else {
            {
                std::vector<Value> args;
                args.push_back(Value::from_string("}"));
                env.set("RESPONSE", emit(env, args));
            }
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("While")) ? 1 : 0)).num.value != 0) {
        env.set("condition", map_get(env.get("g_node"), Value::from_string("condition")));
        env.set("body", map_get(env.get("g_node"), Value::from_string("body")));
        env.set("condCompiled", Value::from_string(""));
        if (Value(Number((string_length(env.get("condition")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("condition"));
                env.set("RESPONSE", compileCondition(env, args));
            }
            env.set("condResult", env.get("RESPONSE"));
            env.set("condCompiled", env.get("condResult"));
        }
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("while (") + env.get("condCompiled")) + Value::from_string(") {")));
            env.set("RESPONSE", emit(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", indent(env, args));
        }
        env.set("bodySize", list_length(env.get("body")));
        env.set("g_bIdx", Value::from_double(0));
        while (Value(Number((env.get("g_bIdx").num.value < env.get("bodySize").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_bIdx"));
                args.push_back(env.get("body"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("child", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("child"));
                env.set("RESPONSE", compileNode(env, args));
            }
            env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", dedent(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("}"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("FunctionDef")) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_node"));
            args.push_back(env.get("g_functions"));
            env.set("RESPONSE", append(env, args));
        }
        env.set("newFuncs", env.get("RESPONSE"));
        env.set("g_functions", env.get("newFuncs"));
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Call")) ? 1 : 0)).num.value != 0) {
        env.set("callName", map_get(env.get("g_node"), Value::from_string("name")));
        env.set("callArgs", map_get(env.get("g_node"), Value::from_string("value")));
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("{"));
            env.set("RESPONSE", emit(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", indent(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("std::vector<Value> args;"));
            env.set("RESPONSE", emit(env, args));
        }
        if (Value(Number((string_length(env.get("callArgs")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("callArgs"));
                args.push_back(Value::from_string(","));
                env.set("RESPONSE", split(env, args));
            }
            env.set("argParts", env.get("RESPONSE"));
            env.set("argCount", list_length(env.get("argParts")));
            env.set("g_bIdx", Value::from_double(0));
            while (Value(Number((env.get("g_bIdx").num.value < env.get("argCount").num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("g_bIdx"));
                    args.push_back(env.get("argParts"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("argPart", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("argPart"));
                    env.set("RESPONSE", trim(env, args));
                }
                env.set("trimmedArg", env.get("RESPONSE"));
                if (Value(Number((string_length(env.get("trimmedArg")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
                    print(Value::from_string(""));
                    {
                        std::vector<Value> args;
                        args.push_back(env.get("trimmedArg"));
                        env.set("RESPONSE", compileExpr(env, args));
                    }
                    env.set("compiledArg", env.get("g_compiled"));
                    {
                        std::vector<Value> args;
                        args.push_back(((Value::from_string("args.push_back(") + env.get("compiledArg")) + Value::from_string(");")));
                        env.set("RESPONSE", emit(env, args));
                    }
                }
                env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
            }
        }
        {
            std::vector<Value> args;
            args.push_back((env.get("callName") + Value::from_string("(env, args);")));
            env.set("RESPONSE", emit(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", dedent(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("}"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Return")) ? 1 : 0)).num.value != 0) {
        env.set("returnExpr", map_get(env.get("g_node"), Value::from_string("value")));
        if (Value(Number((string_length(env.get("returnExpr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            print(Value::from_string(""));
            {
                std::vector<Value> args;
                args.push_back(env.get("returnExpr"));
                env.set("RESPONSE", compileExpr(env, args));
            }
        }
        else {
            env.set("g_compiled", Value::from_string(""));
        }
        env.set("compiled", env.get("g_compiled"));
        {
            std::vector<Value> args;
            args.push_back(((Value::from_string("return ") + env.get("compiled")) + Value::from_string(";")));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Break")) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("break;"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Continue")) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("continue;"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Terminate")) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("return Value::from_double(0);"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("ForIn")) ? 1 : 0)).num.value != 0) {
        env.set("header", map_get(env.get("g_node"), Value::from_string("header")));
        env.set("body", map_get(env.get("g_node"), Value::from_string("body")));
        {
            std::vector<Value> args;
            args.push_back(env.get("header"));
            args.push_back(Value::from_string(" "));
            env.set("RESPONSE", split(env, args));
        }
        env.set("headerParts", env.get("RESPONSE"));
        env.set("headerCount", list_length(env.get("headerParts")));
        env.set("g_bIdx", Value::from_double(0));
        env.set("foundVar", Value::from_double(0));
        env.set("forVarName", Value::from_string(""));
        while (Value(Number((env.get("g_bIdx").num.value < env.get("headerCount").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_bIdx"));
                args.push_back(env.get("headerParts"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("part", env.get("RESPONSE"));
            if (Value(Number(value_equals(env.get("foundVar"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                env.set("forVarName", env.get("part"));
                env.set("foundVar", Value::from_double(2));
            }
            if (Value(Number(value_equals(env.get("part"), Value::from_string("variable")) ? 1 : 0)).num.value != 0) {
                env.set("foundVar", Value::from_double(1));
            }
            env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
        }
        env.set("foundIn", Value::from_double(0));
        env.set("forListExpr", Value::from_string(""));
        env.set("g_bIdx", Value::from_double(0));
        while (Value(Number((env.get("g_bIdx").num.value < env.get("headerCount").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_bIdx"));
                args.push_back(env.get("headerParts"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("part", env.get("RESPONSE"));
            if (Value(Number(value_equals(env.get("foundIn"), Value::from_double(1)) ? 1 : 0)).num.value != 0) {
                if (Value(Number((string_length(env.get("forListExpr")).num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
                    env.set("forListExpr", (env.get("forListExpr") + Value::from_string(" ")));
                }
                env.set("forListExpr", (env.get("forListExpr") + env.get("part")));
            }
            if (Value(Number(value_equals(env.get("part"), Value::from_string("IN")) ? 1 : 0)).num.value != 0) {
                env.set("foundIn", Value::from_double(1));
            }
            env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
        }
        {
            std::vector<Value> args;
            args.push_back(((((Value::from_string("for (const auto& ") + env.get("forVarName")) + Value::from_string(" : ")) + env.get("forListExpr")) + Value::from_string(".lst) {")));
            env.set("RESPONSE", emit(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", indent(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(env.get("forVarName"));
            args.push_back(env.get("forVarName"));
            env.set("RESPONSE", buildEnvSet(env, args));
        }
        env.set("setVar", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("setVar"));
            env.set("RESPONSE", emit(env, args));
        }
        env.set("bodySize", list_length(env.get("body")));
        env.set("g_bIdx", Value::from_double(0));
        while (Value(Number((env.get("g_bIdx").num.value < env.get("bodySize").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_bIdx"));
                args.push_back(env.get("body"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("child", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("child"));
                env.set("RESPONSE", compileNode(env, args));
            }
            env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", dedent(env, args));
        }
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("}"));
            env.set("RESPONSE", emit(env, args));
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("FileWrite")) ? 1 : 0)).num.value != 0) {
        env.set("fileWriteExpr", map_get(env.get("g_node"), Value::from_string("value")));
        {
            std::vector<Value> args;
            args.push_back(env.get("fileWriteExpr"));
            args.push_back(Value::from_string("WRITE"));
            env.set("RESPONSE", split(env, args));
        }
        env.set("writeParts", env.get("RESPONSE"));
        env.set("writeCount", list_length(env.get("writeParts")));
        if (Value(Number((env.get("writeCount").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(Value::from_double(1));
                args.push_back(env.get("writeParts"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("writeContentExpr", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("writeContentExpr"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("trimmedContent", env.get("RESPONSE"));
            print(Value::from_string(""));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmedContent"));
                env.set("RESPONSE", compileExpr(env, args));
            }
            env.set("compiledContent", env.get("g_compiled"));
            {
                std::vector<Value> args;
                args.push_back(Value::from_double(0));
                args.push_back(env.get("writeParts"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("filePart", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("filePart"));
                args.push_back(Value::from_string("file"));
                env.set("RESPONSE", split(env, args));
            }
            env.set("fileSplitParts", env.get("RESPONSE"));
            env.set("fileSplitCount", list_length(env.get("fileSplitParts")));
            if (Value(Number((env.get("fileSplitCount").num.value > Value::from_double(1).num.value) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(Value(Number(env.get("fileSplitCount").num.value - Value::from_double(1).num.value)));
                    args.push_back(env.get("fileSplitParts"));
                    env.set("RESPONSE", getItem(env, args));
                }
                env.set("filePathRaw", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("filePathRaw"));
                    env.set("RESPONSE", trim(env, args));
                }
                env.set("trimmedPath", env.get("RESPONSE"));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("trimmedPath"));
                    env.set("RESPONSE", stripQuotes(env, args));
                }
                env.set("unquotedPath", env.get("RESPONSE"));
                env.set("fwLine", ((((((Value::from_string("file_write(") + env.get("QUOTE")) + env.get("unquotedPath")) + env.get("QUOTE")) + Value::from_string(", ")) + env.get("compiledContent")) + Value::from_string(");")));
                {
                    std::vector<Value> args;
                    args.push_back(env.get("fwLine"));
                    env.set("RESPONSE", emit(env, args));
                }
            }
        }
        return Value::from_double(0);
    }
    if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("Import")) ? 1 : 0)).num.value != 0) {
        return Value::from_double(0);
    }
    return Value::from_double(0);
    return Value::from_double(0);
}

Value compileFunctionDef(Environment& env, const std::vector<Value>& args) {
    env.set("funcNode", args[0]);
    env.set("g_node", env.get("funcNode"));
    env.set("funcName", map_get(env.get("g_node"), Value::from_string("name")));
    env.set("params", map_get(env.get("g_node"), Value::from_string("params")));
    env.set("body", map_get(env.get("g_node"), Value::from_string("body")));
    {
        std::vector<Value> args;
        args.push_back(((Value::from_string("Value ") + env.get("funcName")) + Value::from_string("(Environment& env, const std::vector<Value>& args) {")));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", indent(env, args));
    }
    if (Value(Number(!value_equals(env.get("params"), Value::from_string("")) ? 1 : 0)).num.value != 0) {
        env.set("paramSize", list_length(env.get("params")));
        env.set("g_bIdx", Value::from_double(0));
        while (Value(Number((env.get("g_bIdx").num.value < env.get("paramSize").num.value) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("g_bIdx"));
                args.push_back(env.get("params"));
                env.set("RESPONSE", getItem(env, args));
            }
            env.set("paramName", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("paramName"));
                env.set("RESPONSE", trim(env, args));
            }
            env.set("trimmedParam", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("trimmedParam"));
                args.push_back(((Value::from_string("args[") + env.get("g_bIdx")) + Value::from_string("]")));
                env.set("RESPONSE", buildEnvSet(env, args));
            }
            env.set("paramLine", env.get("RESPONSE"));
            {
                std::vector<Value> args;
                args.push_back(env.get("paramLine"));
                env.set("RESPONSE", emit(env, args));
            }
            env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
        }
    }
    env.set("bodySize", list_length(env.get("body")));
    env.set("g_bIdx", Value::from_double(0));
    while (Value(Number((env.get("g_bIdx").num.value < env.get("bodySize").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_bIdx"));
            args.push_back(env.get("body"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("child", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("child"));
            env.set("RESPONSE", compileNode(env, args));
        }
        env.set("g_bIdx", (env.get("g_bIdx") + Value::from_double(1)));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("return Value::from_double(0);"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", dedent(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("}"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string(""));
        env.set("RESPONSE", emit(env, args));
    }
    return Value::from_double(0);
    return Value::from_double(0);
}

int main(int argc, char* argv[]) {
    Environment env(argc, argv);
    env.set("g_output", Value::from_list({}));
    env.set("g_indent", Value::from_double(0));
    env.set("g_idx", Value::from_double(0));
    env.set("g_i", Value::from_double(0));
    env.set("g_bIdx", Value::from_double(0));
    env.set("g_node", Value::from_map({}));
    env.set("g_compiled", Value::from_string(""));
    env.set("g_functions", Value::from_list({}));
    env.set("g_mainStmts", Value::from_list({}));
    env.set("g_myAst", Value::from_list({}));
    env.set("quoteSource", Value::from_string("a\"b"));
    env.set("QUOTE", char_at(env.get("quoteSource"), Value::from_double(1)));
    env.set("argCount", list_length(env.get("ARGV")));
    env.set("filePath", Value::from_string("examples/hello.mish"));
    if (Value(Number((env.get("argCount").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            args.push_back(env.get("ARGV"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("filePath", env.get("RESPONSE"));
    }
    print(Value::from_string("Compiling: "));
    print(env.get("filePath"));
    print(Value::from_string(""));
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
    env.set("g_myAst", Value::from_list({}));
    while (Value(Number((env.get("g_pos").num.value < env.get("g_lineCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(Value::from_double(0));
            env.set("RESPONSE", parseStatement(env, args));
        }
        env.set("node", env.get("g_result"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("type"));
            args.push_back(env.get("node"));
            env.set("RESPONSE", mapGet(env, args));
        }
        env.set("nodeType", env.get("RESPONSE"));
        if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("Empty")) ? 1 : 0)).num.value != 0) {
            if (Value(Number(!value_equals(env.get("nodeType"), Value::from_string("Comment")) ? 1 : 0)).num.value != 0) {
                {
                    std::vector<Value> args;
                    args.push_back(env.get("node"));
                    args.push_back(env.get("g_myAst"));
                    env.set("RESPONSE", append(env, args));
                }
                env.set("newAst", env.get("RESPONSE"));
                env.set("g_myAst", env.get("newAst"));
            }
        }
    }
    env.set("g_output", Value::from_list({}));
    env.set("g_indent", Value::from_double(0));
    env.set("g_functions", Value::from_list({}));
    env.set("g_mainStmts", Value::from_list({}));
    env.set("astSize", list_length(env.get("g_myAst")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("astSize").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_myAst"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("node", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(Value::from_string("type"));
            args.push_back(env.get("node"));
            env.set("RESPONSE", mapGet(env, args));
        }
        env.set("nodeType", env.get("RESPONSE"));
        if (Value(Number(value_equals(env.get("nodeType"), Value::from_string("FunctionDef")) ? 1 : 0)).num.value != 0) {
            {
                std::vector<Value> args;
                args.push_back(env.get("node"));
                args.push_back(env.get("g_functions"));
                env.set("RESPONSE", append(env, args));
            }
            env.set("newFuncs2", env.get("RESPONSE"));
            env.set("g_functions", env.get("newFuncs2"));
        }
        else {
            {
                std::vector<Value> args;
                args.push_back(env.get("node"));
                args.push_back(env.get("g_mainStmts"));
                env.set("RESPONSE", append(env, args));
            }
            env.set("newMain2", env.get("RESPONSE"));
            env.set("g_mainStmts", env.get("newMain2"));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    {
        std::vector<Value> args;
        args.push_back((((Value::from_string("#include ") + env.get("QUOTE")) + Value::from_string("midshake_runtime.hpp")) + env.get("QUOTE")));
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
    env.set("funcCount", list_length(env.get("g_functions")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("funcCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_functions"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("funcNode", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("funcNode"));
            env.set("RESPONSE", compileFunctionDef(env, args));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("int main(int argc, char* argv[]) {"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", indent(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("Environment env(argc, argv);"));
        env.set("RESPONSE", emit(env, args));
    }
    env.set("mainCount", list_length(env.get("g_mainStmts")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("mainCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_mainStmts"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("stmt", env.get("RESPONSE"));
        {
            std::vector<Value> args;
            args.push_back(env.get("stmt"));
            env.set("RESPONSE", compileNode(env, args));
        }
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("return 0;"));
        env.set("RESPONSE", emit(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_double(0));
        env.set("RESPONSE", dedent(env, args));
    }
    {
        std::vector<Value> args;
        args.push_back(Value::from_string("}"));
        env.set("RESPONSE", emit(env, args));
    }
    env.set("cppOutput", Value::from_string(""));
    env.set("outCount", list_length(env.get("g_output")));
    env.set("g_idx", Value::from_double(0));
    while (Value(Number((env.get("g_idx").num.value < env.get("outCount").num.value) ? 1 : 0)).num.value != 0) {
        {
            std::vector<Value> args;
            args.push_back(env.get("g_idx"));
            args.push_back(env.get("g_output"));
            env.set("RESPONSE", getItem(env, args));
        }
        env.set("line", env.get("RESPONSE"));
        if (Value(Number((env.get("g_idx").num.value > Value::from_double(0).num.value) ? 1 : 0)).num.value != 0) {
            env.set("cppOutput", (env.get("cppOutput") + Value::from_string("\n")));
        }
        env.set("cppOutput", (env.get("cppOutput") + env.get("line")));
        env.set("g_idx", (env.get("g_idx") + Value::from_double(1)));
    }
    file_write("output/generated.cpp", env.get("cppOutput"));
    print(Value::from_string(""));
    print(Value::from_string("Generated C++ code written to output/generated.cpp"));
    print(Value::from_string("Total lines: "));
    print(env.get("outCount"));
    print(Value::from_string(""));
    print(Value::from_string("--- Generated C++ ---"));
    print(env.get("cppOutput"));
    print(Value::from_string(""));
    print(Value::from_string("Compilation complete!"));
    return 0;
}