#include "midshake_engine.hpp"

#include <cctype>
#include <stdexcept>

// ---------------------------
// Tokenizer helpers
// ---------------------------

static bool isIdentifierStart(char c) {
    return std::isalpha(static_cast<unsigned char>(c)) || c == '_';
}

static bool isIdentifierPart(char c) {
    return std::isalnum(static_cast<unsigned char>(c)) || c == '_';
}

static bool isDigit(char c) {
    return std::isdigit(static_cast<unsigned char>(c));
}

static bool isWhitespace(char c) {
    return c == ' ' || c == '\t' || c == '\r';
}

static bool isKeyword(const std::string& s) {
    static const std::vector<std::string> keywords = {
        "LET", "BE", "PROCLAIM", "ASK", "IF", "ELSE", "WHILST", "END"
    };
    for (const auto& k : keywords) {
        if (s == k) return true;
    }
    return false;
}

// ---------------------------
// Tokenize
// ---------------------------

std::vector<Token> tokenize(const std::string& source) {
    std::vector<Token> tokens;
    int line = 1;
    int col = 1;

    for (size_t i = 0; i < source.size(); ) {
        char c = source[i];

        // Newline
        if (c == '\n') {
            line++;
            col = 1;
            i++;
            continue;
        }

        // Whitespace
        if (isWhitespace(c)) {
            col++;
            i++;
            continue;
        }

        // Comment: # ...
        if (c == '#') {
            while (i < source.size() && source[i] != '\n') {
                i++;
                col++;
            }
            continue;
        }

        // String literal
        if (c == '"') {
            int startCol = col;
            i++;
            col++;
            std::string value;

            while (i < source.size() && source[i] != '"') {
                value.push_back(source[i]);
                i++;
                col++;
            }

            if (i >= source.size()) {
                throw std::runtime_error("Unterminated string literal");
            }

            i++;
            col++; // closing quote

            tokens.push_back({TokenType::String, value, line, startCol});
            continue;
        }

        // Number literal
        if (isDigit(c)) {
            int startCol = col;
            std::string value;

            while (i < source.size() && isDigit(source[i])) {
                value.push_back(source[i]);
                i++;
                col++;
            }

            tokens.push_back({TokenType::Number, value, line, startCol});
            continue;
        }

        // Identifier or keyword
        if (isIdentifierStart(c)) {
            int startCol = col;
            std::string value;

            while (i < source.size() && isIdentifierPart(source[i])) {
                value.push_back(source[i]);
                i++;
                col++;
            }

            if (isKeyword(value)) {
                tokens.push_back({TokenType::Keyword, value, line, startCol});
            } else {
                tokens.push_back({TokenType::Identifier, value, line, startCol});
            }
            continue;
        }

        // Symbol (single char)
        {
            int startCol = col;
            std::string value(1, c);
            tokens.push_back({TokenType::Symbol, value, line, startCol});
            i++;
            col++;
            continue;
        }
    }

    tokens.push_back({TokenType::EndOfFile, "", line, col});
    return tokens;
}

// ---------------------------
// Parser implementation
// ---------------------------

Parser::Parser(const std::vector<Token>& tokens)
    : tokens(tokens), current(0) {}

std::vector<StmtPtr> Parser::parse() {
    std::vector<StmtPtr> statements;
    while (!isAtEnd()) {
        statements.push_back(declaration());
    }
    return statements;
}

const Token& Parser::peek() const {
    return tokens[current];
}

const Token& Parser::previous() const {
    return tokens[current - 1];
}

bool Parser::isAtEnd() const {
    return peek().type == TokenType::EndOfFile;
}

bool Parser::check(TokenType type) const {
    if (isAtEnd()) return false;
    return peek().type == type;
}

bool Parser::match(TokenType type) {
    if (check(type)) {
        current++;
        return true;
    }
    return false;
}

bool Parser::matchKeyword(const std::string& kw) {
    if (isAtEnd()) return false;
    const Token& t = peek();
    if (t.type == TokenType::Keyword && t.value == kw) {
        current++;
        return true;
    }
    return false;
}

const Token& Parser::consume(TokenType type, const std::string& message) {
    if (check(type)) {
        current++;
        return previous();
    }
    error(message);
    throw std::runtime_error("Parse error");
}

void Parser::error(const std::string& message) const {
    const Token& t = peek();
    throw std::runtime_error(
        "Parse error at line " + std::to_string(t.line) +
        ", col " + std::to_string(t.column) + ": " + message
    );
}

// ---------------------------
// Declarations & statements
// ---------------------------

StmtPtr Parser::declaration() {
    // later: function declarations, etc.
    return statement();
}

