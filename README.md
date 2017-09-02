# Log Highlight for Sublime Text

[![Package Control](https://packagecontrol.herokuapp.com/downloads/Log%20Highlight.svg?style=round-square)](https://packagecontrol.io/packages/Log%20Highlight)

Log Highlight helps to view a log (any type) with customizable error/warning syntax & color scheme & extensible severity levels.
Open a log file (like .log) and run __*Log Highlight*__ in the context menu or __*Log Highlight : Highlight Error/Warning*__ in the command palette.

(Log File - auto-highlight off)  
![Image of Log Highlight](https://raw.githubusercontent.com/poucotm/Links/master/image/Log-Highlight/lh-log.gif)

(Build Window - auto-highlight on)  
![Image of Log Highlight](https://raw.githubusercontent.com/poucotm/Links/master/image/Log-Highlight/lh-build.gif)

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

__Customizable Syntax & Color Scheme__

After changing syntax and color scheme in __*Log Highlight.sublime-settings*__, run __*Log Hightlight: Generate Custom Syntax & Theme*__ command. You may have to restart sublime text once.

__Extensible Severity Levels__

You can add, remove, change severity levels like debug/notice/emergency in __*Log Highlight.sublime-settings*__, run __*Log Hightlight: Generate Custom Syntax & Theme*__ command. You may have to restart sublime text once.

__Bookmarks__

When errors/warnings found, it will add bookmarks for them for each icon.

__Go To Position__

By double-click, you can go to positions of links like `"../../abc.cpp", 32` or `./abc.v line 234` in a log. For relative path, it may automatically search a base directory near the log file

__Summary Output Panel__

By default, it summarizes error/warning list in a new output panel at the bottom of window. It is useful to debug without monitoring the log file directly. But do not close the log file, it is needed to get the event. (default keymap - toggle : alt+f12, hide : ESC)

__More Flexible Style Syntax__

You can highlight links and quotes inside "begin regex", "end regex" and "match regex" by using special words `{{{LINK}}}`, `{{{QUOTE}}}`. It can be used for the following gcc style error/warning message : `./src/abc.cpp:40:2 error: unknown escape seque ...`

__Auto Refresh for Multiple Logs__

When the log files are updated, it automatically refreshes the bookmarks, summary output panel. There's some inertial delays for smooth action.

__Continuous Tracking for Multiple Logs__

If there are open files which already log-highlighted when sublime text restart, it will track all again. (ST3 only)

__Enable Build Window (Output Panel)__

Log Highlight can be used for Build Window or Unsaved View. But relative path link won't be used because the absolute path is unknown. In order to use relative path, you should set like the following: `output_view.settings().set('filepath', [PATH])` output_view is the handle of your output panel view.

### Settings

Please, refer to [__Log Highlight.sublime-settings__](https://github.com/poucotm/Log-Highlight/blob/master/Log%20Highlight.sublime-settings), Usable Icons : [__Icon List__](https://github.com/poucotm/Log-Highlight/tree/master/icons)

__Regular Expression Pattern in Settings__

__Usage__   : `[ "begin regex", "end regex" ] or [ "match regex", "" ]`  
__Caution__ : avoid OR '|' and separate them, it can make an unexpected result.

example)
```java
Error-[SE] Syntax error :
   ./src/macros/uvm_object_defines.svh line: 764: token is 'for'
--> [ "^Error-\\[", "^\\s*[\\n]" ] // Error-[ ~ next empty line (multi-line)

error ../src/foo.cpp:40
--> [ "^(?i)error", "[\\r\\n]" ] // single line

../src/foo.cpp:40 error:
--> [ "^{{{LINK}}}?[^\\r\\n]*?(?i)error", "[\\r\\n]" ] // single line
```

__Restore Settings__

Use __*Log Hightlight: Erase Custom Syntax & Theme*__ in the command palette Or  
Just remove __*Packages/User/Log Highlight.tmLanguage*__, __*Log Highlight.hidden-tmTheme*__

### Donate

[![Doate Image](https://raw.githubusercontent.com/poucotm/Links/master/image/PayPal/donate-paypal.png)](https://www.paypal.com/cgi-bin/webscr?cmd=_s-xclick&hosted_button_id=89YVNDSC7DZHQ "PayPal")  
Thank you for donating. It is helpful to continue to improve the plug-in.

### Issues

When you have an issue, tell me through [https://github.com/poucotm/Log-Highlight/issues](https://github.com/poucotm/Log-Highlight/issues), or send me an e-mail poucotm@gmail.com
