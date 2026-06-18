#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "../cpp/midshake_engine.hpp"

namespace py = pybind11;

// Convert AST nodes into Python-friendly structures
// (simple dicts so Python can inspect them)
py::dict expr_to_dict(const ExprPtr& expr) {
    py::dict d;

    switch (expr->type) {
        case ExprType::Number: {
            auto* e = static_cast<NumberExpr*>(expr.get());
            d["type"] = "Number";
            d["value"] = e->value;
            break;
        }
        case ExprType::String: {
            auto* e = static_cast<StringExpr*>(expr.get());
            d["type"] = "String";
            d["value"] = e->value;
            break;
        }
        case ExprType::Variable: {
            auto* e = static_cast<VariableExpr*>(expr.get());
            d["type"] = "Variable";
            d["name"] = e->name;
            break;
        }
        case ExprType::Unary: {
            auto* e = static_cast<UnaryExpr*>(expr.get());
            d["type"] = "Unary";
            d["op"] = e->op;
            d["right"] = expr_to_dict(e->right);
            break;
        }
        case ExprType::Binary: {
            auto* e = static_cast<BinaryExpr*>(expr.get());
            d["type"] = "Binary";
            d["op"] = e->op;
            d["left"] = expr_to_dict(e->left);
            d["right"] = expr_to_dict(e->right);
            break;
        }
    }

    return d;
}

py::dict stmt_to_dict(const StmtPtr& stmt) {
    py::dict d;

    switch (stmt->type) {
        case StmtType::Print: {
            auto* s = static_cast<PrintStmt*>(stmt.get());
            d["type"] = "Print";
            d["value"] = expr_to_dict(s->value);
            break;
        }
        case StmtType::VarAssign: {
            auto* s = static_cast<VarAssignStmt*>(stmt.get());
            d["type"] = "VarAssign";
            d["name"] = s->name;
            d["value"] = expr_to_dict(s->value);
            break;
        }
        case StmtType::Block: {
            auto* s = static_cast<BlockStmt*>(stmt.get());
            d["type"] = "Block";
            py::list items;
            for (auto& st : s->statements) {
                items.append(stmt_to_dict(st));
            }
            d["statements"] = items;
            break;
        }
        case StmtType::If: {
            auto* s = static_cast<IfStmt*>(stmt.get());
            d["type"] = "If";
            d["condition"] = expr_to_dict(s->condition);
            d["then"] = stmt_to_dict(s->thenBranch);
            if (s->elseBranch)
                d["else"] = stmt_to_dict(s->elseBranch);
            break;
        }
        case StmtType::While: {
            auto* s = static_cast<WhileStmt*>(stmt.get());
            d["type"] = "While";
            d["condition"] = expr_to_dict(s->condition);
            d["body"] = stmt_to_dict(s->body);
            break;
        }
    }

    return d;
}

PYBIND11_MODULE(midshake_cpp, m) {
    m.doc() = "MidShake C++ engine bindings";

    // Expose tokenizer
    m.def("tokenize", &tokenize, "Tokenize MidShake source code");

    // Expose parser
    m.def("parse", [](const std::string& src) {
        auto tokens = tokenize(src);
        Parser parser(tokens);
        auto stmts = parser.parse();

        py::list out;
        for (auto& s : stmts) {
            out.append(stmt_to_dict(s));
        }
        return out;
    });
}
