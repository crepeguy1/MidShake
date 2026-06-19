#include "midshake_engine.hpp"

#include <cctype>
#include <stdexcept>
#include <sstream>

// ===== Lexer implementation =====

Lexer::Lexer(const std::string &source) : source(source) {}

char Lexer::peek() const {
    if (isAtEnd()) return '\0';
    return source[pos];
}

char Lexer::advance() {
    if (isAtEnd()) return '\0';
    return source[pos++];
}

bool Lexer::isAtEnd() const {
    return pos >= source.size();
}

void Lexer::skipWhitespace() {
    while (!isAtEnd()) {
        char c = peek();
        if (c == ' ' || c == '\t' || c == '\r') {
            advance();
        } else {
            break;
        }
    }
}

Token Lexer::identifier() {
    std::size_t start = pos - 1;
    while (!isAtEnd() && (std::isalnum(peek()) || peek() == '_')) {
        advance();
    }
    std::string text = source.substr(start, pos - start);

    if (text == "LET") {
        return {TokenType::Let, text};
    } else if (text == "BE") {
        return {TokenType::Be, text};
    }

    return {TokenType::Identifier, text};
}

Token Lexer::number() {
    std::size_t start = pos - 1;
    while (!isAtEnd() && std::isdigit(peek())) {
        advance();
    }
    if (!isAtEnd() && peek() == '.') {
        advance();
        while (!isAtEnd() && std::isdigit(peek())) {
            advance();
        }
    }
    std::string text = source.substr(start, pos - start);
    return {TokenType::Number, text};
}

Token Lexer::stringLiteral() {
    std::string result;
    while (!isAtEnd() && peek() != '"') {
        result += advance();
    }
    advance(); // closing quote
    return {TokenType::String, result};
}

std::vector<Token> Lexer::tokenize() {
    std::vector<Token> tokens;

    while (!isAtEnd()) {
        skipWhitespace();
        if (isAtEnd()) break;

        char c = advance();

        if (std::isalpha(c) || c == '_') {
            tokens.push_back(identifier());
        } else if (std::isdigit(c)) {
            tokens.push_back(number());
        } else if (c == '"') {
            tokens.push_back(stringLiteral());
            continue;
        } else {
            switch (c) {
            case '+': tokens.push_back({TokenType::Plus, "+"}); break;
            case '-': tokens.push_back({TokenType::Minus, "-"}); break;
            case '*': tokens.push_back({TokenType::Star, "*"}); break;
            case '/': tokens.push_back({TokenType::Slash, "/"}); break;
            case '(': tokens.push_back({TokenType::LeftParen, "("}); break;
            case ')': tokens.push_back({TokenType::RightParen, ")"}); break;
            case '\n': tokens.push_back({TokenType::Newline, "\\n"}); break;
            default:
                // ignore unknown for now or throw
                break;
            }
        }
    }

    tokens.push_back({TokenType::EndOfFile, ""});
    return tokens;
}

// ===== Parser implementation =====

Parser::Parser(const std::vector<Token> &tokens) : tokens(tokens) {}

bool Parser::isAtEnd() const {
    return peek().type == TokenType::EndOfFile;
}

const Token &Parser::peek() const {
    return tokens[current];
}

const Token &Parser::previous() const {
    return tokens[current - 1];
}

const Token &Parser::advance() {
    if (!isAtEnd()) current++;
    return previous();
}

bool Parser::check(TokenType type) const {
    if (isAtEnd()) return false;
    return peek().type == type;
}

bool Parser::match(TokenType type) {
    if (check(type)) {
        advance();
        return true;
    }
    return false;
}

const Token &Parser::consume(TokenType type, const std::string &message) {
    if (check(type)) return advance();
    throw std::runtime_error("Parse error: " + message);
}

std::vector<Statement> Parser::parse() {
    std::vector<Statement> stmts;
    while (!isAtEnd()) {
        // skip stray newlines
        while (match(TokenType::Newline)) {}
        if (isAtEnd()) break;
        stmts.push_back(parseStatement());
    }
    return stmts;
}

Statement Parser::parseStatement() {
    if (match(TokenType::Let)) {
        // we already consumed LET, so back up one step in parseVariableDeclaration
        current--; // undo match
        return parseVariableDeclaration();
    }
    return parseExpressionStatement();
}

VariableDeclaration Parser::parseVariableDeclaration() {
    consume(TokenType::Let, "Expected 'LET' at start of variable declaration.");
    std::string name = consume(TokenType::Identifier, "Expected variable name.").text;
    consume(TokenType::Be, "Expected 'BE' after variable name.");
    auto expr = parseExpression();

    // optional newline
    match(TokenType::Newline);

    return VariableDeclaration{name, expr};
}

ExpressionStatement Parser::parseExpressionStatement() {
    auto expr = parseExpression();
    // optional newline
    match(TokenType::Newline);
    return ExpressionStatement{expr};
}

std::shared_ptr<Expression> Parser::parseExpression() {
    return parseTerm();
}