StmtPtr Parser::statement() {
    if (matchKeyword("PROCLAIM")) return printStatement();
    if (matchKeyword("LET"))      return varAssignStatement();
    if (matchKeyword("IF"))       return ifStatement();
    if (matchKeyword("WHILST"))   return whileStatement();
    // fallback: treat as expression statement inside a block
    return blockStatement();
}

StmtPtr Parser::printStatement() {
    ExprPtr value = expression();
    return std::make_shared<PrintStmt>(value);
}

StmtPtr Parser::varAssignStatement() {
    // LET <identifier> BE <expr>
    const Token& nameTok = consume(TokenType::Identifier, "Expected variable name after LET.");
    if (!matchKeyword("BE")) {
        error("Expected BE after variable name.");
    }
    ExprPtr value = expression();
    return std::make_shared<VarAssignStmt>(nameTok.value, value);
}

StmtPtr Parser::ifStatement() {
    // IF <expr> <then-block> (ELSE <else-block>)? END
    ExprPtr condition = expression();

    StmtPtr thenBranch = blockStatement();
    StmtPtr elseBranch = nullptr;

    if (matchKeyword("ELSE")) {
        elseBranch = blockStatement();
    }

    if (!matchKeyword("END")) {
        error("Expected END after IF statement.");
    }

    return std::make_shared<IfStmt>(condition, thenBranch, elseBranch);
}

StmtPtr Parser::whileStatement() {
    // WHILST <expr> <body-block> END
    ExprPtr condition = expression();
    StmtPtr body = blockStatement();

    if (!matchKeyword("END")) {
        error("Expected END after WHILST block.");
    }

    return std::make_shared<WhileStmt>(condition, body);
}

StmtPtr Parser::blockStatement() {
    // Minimal version: treat a single statement as a block.
    auto block = std::make_shared<BlockStmt>();
    // For now, just parse a single print of an expression as the block content.
    // You’ll likely want to change this to a loop over multiple statements
    // once you define explicit block delimiters in the language.
    block->statements.push_back(
        std::make_shared<PrintStmt>(expression())
    );
    return block;
}

// ---------------------------
// Expressions
// ---------------------------

ExprPtr Parser::expression() {
    return equality();
}

ExprPtr Parser::equality() {
    ExprPtr expr = comparison();

    while (!isAtEnd() && peek().type == TokenType::Symbol &&
           (peek().value == "==" || peek().value == "!=")) {
        std::string op = peek().value;
        current++;
        ExprPtr right = comparison();
        expr = std::make_shared<BinaryExpr>(expr, op, right);
    }

    return expr;
}

ExprPtr Parser::comparison() {
    ExprPtr expr = term();

    while (!isAtEnd() && peek().type == TokenType::Symbol &&
           (peek().value == ">" || peek().value == ">=" ||
            peek().value == "<" || peek().value == "<=")) {
        std::string op = peek().value;
        current++;
        ExprPtr right = term();
        expr = std::make_shared<BinaryExpr>(expr, op, right);
    }

    return expr;
}

ExprPtr Parser::term() {
    ExprPtr expr = factor();

    while (!isAtEnd() && peek().type == TokenType::Symbol &&
           (peek().value == "+" || peek().value == "-")) {
        std::string op = peek().value;
        current++;
        ExprPtr right = factor();
        expr = std::make_shared<BinaryExpr>(expr, op, right);
    }

    return expr;
}

ExprPtr Parser::factor() {
    ExprPtr expr = unary();

    while (!isAtEnd() && peek().type == TokenType::Symbol &&
           (peek().value == "*" || peek().value == "/")) {
        std::string op = peek().value;
        current++;
        ExprPtr right = unary();
        expr = std::make_shared<BinaryExpr>(expr, op, right);
    }

    return expr;
}

ExprPtr Parser::unary() {
    if (!isAtEnd() && peek().type == TokenType::Symbol &&
        (peek().value == "-")) {
        std::string op = peek().value;
        current++;
        ExprPtr right = unary();
        return std::make_shared<UnaryExpr>(op, right);
    }
    return primary();
}

ExprPtr Parser::primary() {
    if (match(TokenType::Number)) {
        double value = std::stod(previous().value);
        return std::make_shared<NumberExpr>(value);
    }

    if (match(TokenType::String)) {
        return std::make_shared<StringExpr>(previous().value);
    }

    if (match(TokenType::Identifier)) {
        return std::make_shared<VariableExpr>(previous().value);
    }

    if (!isAtEnd() && peek().type == TokenType::Symbol && peek().value == "(") {
        current++; // consume '('
        ExprPtr expr = expression();
        if (!(peek().type == TokenType::Symbol && peek().value == ")")) {
            error("Expected ')' after expression.");
        }
        current++; // consume ')'
        return expr;
    }

    error("Expected expression.");
    throw std::runtime_error("Parse error");
}
