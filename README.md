# Log Highlight for Sublime Text

[![Package Control](https://packagecontrol.herokuapp.com/downloads/Log%20Highlight.svg?style=flat-square)](https://packagecontrol.io/packages/Log%20Highlight)

Log Highlight helps to view a log (any type) with customizable error/warning syntax & color scheme & extensible severity levels.
Open `.log` file and run `Log Highlight` in the context menu or `Log Highlight : Highlight Error/Warning` in the command palette.

(Build Window)
![Image of Log Highlight](https://raw.githubusercontent.com/poucotm/Links/master/image/lh-build.png)

(Log File)
![Image of Log Highlight](https://raw.githubusercontent.com/poucotm/Links/master/image/lh-log.gif)

## Features
***********

 * Customizable Syntax & Color Scheme
 * Extensible Severity Levels
 * Add Bookmarks Automatically for Navigating Errors/Warnings with customizable icons
 * Support Go To Position in a Log by `result_file_regex`
 * Search a Base Directory Automatically for Relative Path Link
 * Summary Output Panel
 * Auto Refresh for Multiple Logs
 * Continuous Tracking for Multiple Logs
 * Enable Build Window (Output Panel)

#### Customizable Syntax & Color Scheme

After changing syntax and color scheme in **settings**, run `Log Hightlight: Generate Custom Syntax & Theme` command. You may have to restart sublime text once.

#### Extensible Severity Levels

You can add, remove, change severity levels like debug/notice/emergency in **settings**, run `Log Hightlight: Generate Custom Syntax & Theme` command. You may have to restart sublime text once.

#### Bookmarks

When errors/warnings found, it will add bookmarks for them for each icon.

#### Go To Position

By double-click, you can go to positions of links like `"../../abc.cpp", 32` or `./abc.v line 234` in a log. For relative path, it may automatically search a base directory near the log file

#### Summary Output Panel

By default, it summarizes error/warning list in a new output panel at the bottom of window. It is useful to debug without monitoring the log file directly. But do not close the log file, it is needed to get the event. (default keymap - toggle : alt+f12, hide : ESC)

#### More Flexible Style Syntax

You can highlight links and quotes inside "begin regex", "end regex" and "match regex" by using special words `{{{LINK}}}`, `{{{QUOTE}}}`. It can be used for the following gcc style error/warning message : `./src/abc.cpp:40:2 error: unknown escape seque ...`

#### Auto Refresh for Multiple Logs

When the log files are updated, it automatically refreshes the bookmarks, summary output panel. There's some inertial delays for smooth action.

#### Continuous Tracking for Multiple Logs

If there are open files which already log-highlighted when sublime text restart, it will track all again. (ST3 only)

#### Enable Build Window (Output Panel)

Log Highlight can be used for Build Window or Unsaved View. But relative path link won't be used because the absolute path is unknown. In order to use relative path, you should set like the following: `output_view.settings().set('filepath', [PATH])` output_view is the handle of your output panel view.

#### Restore Settings :

Just remove `Packages/User/Log Highlight.tmLanguage`, `Log Highlight.hidden-tmTheme`

#### Pattern Regular Expression in Settings :

usage :  `[ "begin regex", "end regex" ] or [ "match regex", "" ]`

example)
```java
Error-[SE] Syntax error :
   ./src/macros/uvm_object_defines.svh line: 764: token is 'for'
--> [ "^Error-\\[", "^\\s*[\\n]" ], // Error-[ ~ next empty line (multi-line)

error ../src/foo.cpp:40
--> [ "^(?i)error", "[\\r\\n]" ]

../src/foo.cpp:40 error:
--> [ "^{{{LINK}}}?[^\\r\\n]*?(?i)error", "[\\r\\n]" ]
```

#### Settings :

```java
{
   // enable context menu
   "context_menu": true,

   // log file extension
   "log_ext": [ ".log" ], // use ".*" for all file extensions

   // search base directory automatically for relative path
   "search_base": true,

   // severity level
   "severity" : {

      // error __________________________________________________
      "error" : {
         "enable"  : true,
         "summary" : true,
         "pattern" : [
            // [ "begin regex", "end regex" ] or [ "match regex", "" ]
            [ "^Error-\\[", "^\\s*[\\n]" ],                      // Error-[ ~ next empty line (multi-line)
            [ "^{{{LINK}}}?[^\\r\\n]*?(?i)error", "[\\r\\n]" ],  // a line including case-insensitive 'error' with or without a link in front of 'error'
            [ "^\\w+:\\s*\\*E", "[\\r\\n]" ]                     // ...: *E ... (single line)
            // <-- Remove, Change, Add More Patterns Here -->
         ],
         "color" : {
            "base"  : "#F92672", // error message
            "link"  : "#E6DB74", // link in error message
            "quote" : "#4F99D3"  // quote in error message
         },
         "icon"  : "error.png"   // remove "icon" not to use icon, "dot", "circle" "bookmark" are possible
      },

      // warning ________________________________________________
      "warning" : {
         "enable"  : true,
         "summary" : true,
         "pattern" : [
            // [ "begin regex", "end regex" ] or [ "match regex", "" ]
            [ "^Warning-\\[", "^\\s*[\\n]" ],                    // Warning-[ ~ next empty line (multi-line)
            [ "^{{{LINK}}}?[^\\r\\n]*?(?i)warning", "[\\r\\n]" ],// a line including case-insensitive 'warning' with or without a link in front of 'warning'
            [ "^\\w+:\\s*\\*W", "[\\r\\n]" ]                     // ...: *W ... (single line)
            // <-- Remove, Change, Add More Patterns Here -->
         ],
         "color" : {
            "base"  : "#A1B347", // warning message
            "link"  : "#FD971F", // link in warning message
            "quote" : "#4F99D3"  // quote in warning message
         },
         "icon"  : "warning.png" // remove "icon" not to use icon, "dot", "circle" "bookmark" are possible
      },

      // info ___________________________________________________
      "info" : {
         "enable"  : false,
         "summary" : false,
         "pattern" : [
            // [ "begin regex", "end regex" ] or [ "match regex", "" ]
            [ "^Information-\\[", "^\\s*[\\n]" ],                // Information-[ ~ next empty line (multi-line)
            [ "^\\[INFO\\]", "[\\r\\n]" ]                        // [INFO] ... (single line)
            // <-- Remove, Change, Add More Patterns Here -->
         ],
         "color" : {
            "base"  : "#70991f", // info message
            "link"  : "#b36915", // link in info message
            "quote" : "#428a99"  // quote in info message
         },
         "icon"  : "info.png"    // remove "icon" not to use icon, "dot", "circle" "bookmark" are possible
      }

      // <-- Remove, Change, Add More Severity Level Here -->
   },

   // theme color set
   "theme_color": {
      "background"      : "#13181F",
      "foreground"      : "#D7D7D7",
      "caret"           : "#F29718",
      "selection"       : "#3A5166",
      "selectionBorder" : "#181E26",
      "lineHighlight"   : "#283240",
      "summary_title"   : "#D7D7D7"
   },

   // summary panel
   "summary_panel": true,         // show summary panel

   // bookmark
   "bookmark_enable": true,       // enable/disable bookmarks
   "bookmark_goto_error": true    // automatically go to 1st error line
}
```

## issues

When you have an issue, tell me through [https://github.com/poucotm/Log-Highlight/issues](https://github.com/poucotm/Log-Highlight/issues), or send me an e-mail poucotm@gmail.com, yongchan.jeon@samsung.com