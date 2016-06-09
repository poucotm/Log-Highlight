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

After changing syntax and color scheme in settings, run `Log Hightlight: Generate Custom Syntax & Theme` command. You may have to restart sublime text once.

#### Bookmarks

When errors/warnings found, it will add bookmarks for them. You can navigate easily with new key binding (`alt+pagedown / up`)

#### Go To Position

By double-click, you can go to positions of links like `"../../abc.cpp", 32` or `./abc.v line 234` in a log. For relative path, it may automatically searche a base directory near the log file

#### Summary Output Panel

By default, it summarizes error/warning list in a new output panel at the bottom of window

Settings :
```java
{
	// enable context menu
	"context_menu": true,

	// log file extension
	"log_ext": [ ".log" ],

	// error pattern set (regular expression)
	// [ "begin regex", "end regex" ] or [ "match regex", "" ]
	"error_pattern": [
		[ "^Error-\\[", "^\\s*[\\n]" ],           // Error-[ ~
		[ "^[^\\r\\n]*?(?i)error", "[\\r\\n]" ]   // lines including 'error' with ignore case
	],

	// warning pattern set (regular expression)
	// [ "begin regex", "end regex" ] or [ "match regex", "" ]
	"warning_pattern": [
		[ "^Warning-\\[", "^\\s*[\\n]" ],         // Warning-[ ~
		[ "^[^\\r\\n]*?(?i)warning", "[\\r\\n]" ] // lines including 'warning' with ignore case
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
	"summary_panel": true,	// show summary panel
	"error_only": false		// display only errors in the summary panel
}
```

![Image of Verilog Gadget](https://raw.githubusercontent.com/poucotm/Links/master/image/view_log.png)

## issues

When you have an issue, tell me through [https://github.com/poucotm/Log-Highlight/issues](https://github.com/poucotm/Log-Highlight/issues), or send me an e-mail poucotm@gmail.com, yongchan.jeon@samsung.com