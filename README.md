# Log Highlight for Sublime Text
==================================

Log Highlight helps to view log with customizable error/warning syntax & color scheme.  
Open `.log` file and run `Log Highlight` in context menu or `Log Highlight : Highlight Error/Warning` in the command palette.

## Features
***********

 * Customizable Syntax & Color Scheme
 * Add Bookmarks Automatically for Navigating Errors/Warnings
 * Support Go To Position in a Log by `result_file_regex`
 * Search a Base Directory Automatically for Relative Path Link
 * Summary Output Panel

#### Customizable Syntax & Color Scheme

After changing syntax and color scheme in **settings**, run `Log Hightlight: Generate Custom Syntax & Theme` command. You may have to restart sublime text once.

#### Bookmarks

When errors/warnings found, it will add bookmarks for them. You can navigate easily with new key binding (`alt+pagedown/up`)

#### Go To Position

By double-click, you can go to positions of links like `"../../abc.cpp", 32` or `./abc.v line 234` in a log. For relative path, it may automatically search a base directory near the log file

#### Summary Output Panel

By default, it summarizes error/warning list in a new output panel at the bottom of window

#### etc

From v0.4.0, you can highlight links and quotes inside of begin regex, end regex and match regex. by using special words `{{{LINK}}}`, `{{{QUOTE}}}`
It can be used like gcc style error message : `./src/abc.cpp:40:2 error ...`

#### Settings :

```java
{
	// enable context menu
	"context_menu": true,

	// log file extension
	"log_ext": [ ".log" ],

	// error pattern set (regular expression)
	// [ "begin regex", "end regex" ] or [ "match regex", "" ]
	//
	// non-regex special word (sensitive case) : {{{LINK}}}, {{{QUOTE}}}
	//  -> They will be replaced with regex capturing groups in "begin regex", "end regex" or "match regex" for LINK regex, QUOTE regex
	//
	//  e.g.) ../src/foo.cpp:40 error: ../src/foo.cpp:40
	//      - You don't need to use {{{LINK}}} to highlight second `../src/foo.cpp` link, because it is inside of begin ~ end
	//      - [ "^[\\r\\n].*?(?i)error", "[\\r\\n]" ] is enough for 2nd link
	//      - For 1st link, the former setting can't, because it is outside of begin ~ end
	//      - You have to put {{{LINK}}} like [ "^{{{LINK}}}?[^\\r\\n]*?(?i)error", "[\\r\\n]" ]

	"error_pattern": [
		[ "^Error-\\[", "^\\s*[\\n]" ],                      // Error-[ ~ next empty line
		[ "^{{{LINK}}}?[^\\r\\n]*?(?i)error", "[\\r\\n]" ]   // lines including 'error' with ignore case with a link in front of 'error'
	],

	// warning pattern set (regular expression)
	// [ "begin regex", "end regex" ] or [ "match regex", "" ]
	//
	// non-regex special word (sensitive case) : {{{LINK}}}, {{{QUOTE}}}
	//  -> see error pattern description

	"warning_pattern": [
		[ "^Warning-\\[", "^\\s*[\\n]" ],                    // Warning-[ ~ next empty line
		[ "^{{{LINK}}}?[^\\r\\n]*?(?i)warning", "[\\r\\n]" ] // lines including 'warning' with ignore case with a link in front of 'warning'
	],

	// theme color set
	"theme_color": [
		"#272822", // background
		"#ffffff", // foreground
		"#ffffff", // caret
		"#555555", // selection
		"#555555", // selectionBorder
		"#272822", // lineHighlight
		"#F92672", // error message
		"#ffff00", // link in error message
		"#66D9EF", // quote in error message
		"#A6E22E", // warning message
		"#FD971F", // link in warning message
		"#66D9EF", // quote in warning message
		"#FFFFFF"  // summary title
	],

	// summary panel
	"summary_panel": true,  // show summary panel
	"error_only": false,    // display only errors in the summary panel
	"show_keymap": true     // display summary panel key map information
}
```

![Image of Log Highlight](https://raw.githubusercontent.com/poucotm/Links/master/image/log_highlight.gif)

## issues

When you have an issue, tell me through [https://github.com/poucotm/Log-Highlight/issues](https://github.com/poucotm/Log-Highlight/issues), or send me an e-mail poucotm@gmail.com, yongchan.jeon@samsung.com