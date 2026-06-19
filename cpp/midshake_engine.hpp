#pragma once

#include <string>
#include <vector>
#include <memory>
#include <unordered_map>
#include <variant>
#include <optional>

// ===== Tokens =====

enum class TokenType {
    EndOfFile,
    Identifier,
    Number,
    String,
    Let,
    Be,
    Plus,
    Minus,
    Star,
    Slash,
    LeftParen,
    RightParen,
    Newline,
};

struct Token {
    TokenType type;
    std::string text;
};

// ===== Lexer =====

class Lexer {
public:
    explicit Lexer(const std::string &source);

    std::vector<Token> tokenize();

private:
    std::string source;
    std::size_t pos = 0;

    char peek() const;
    char advance();
    bool isAtEnd() const;

    void skipWhitespace();
    Token stringLiteral();
    Token identifier();
    Token number();
};

// ===== AST: Expressions =====

enum class ExprType {
    Number,
    Binary,
    Variable,
    String
};

struct Expression {
    ExprType type;
    explicit Expression(ExprType t) : type(t) {}
    virtual ~Expression() = default;
};

struct NumberExpr : public Expression {
    double value;
    explicit NumberExpr(double v) : Expression(ExprType::Number), value(v) {}
};

struct StringExpr : public Expression {
    std::string value;
    explicit StringExpr(const std::string &v)
        : Expression(ExprType::String), value(v) {}
};

enum class BinaryOp {
    Add,
    Sub,
    Mul,
    Div,
};

struct BinaryExpr : public Expression {
    BinaryOp op;
    std::shared_ptr<Expression> left;
    std::shared_ptr<Expression> right;

    BinaryExpr(BinaryOp o,
               std::shared_ptr<Expression> l,
               std::shared_ptr<Expression> r)
        : Expression(ExprType::Binary), op(o), left(std::move(l)), right(std::move(r)) {}
};

struct VariableExpr : public Expression {
    std::string name;
    explicit VariableExpr(const std::string &n)
        : Expression(ExprType::Variable), name(n) {}
};

// ===== AST: Statements =====

struct VariableDeclaration {
    std::string name;
    std::shared_ptr<Expression> value;
};

struct ExpressionStatement {
    std::shared_ptr<Expression> expr;
};

using Statement = std::variant<VariableDeclaration, ExpressionStatement>;

// ===== Parser =====

class Parser {
public:
    explicit Parser(const std::vector<Token> &tokens);

    std::vector<Statement> parse();

private:
    const std::vector<Token> &tokens;
    std::size_t current = 0;

    bool isAtEnd() const;
    const Token &peek() const;
    const Token &previous() const;
    const Token &advance();
    bool check(TokenType type) const;
    bool match(TokenType type);
    const Token &consume(TokenType type, const std::string &message);

    // Statements
    Statement parseStatement();
    VariableDeclaration parseVariableDeclaration();
    ExpressionStatement parseExpressionStatement();

    // Expressions
    std::shared_ptr<Expression> parseExpression();
    std::shared_ptr<Expression> parseTerm();
    std::shared_ptr<Expression> parseFactor();
    std::shared_ptr<Expression> parsePrimary();
};

// ===== Runtime / Interpreter =====

using Value = std::variant<double, std::string>;

class Interpreter {
public:
    Interpreter() = default;

    Value evaluate(const std::vector<Statement> &program);

private:
    std::unordered_map<std::string, Value> variables;

    Value evalExpression(const std::shared_ptr<Expression> &expr);
    void execStatement(const Statement &stmt);
    void execVariableDeclaration(const VariableDeclaration &decl);
    void execExpressionStatement(const ExpressionStatement &stmt);
};

// ===== Public API =====

// Tokenize + parse + evaluate a MidShake program string.
// Returns the last expression value (or 0 if none).
Value run_midshake(const std::string &source);

// Tokenize only (for Python bindings / debugging).
std::vector<Token> tokenize_midshake(const std::string &source);

