# MidShake IDE Syntax Highlighting

This folder contains syntax highlighting files for MidShake code in various editors.

## File Structure

```
ide/
├── sublime/
│   └── midshake.sublime-syntax    # Sublime Text syntax definition
├── vim/
│   └── midshake.vim               # Vim/Neovim syntax file
├── atom/
│   └── grammar.json               # Atom/TextMate grammar
└── intellij/                      # IntelliJ IDEA / JetBrains IDE TextMate bundle
    ├── README.md                  # Installation guide
    ├── info.plist                 # Bundle metadata (required)
    └── Syntaxes/
        ├── midshake.tmLanguage.json       # TextMate grammar
        └── midshake.tmPreferences         # Color theme preferences
```

## Installation

### Sublime Text

1. Open Sublime Text → `Preferences` → `Browse Packages...`
2. Create a new folder called `MidShake`
3. Copy `sublime/midshake.sublime-syntax` into it
4. Restart Sublime Text

### Vim / Neovim

1. Copy `vim/midshake.vim` to your syntax directory:
   - **Vim**: `~/.vim/syntax/midshake.vim`
   - **Neovim**: `~/.config/nvim/syntax/midshake.vim`
2. Add to your `vimrc` / `init.vim`:
   ```vim
   au BufRead,BufNewFile *.mish,*.ms setfiletype midshake
   filetype plugin indent on
   ```
3. Restart Vim/Neovim

### Atom

1. Copy `atom/grammar.json` to your package's `grammars/` folder
2. Add to your package's `package.json`:
   ```json
   {
     "grammars": [{
       "name": "MidShake",
       "scopeName": "source.midshake",
       "path": "grammars/grammar.json",
       "fileTypes": ["mish", "ms"]
     }]
   }
   ```

### IntelliJ IDEA / JetBrains IDEs

MidShake syntax highlighting works with all JetBrains IDEs via a **TextMate bundle** — no compilation or Java SDK needed.

**Quick install:**

1. Open your JetBrains IDE
2. Go to `File` → `Settings` → `Editor` → `TextMate Bundles` (`Ctrl+Alt+S`)
3. Click **+** (Add) and select the `ide/intellij/` folder
4. Click **OK** — syntax highlighting activates automatically for `.mish` files

**Alternative:** Use `Settings` → `Editor` → `File Types` to create a user-defined file type with keyword groups.

See `ide/intellij/README.md` for full details and a color scheme reference.

### VS Code / Cursor / Zed

VS Code support is built into the repo via the `.vscode/` folder. When you open the MidShake repo in VS Code, syntax highlighting activates automatically.

For a standalone VS Code extension, see the `midshake-vscode` project at `C:/Users/crepe/midshake-vscode`.

## Supported File Extensions

- `.mish` (primary)
- `.ms` (legacy)

## What's Highlighted

- **Keywords**: `LET`, `SET`, `PROCLAIM`, `IF`, `WHILST`, `DEFINE`, `CALL`, `IMPORT`, `RETURN`, `FOR`, `BREAK`, `CONTINUE`, `TERMINATE`
- **Block endings**: `END IF`, `END WHILST`, `END FUNCTION`, `END FOR`
- **Expression prefixes**: `the value of`, `the length of`, `the character at`, etc.
- **Built-in functions**: `startsWith`, `endsWith`, `isDigit`, `isLetter`, `min`, `max`, `abs`, `round`, etc.
- **Operators**: `plus`, `minus`, `times`, `divided by`, `modulo`, `IS equal to`, `AND`, `OR`, `NOT`
- **Strings**: Double-quoted strings with escape sequences
- **Numbers**: Integers and floats
- **Booleans**: `true`, `false`
- **Comments**: `^` and `#` style comments
- **Punctuation**: Semicolons, brackets, braces, parentheses
