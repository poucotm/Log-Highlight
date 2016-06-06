## -----------------------------------------------------------------------------
## Author : yongchan jeon (Kris) poucotm@gmail.com
## File   : Verilog Gadget Log.py
## Create : 2016-06-06 19:41:37
## Editor : sublime text3, tab size (3)
## -----------------------------------------------------------------------------

import sublime, sublime_plugin
import re
import threading
import os

############################################################################
# for settings

ST3 = int(sublime.version()) >= 3000
MAX_SCAN_PATH     = 1000
MAX_STAIR_UP_PATH = 10

def plugin_loaded():
	global lh_settings
	lh_settings = sublime.load_settings('Log Highlight.sublime-settings')
	lh_settings.clear_on_change('reload')
	lh_settings.add_on_change('reload', plugin_loaded)

# def plugin_unloaded():
	# print ("unloaded : Verilog Gadget Log.py")

def get_settings():
	if ST3:
		return lh_settings
	else:
		return sublime.load_settings('Log Highlight.sublime-settings')

############################################################################
# LogHighlightGenCustomSyntaxThemeCommand

class LogHighlightGenCustomSyntaxThemeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.gen_syntax()
		self.gen_theme()
		return

	def gen_syntax(self):
		llh_settings  = get_settings()
		error_pattern = llh_settings.get('error_pattern')

		_tmlang = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>fileTypes</key>
	<array/>
	<key>name</key>
	<string>Log Highlight</string>
	<key>patterns</key>
	<array>"""
		for _str in error_pattern:
			_tmlang = _tmlang + """
		<dict>
			<key>begin</key>
			<string>""" + _str[0] + """</string>
			<key>end</key>
			<string>""" + _str[1] + """</string>
			<key>name</key>
			<string>msg.error</string>
			<key>patterns</key>
			<array>
				<dict>
					<key>include</key>
					<string>$self</string>
				</dict>
				<dict>
					<key>match</key>
					<string>\"?[\w\d\:\\/\.\-\=]+\.\w+[\w\d]*\"?[,:]\s*\d+</string>
					<key>name</key>
					<string>msg.error.link</string>
				</dict>
				<dict>
					<key>match</key>
					<string>(?&lt;=\')[^\']+(?=\')</string>
					<key>name</key>
					<string>msg.error.quote</string>
				</dict>
			</array>
		</dict>"""

		_tmlang = _tmlang + """
	</array>
	<key>scopeName</key>
	<string>source.loghighlight</string>
	<key>uuid</key>
	<string>0ed2482c-a94a-49dc-9aae-b1401bcff2e0</string>
</dict>
</plist>
"""
		_user_path   = os.path.join(sublime.packages_path(), 'User')
		if not os.path.exists(_user_path):
			os.makedirs(_user_path)
		_tmlang_path = os.path.join(_user_path, 'Log Highlight.tmLanguage')
		f = open(_tmlang_path, "w")
		f.write(_tmlang)
		f.close()
		return

	def gen_theme(self):
		llh_settings = get_settings()
		theme_color  = llh_settings.get('theme_color')

		if ST3:
			_tmtheme = sublime.load_resource('Packages/Log Highlight/Log Highlight.hidden-tmTheme')
		else:
			fname = os.path.join(sublime.packages_path(), 'Log Highlight/Log Highlight.hidden-tmTheme')
			f = open(fname, 'r')
			_tmtheme = str(f.read())
			f.close()

		for index, color_new in enumerate(theme_color):
			try:
				line_old  = re.compile('\<\!-- #' + str(index) + ' .+').findall(_tmtheme)[0]
				color_old = re.compile('#[\w\d]{6}').findall(line_old)[0]
				line_new  = re.sub(color_old, color_new, line_old)
				_tmtheme  = re.sub(line_old, line_new, _tmtheme)
			except:
				pass

		_user_path   = os.path.join(sublime.packages_path(), 'User')
		if not os.path.exists(_user_path):
			os.makedirs(_user_path)
		_tmtheme_path = os.path.join(_user_path, 'Log Highlight.hidden-tmTheme')
		f = open(_tmtheme_path, "w")
		f.write(_tmtheme)
		f.close()
		return

############################################################################
# LogHighlightCommand

class LogHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		if ST3:
			LogHighlightThread().start()
		else:
			LogHighlightThread().run()

class  LogHighlightThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		window    = sublime.active_window()
		self.view = window.active_view()
		log_name  = self.view.file_name()
		if not log_name or not os.path.isfile(log_name):
			sublime.status_message("Log Highlight : Unknown name for current view")
			return

		# set syntax for coloring / set read only
		self.set_syntax_theme(self.view)
		self.view.set_read_only(True)

		# to set base directory
		rel_path_file = self.get_rel_path_file()
		self.base_dir = ""
		if rel_path_file != "":
			self.search_base(log_name, rel_path_file)

		# set base dir & apply 'result_file_regex'
		if self.base_dir != "":
			self.view.settings().set('result_base_dir', self.base_dir)
		self.view.settings().set('result_file_regex', '\"?([\w\d\:\\/\.\-\=]+\.\w+[\w\d]*)\"?\s*[,:line]{1,4}\s*(\d+)')
		if ST3: # this is for ST3 bug related with 'result_file_regex' which I suspect
			self.view.run_command('revert')

		# add bookmarks
		self.add_bookmarks(self.view)

		# summary
		self.do_summary(self.view)

		return

	def set_syntax_theme(self, view):
		# usr_syntax = os.path.join(sublime.packages_path(), 'User/Log Highlight.tmLanguage')
		# print (usr_syntax)
		# view.set_syntax_file(usr_syntax)

		# usr_syntax = os.path.join(sublime.packages_path(), 'User/Log Highlight.tmLanguage')
		# if os.path.exists(usr_syntax):
		# 	view.set_syntax_file(usr_syntax)
		# else:
		# 	view.set_syntax_file('Packages/Log Highlight/Log Highlight.tmLanguage')

		usr_theme = os.path.join(sublime.packages_path(), 'User/Log Highlight.hidden-tmTheme')
		if os.path.exists(usr_theme):
			view.settings().set('color_scheme', usr_theme)
		else:
			view.settings().set('color_scheme', 'Packages/Log Highlight/Log Highlight.hidden-tmTheme')
		return

	def get_rel_path_file(self):
		text     = self.view.substr(sublime.Region(0, self.view.size()))
		files_l  = re.compile('\"?([\w\d\:\\/\.\-\=]+\.\w+[\w\d]*)\"?\s*[,:line]{1,4}\s*\d+').findall(text)
		rel_path = False
		if len(files_l) > 0:
			for file_name in files_l:
				if not os.path.isabs(file_name): # use the first in relative path list
					rel_path = True
					break
			if rel_path:
				return file_name
			else:
				sublime.status_message("Log Highlight : There is no relative path file")
				return ""
		else:
			sublime.status_message("Log Highlight : There is no openable file path")
			return ""

	def search_base(self, log_name, file_name):
		sublime.status_message("Log Highlight : Searching base directory ...")
		old_path  = ["", 0]
		_path     = os.path.dirname(os.path.dirname(log_name))
		_depth    = _path.count(os.path.sep)
		new_path  = [_path, _depth]
		scan_path = 0
		found     = False
		try:
			for i in range(MAX_STAIR_UP_PATH):
				for _dir in os.walk(new_path[0]):
					if i == 0 or not _dir[0].startswith(old_path[0]):
						sublime.status_message("Log Highlight : Searching - " + _dir[0])
						if os.path.isfile(os.path.join(_dir[0], file_name)):
							self.base_dir = _dir[0]
							found = True
							break
						else:
							scan_path = scan_path + 1
							if scan_path > MAX_SCAN_PATH - 1:
								break
				if found or scan_path > MAX_SCAN_PATH - 1:
					break
				else:
					# print ("Searching Uppder Directory")
					old_path = [new_path[0], new_path[0].count(os.path.sep)]
					_path    = os.path.dirname(old_path[0])
					_depth   = _path.count(os.path.sep)
					if old_path[1] == _depth or _depth < 1: # to stop level 1 (old_path[1] == _depth == 1)
						break
					else:
						new_path = [_path, _depth]
		except PermissionError:
			pass

		if found:
			sublime.status_message("Log Highlight : Found base directory (" + str(scan_path) + ") - " + self.base_dir)
		else:
			sublime.status_message("Log Highlight : Fail to find (" + str(scan_path) + ") - " + file_name)

		return found

	def add_bookmarks(self, view):
		err_head  = '^Error-\[.+|^Error:.+|^\*Error\*.+|^\w+:\s*\*E.+|^ERROR:.+|^Error\s*\(\d+\):.+'
		warn_head = '^Warning-\[.+|^Warning:.+|^\*Warning\*.+|^\w+:\s*\*E.+|^WARNING:.+|^Warning\s*\(\d+\):.+'
		filt_head = err_head + '|' + warn_head
		sublime.active_window().focus_view(view)
		regions   = view.find_all(filt_head)
		view.add_regions("bookmarks", regions, "bookmarks", "dot", sublime.HIDDEN | sublime.PERSISTENT)
		return

	def do_summary(self, view):
		lvg_settings = get_settings()
		log_panel    = lvg_settings.get("log_panel", True)
		error_only   = lvg_settings.get("error_only", False)
		if not log_panel:
			return

		err_msg   = '^Error-\[.+?^\s*\n|^Error:.+?(?=^[^\s]|\r?\n\r?\n)|^\*Error\*.+?^\s*\n|^\w+:\s*\*E[^\r\n]+|^ERROR:.[^\r\n]+|^Error\s*\(\d+\):[^\r\n]+'
		warn_msg  = '^Warning-\[.+?^\s*\n|^Warning:.+?(?=^[^\s]|\r?\n\r?\n)|^\*Warning\*.+?^\s*\n|^\w+:\s*\*W[^\r\n]+|^WARNING:.[^\r\n]+|^Warning\s*\(\d+\):[^\r\n]+'
		if error_only:
			filt_msg  = err_msg
			summary   = "\n" + "Error Summary (toggle : ctrl+f11 (default))\n" + "-" * 100 + "\n\n"
		else:
			filt_msg  = err_msg + '|' + warn_msg
			summary   = "\n" + "Error / Warning Summary (toggle : ctrl+f11 (default))\n" + "-" * 100 + "\n\n"

		sublime.active_window().focus_view(view)
		text      = view.substr(sublime.Region(0, view.size()))
		ewtext_l  = re.compile(filt_msg, re.MULTILINE|re.DOTALL).findall(text)
		for _str in ewtext_l:
			_str = re.sub(re.compile('\r?\n\r?\n'), '\n', _str)
			summary = summary + _str + ('\n\n' if _str[-1] != '\n' else '\n')

		global g_output_view
		g_output_view = view.window().get_output_panel('loghighlight')
		g_output_view.set_read_only(False)
		view.window().run_command("show_panel", {"panel": "output.errors"})
		g_output_view.settings().set('result_file_regex', '\"?([\w\d\:\\/\.\-\=]+\.\w+[\w\d]*)\"?\s*[,:line]{1,4}\s*(\d+)')
		if self.base_dir != "":
			g_output_view.settings().set('result_base_dir', self.base_dir)

		self.set_syntax_theme(self.view)

		g_output_view.set_syntax_file('Packages/Verilog Gadget/Verilog Gadget Log.tmLanguage')
		g_output_view.settings().set('color_scheme', 'Packages/Verilog Gadget/Verilog Gadget Log.hidden-tmTheme')
		g_output_view.run_command("append", {"characters": summary})
		g_output_view.set_read_only(True)
		# add bookmarks
		self.add_bookmarks(g_output_view)
		return

# ############################################################################
# # for context menu

# def log_check_visible(file_name, view_name):
# 	llh_settings = get_settings()
# 	if not llh_settings.get("context_menu", True):
# 		return False
# 	try:
# 		_name = file_name if view_name == "" else view_name
# 		ext   = os.path.splitext(_name)[1]
# 		ext   = ext.lower()
# 		if ext == ".log":
# 			return True
# 		else:
# 			return False
# 	except:
# 		return False

class LogHighlightPanelCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		try:
			if g_output_view:
				if bool(g_output_view.window()):
					self.view.window().run_command("hide_panel", {"panel": "output.loghighlight"})
				else:
					self.view.window().run_command("show_panel", {"panel": "output.loghighlight"})
		except:
			pass

# class LogHighlightCtxCommand(sublime_plugin.TextCommand):
# 	def run(self, edit):
# 		self.view.run_command('verilog_gadget_view_log')
# 	def is_visible(self):
# 		return log_check_visible(self.view.file_name(), self.view.name())

