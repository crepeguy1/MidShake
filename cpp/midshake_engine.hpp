#pragma once

#include <string>
#include <vector>
#include <memory>

// ---------------------------
// Tokens
// ---------------------------

enum class TokenType {
    Identifier,
    Number,
    String,
    Keyword,
    Symbol,
    EndOfFile
};

struct Token {
    TokenType type;
    std::string value;
    int line;
    int column;
};

std::vector<Token> tokenize(const std::string& source);

// ---------------------------
// AST Forward Declarations
// ---------------------------

struct Expression;
struct Statement;

using ExprPtr = std::shared_ptr<Expression>;
using StmtPtr = std::shared_ptr<Statement>;

// ---------------------------
// Expressions
// ---------------------------

enum class ExprType {
    Number,
    String,
    Variable,
    Binary,
    Unary
};

struct Expression {
    ExprType type;
    Expression(ExprType t) : type(t) {}
    virtual ~Expression() = default;
};

struct NumberExpr : public Expression {
    double value;
    NumberExpr(double v) : Expression(ExprType::Number), value(v) {}
};

struct StringExpr : public Expression {
    std::string value;
    StringExpr(const std::string& v) : Expression(ExprType::String), value(v) {}
};

struct VariableExpr : public Expression {
    std::string name;
    VariableExpr(const std::string& n) : Expression(ExprType::Variable), name(n) {}
};

struct UnaryExpr : public Expression {
    std::string op;
    ExprPtr right;
    UnaryExpr(const std::string& o, ExprPtr r)
        : Expression(ExprType::Unary), op(o), right(r) {}
};

struct BinaryExpr : public Expression {
    ExprPtr left;
    std::string op;
    ExprPtr right;
    BinaryExpr(ExprPtr l, const std::string& o, ExprPtr r)
        : Expression(ExprType::Binary), left(l), op(o), right(r) {}
};

// ---------------------------
// Statements
// ---------------------------

enum class StmtType {
    Print,
    VarAssign,
    Block,
    If,
    While
};

struct Statement {
    StmtType type;
    Statement(StmtType t) : type(t) {}
    virtual ~Statement() = default;
};

struct PrintStmt : public Statement {
    ExprPtr value;
    PrintStmt(ExprPtr v) : Statement(StmtType::Print), value(v) {}
};

struct VarAssignStmt : public Statement {
    std::string name;
    ExprPtr value;
    VarAssignStmt(const std::string& n, ExprPtr v)
        : Statement(StmtType::VarAssign), name(n), value(v) {}
};

struct BlockStmt : public Statement {
    std::vector<StmtPtr> statements;
    BlockStmt() : Statement(StmtType::Block) {}
};

struct IfStmt : public Statement {
    ExprPtr condition;
    StmtPtr thenBranch;
    StmtPtr elseBranch;
    IfStmt(ExprPtr cond, StmtPtr thenB, StmtPtr elseB)
        : Statement(StmtType::If), condition(cond), thenBranch(thenB), elseBranch(elseB) {}
};

struct WhileStmt : public Statement {
    ExprPtr condition;
    StmtPtr body;
    WhileStmt(ExprPtr cond, StmtPtr b)
        : Statement(StmtType::While), condition(cond), body(b) {}
};

// ---------------------------
// Parser
// ---------------------------

struct Parser {
    Parser(const std::vector<Token>& tokens);

    std::vector<StmtPtr> parse();

private:
    const std::vector<Token>& tokens;
    size_t current;

    const Token& peek() const;
    const Token& previous() const;
    bool isAtEnd() const;
    bool check(TokenType type) const;
    bool match(TokenType type);
    bool matchKeyword(const std::string& kw);
    const Token& consume(TokenType type, const std::string& message);
    void error(const std::string& message) const;

    StmtPtr declaration();
    StmtPtr statement();
    StmtPtr printStatement();
    StmtPtr varAssignStatement();
    StmtPtr ifStatement();
    StmtPtr whileStatement();
    StmtPtr blockStatement();

    ExprPtr expression();
    ExprPtr equality();
    ExprPtr comparison();
    ExprPtr term();
    ExprPtr factor();
    ExprPtr unary();
    ExprPtr primary();
};

