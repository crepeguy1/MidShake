# MidShake Syntax Highlighting for JetBrains IDEs

TextMate bundle for MidShake (`.mish`) syntax highlighting in IntelliJ IDEA, PyCharm, WebStorm, and all other JetBrains IDEs.

No compilation or Java SDK required — just import the bundle through your IDE settings.

## Features

- **Block keywords**: `IF`, `WHILST`, `DEFINE`, `FUNCTION`, `END IF`, `END WHILST`, `END FUNCTION`, `END FOR`, `ELSE`, `RETURN`, `TERMINATE`, `BREAK`, `CONTINUE`
- **Statement keywords**: `LET`, `SET`, `PROCLAIM`, `CALL`, `INQUIRE`, `FOR`, `GLOBAL`, `WRITE`
- **Expression prefixes**: `the value of`, `the length of`, `the character at`, `the content of the file`, etc.
- **Built-in functions**: `startsWith`, `endsWith`, `isDigit`, `min`, `max`, `abs`, `round`, `toupper`, `tolower`, `mapGet`, `mapSet`, `readFile`, etc.
- **Operators**: `plus`, `minus`, `times`, `divided by`, `modulo`, `IS greater than`, `IS equal to`, `AND`, `OR`, `NOT`
- **Symbolic operators**: `+`, `-`, `*`, `/`, `=`, `<`, `>`, `!`
- **Strings**: Double-quoted strings with escape sequences
- **Numbers**: Integers and floats
- **Booleans**: `true`, `false`
- **Comments**: `^` and `#` style comments
- **Punctuation**: Semicolons, brackets, braces, parentheses

## Installation

### Method 1: Import TextMate Bundle (Recommended)

1. Open your JetBrains IDE
2. Go to `File` → `Settings` → `Editor` → `TextMate Bundles` (or `IntelliJ IDEA` → `Preferences` → `Editor` → `TextMate Bundles` on macOS)
   - Use `Ctrl+Alt+S` to open Settings
3. Click the **+** (Add) button
4. Navigate to this folder (`ide/intellij/`) and select it
5. The bundle appears in the list — click **OK**
6. Open a `.mish` file and syntax highlighting activates automatically

### Method 2: User-Defined File Type (Alternative)

If TextMate Bundles is not available in your IDE:

1. Go to `File` → `Settings` → `Editor` → `File Types`
2. Under **Recognized File Types**, click **Add** (+)
3. Name it "MidShake" with description "MidShake source file"
4. Add `.mish` and `.ms` to **File name patterns**
5. Under **Syntax Highlighting**, configure:
   - **Line comment**: `^` and `#`
   - **Block comment**: (none)
   - Check **Support paired braces**, **brackets**, **parens**, and **string escapes**
6. Under **Keywords**, add MidShake keywords in up to 4 groups (each group gets a different color)
7. Click **OK**

You can customize the colors at `File` → `Settings` → `Editor` → `Color Scheme` → `User-Defined File Types`.

## File Structure

```
ide/intellij/
├── README.md                          # This file
├── info.plist                         # Bundle metadata (required)
└── Syntaxes/
    ├── midshake.tmLanguage.json       # TextMate grammar definition
    └── midshake.tmPreferences         # Color theme preferences
```

## Supported File Extensions

- `.mish` (primary)
- `.ms` (legacy)

## Compatibility

Works with all JetBrains IDEs that support TextMate Bundles:

- IntelliJ IDEA (Community & Ultimate)
- PyCharm
- WebStorm
- PhpStorm
- RubyMine
- CLion
- GoLand
- Rider
- Android Studio
- DataGrip
- AppCode

## Color Scheme Reference

| Element | Color | Style |
|---------|-------|-------|
| Block keywords | Blue (#569CD6) | Bold |
| Statement keywords | Purple (#C586C0) | Bold |
| Expression prefixes | Teal (#4EC9B0) | Italic |
| Operators | Yellow (#DCDCAA) | Bold |
| Built-in functions | Yellow (#DCDCAA) | Italic |
| Strings | Orange (#CE9178) | — |
| Numbers | Green (#B5CEA8) | — |
| Booleans | Blue (#569CD6) | Bold |
| Comments | Green (#6A9955) | Italic |
| Variable types | Light blue (#9CDCFE) | Italic |
