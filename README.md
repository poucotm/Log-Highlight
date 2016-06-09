# Log Highlight for Sublime Text
==================================

Log Highlight helps to view log with customizable error/warning syntax & color scheme.  
It is possible to go to positions of files in a log by double-click. Summary panel will be seen by default.  
It automatically generates bookmarks to navigate errors/warnings easily with new key bindings (`alt+pagedown/up`).  

There's two commands `Log Highlight: Highlight Error/Warning`, `Log Hightlight: Generate Custom Syntax & Theme`.  
You can change syntax, color scheme by changing settings and running latter command.  
After changing color scheme, you may have to restart sublime text once.

The context menu only can be seen for `.log` file.  
(file extensions can be added or changed in settings)

Settings :
```java
{
	// enable context menu
	"context_menu": true,

	// log file extension
	"log_ext": [ ".log" ],

	// error pattern set (regular expression)
	// [ "begin regex", "end regex" ]
	"error_pattern": [
		[ "^[^\\r\\n]+?(?i)error", "[\\r\\n]" ] // lines including 'error' with ignore case
	],

	// warning pattern set (regular expression)
	// [ "begin regex", "end regex" ]
	"warning_pattern": [
		[ "^[^\\r\\n]+?(?i)warning", "[\\r\\n]" ] // lines including 'warning' with ignore case
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