std::shared_ptr<Expression> Parser::parseTerm() {
    auto expr = parseFactor();

    while (true) {
        if (match(TokenType::Plus)) {
            auto right = parseFactor();
            expr = std::make_shared<BinaryExpr>(BinaryOp::Add, expr, right);
        } else if (match(TokenType::Minus)) {
            auto right = parseFactor();
            expr = std::make_shared<BinaryExpr>(BinaryOp::Sub, expr, right);
        } else {
            break;
        }
    }

    return expr;
}

std::shared_ptr<Expression> Parser::parseFactor() {
    auto expr = parsePrimary();

    while (true) {
        if (match(TokenType::Star)) {
            auto right = parsePrimary();
            expr = std::make_shared<BinaryExpr>(BinaryOp::Mul, expr, right);
        } else if (match(TokenType::Slash)) {
            auto right = parsePrimary();
            expr = std::make_shared<BinaryExpr>(BinaryOp::Div, expr, right);
        } else {
            break;
        }
    }

    return expr;
}

std::shared_ptr<Expression> Parser::parsePrimary() {
    if (match(TokenType::Number)) {
        double v = std::stod(previous().text);
        return std::make_shared<NumberExpr>(v);
    }

    if (match(TokenType::Identifier)) {
        std::string name = previous().text;
        return std::make_shared<VariableExpr>(name);
    }

    if (match(TokenType::String)) {
        return std::make_shared<StringExpr>(previous().text);
    }

    if (match(TokenType::LeftParen)) {
        auto expr = parseExpression();
        consume(TokenType::RightParen, "Expected ')' after expression.");
        return expr;
    }

    throw std::runtime_error("Parse error: expected expression.");
}

// ===== Interpreter implementation =====

Value Interpreter::evaluate(const std::vector<Statement> &program) {
    Value last = 0.0;
    for (const auto &stmt : program) {
        execStatement(stmt);
        if (std::holds_alternative<ExpressionStatement>(stmt)) {
            const auto &es = std::get<ExpressionStatement>(stmt);
            last = evalExpression(es.expr);
        }
    }
    return last;
}

void Interpreter::execStatement(const Statement &stmt) {
    if (std::holds_alternative<VariableDeclaration>(stmt)) {
        execVariableDeclaration(std::get<VariableDeclaration>(stmt));
    } else if (std::holds_alternative<ExpressionStatement>(stmt)) {
        execExpressionStatement(std::get<ExpressionStatement>(stmt));
    }
}

void Interpreter::execVariableDeclaration(const VariableDeclaration &decl) {
    Value v = evalExpression(decl.value);
    variables[decl.name] = v;
}

void Interpreter::execExpressionStatement(const ExpressionStatement &stmt) {
    (void)evalExpression(stmt.expr); // ignore result here
}

static bool isString(const Value &value) {
    return std::holds_alternative<std::string>(value);
}

static std::string toString(const Value &value) {
    if (std::holds_alternative<std::string>(value)) {
        return std::get<std::string>(value);
    }
    std::ostringstream oss;
    oss << std::get<double>(value);
    return oss.str();
}

static double getNumber(const Value &value) {
    if (!std::holds_alternative<double>(value)) {
        throw std::runtime_error("Runtime error: expected numeric value");
    }
    return std::get<double>(value);
}

Value Interpreter::evalExpression(const std::shared_ptr<Expression> &expr) {
    switch (expr->type) {
    case ExprType::Number: {
        auto *n = static_cast<NumberExpr *>(expr.get());
        return n->value;
    }
    case ExprType::String: {
        auto *s = static_cast<StringExpr *>(expr.get());
        return s->value;
    }
    case ExprType::Binary: {
        auto *b = static_cast<BinaryExpr *>(expr.get());
        Value left = evalExpression(b->left);
        Value right = evalExpression(b->right);
        switch (b->op) {
        case BinaryOp::Add: {
            if (isString(left) || isString(right)) {
                return toString(left) + toString(right);
            }
            return getNumber(left) + getNumber(right);
        }
        case BinaryOp::Sub: {
            return getNumber(left) - getNumber(right);
        }
        case BinaryOp::Mul: {
            return getNumber(left) * getNumber(right);
        }
        case BinaryOp::Div: {
            double rhs = getNumber(right);
            return rhs != 0 ? getNumber(left) / rhs : 0;
        }
        }
        break;
    }
    case ExprType::Variable: {
        auto *v = static_cast<VariableExpr *>(expr.get());
        auto it = variables.find(v->name);
        if (it == variables.end()) {
            std::ostringstream oss;
            oss << "Runtime error: undefined variable '" << v->name << "'";
            throw std::runtime_error(oss.str());
        }
        return it->second;
    }
    }

    throw std::runtime_error("Runtime error: unknown expression type.");
}

// ===== Public API =====

Value run_midshake(const std::string &source) {
    Lexer lexer(source);
    auto tokens = lexer.tokenize();

    Parser parser(tokens);
    auto program = parser.parse();

    Interpreter interp;
    return interp.evaluate(program);
}

std::vector<Token> tokenize_midshake(const std::string &source) {
    Lexer lexer(source);
    return lexer.tokenize();
}
