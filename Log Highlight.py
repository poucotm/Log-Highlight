# -*- coding: utf8 -*-

## -----------------------------------------------------------------------------
## Author : yongchan jeon (Kris) poucotm@gmail.com
## File   : Log Highlight.py
## Create : 2016-06-06 19:41:37
## Editor : sublime text3, tab size (3)
## -----------------------------------------------------------------------------

import sublime, sublime_plugin
import re
import threading, time
import os

############################################################################
# for settings

ST3 = int(sublime.version()) >= 3000
MAX_SCAN_PATH     = 1000
MAX_STAIR_UP_PATH = 10
REFRESH_WAIT      = 500 # 0.5s

def plugin_loaded():
	global lh_settings
	lh_settings = sublime.load_settings('Log Highlight.sublime-settings')
	# lh_settings.clear_on_change('reload')
	# lh_settings.add_on_change('reload', plugin_loaded)
	view_l = sublime.active_window().views()
	global logh_view
	for v in view_l:
		if v.settings().get('syntax').endswith('Log Highlight.tmLanguage'):
			logh_view.append([v.id(), 0])
		if v.settings().get('logh_lastv') == True:
			global logh_lastv
			logh_lastv = v.id()

# def plugin_unloaded():
	# print ("unloaded : Log Highlight.py")

def get_settings():
	if ST3:
		return lh_settings
	else:
		return sublime.load_settings('Log Highlight.sublime-settings')

############################################################################
# LogHighlightGenCustomSyntaxThemeCommand

LINK_REGX_PLIST    = r"""["']?[\w\d\:\\\/\.\-\=]+\.\w+[\w\d]*["']?\s*[,:line\(]{1,5}\s*\d+\)?"""
LINK_REGX_SETTING  = r"""(["']?[\w\d\:\\/\.\-\=]+\.\w+[\w\d]*["']?\s*[,:line\(]{1,5}\s*\d+\)?)"""
LINK_REGX_RESULT   = r"""["']?([\w\d\:\\/\.\-\=]+\.\w+[\w\d]*)["']?\s*[,:line\(]{1,5}\s*(\d+)\)?"""
LINK_REGX_RELPATH  = r"""["']?([\w\d\:\\/\.\-\=]+\.\w+[\w\d]*)["']?\s*[,:line\(]{1,5}\s*\d+\)?"""
LINK_REGX_SUMMARY  = r"""(?:["']?[\w\d\:\\/\.\-\=]+\.\w+[\w\d]*["']?\s*[,:line\(]{1,5}\s*\d+\)?)"""

QUOTE_REGX_PLIST   = r"""(["'])(?:(?=(\\?))\2.)*?\1"""
QUOTE_REGX_SETTING = r"""(["'].+?["'])"""
QUOTE_REGX_SUMMARY = r"""(?:["'].+?["'])"""

class LogHighlightGenCustomSyntaxThemeCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		self.gen_syntax()
		self.gen_theme()
		sublime.status_message("Log Highlight : Custom syntax & theme files are generated")
		return

	def gen_syntax(self):

		_tmlang = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
	<key>fileTypes</key>
	<array/>
	<key>name</key>
	<string>Log Highlight</string>
	<key>patterns</key>
	<array>
		<dict>
			<key>begin</key>
			<string>Log Highlight</string>
			<key>comment</key>
			<string>...</string>
			<key>end</key>
			<string>[\\r\\n]</string>
			<key>name</key>
			<string>summary.title</string>
		</dict>"""
		# error
		_tmlang = _tmlang + self.gen_syntax_sub_pattern(0)
		# warning
		_tmlang = _tmlang + self.gen_syntax_sub_pattern(1)
		_tmlang = _tmlang + """
	</array>
	<key>repository</key>
	<dict>
		<key>error_link</key>
		<dict>
			<key>match</key>
			<string>""" + LINK_REGX_PLIST + """</string>
			<key>name</key>
			<string>msg.error.link</string>
		</dict>
		<key>error_quote</key>
		<dict>
			<key>match</key>
			<string>""" + QUOTE_REGX_PLIST + """</string>
			<key>name</key>
			<string>msg.error.quote</string>
		</dict>
		<key>warning_link</key>
		<dict>
			<key>match</key>
			<string>""" + LINK_REGX_PLIST + """</string>
			<key>name</key>
			<string>msg.warning.link</string>
		</dict>
		<key>warning_quote</key>
		<dict>
			<key>match</key>
			<string>""" + QUOTE_REGX_PLIST + """</string>
			<key>name</key>
			<string>msg.warning.quote</string>
		</dict>
	</dict>
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

	def gen_syntax_sub_pattern(self, sel):
		llh_settings    = get_settings()
		if sel == 0:
			pattern = llh_settings.get('error_pattern')
			word    = "error"
		else:
			pattern = llh_settings.get('warning_pattern')
			word    = "warning"

		pattern_tmlang = ""
		for _str in pattern:
			_str[0] = self.conv_for_plist(_str[0])
			_str[1] = self.conv_for_plist(_str[1])
			if _str[1] != "":
				pattern_tmlang = pattern_tmlang + """
		<dict>
			<key>begin</key>
			<string>""" + self.conv_for_regx(_str[0]) + """</string>""" + self.gen_syntax_sub_capture(_str[0], sel, 0) + """
			<key>end</key>
			<string>""" + self.conv_for_regx(_str[1]) + """</string>""" + self.gen_syntax_sub_capture(_str[1], sel, 1)
			else:
				pattern_tmlang = pattern_tmlang + """
		<dict>
			<key>match</key>
			<string>""" + self.conv_for_regx(_str[0]) + """</string>""" + self.gen_syntax_sub_capture(_str[0], sel, 2)
			pattern_tmlang = pattern_tmlang + """
			<key>name</key>
			<string>msg.""" + word + """</string>
			<key>patterns</key>
			<array>
				<dict>
					<key>include</key>
					<string>#""" + word + """_link</string>
				</dict>
				<dict>
					<key>include</key>
					<string>#""" + word + """_quote</string>
				</dict>
			</array>
		</dict>"""
		return pattern_tmlang

	def gen_syntax_sub_capture(self, regx, sel0, sel1):
		spw  = re.compile(r'\{\{\{LINK\}\}\}|\{\{\{QUOTE\}\}\}').findall(regx)
		if len(spw) == 0:
			return ""

		word = "error" if sel0 == 0 else "warning"
		if sel1 == 0:
			ret = """
			<key>beginCaptures</key>
			<dict>"""
		elif sel1 == 1:
			ret = """
			<key>endCaptures</key>
			<dict>"""
		else:
			ret = """
			<key>captures</key>
			<dict>"""
		lqs = ""
		for i, _str in enumerate(spw):
			if _str == r'{{{LINK}}}':
				lqs = "link"
			elif _str == r'{{{QUOTE}}}':
				lqs = "quote"
			ret = ret + """
				<key>""" + str(i+1) + """</key>
				<dict>
					<key>name</key>
					<string>msg.""" + word + """.""" + lqs + """</string>
				</dict>"""
		ret = ret + """
			</dict>"""
		return ret

	def conv_for_plist(self, _str):
		_str = re.sub('\<', '&lt;', _str)
		_str = re.sub('\>', '&gt;', _str)
		return _str

	def conv_for_regx(self, _str):
		_str = re.sub(r'\{\{\{LINK\}\}\}', LINK_REGX_SETTING, _str)
		_str = re.sub(r'\{\{\{QUOTE\}\}\}', QUOTE_REGX_SETTING, _str)
		return _str

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

is_working  = False
is_waiting  = False
req_refresh = []
logh_view   = []
logh_lastv  = -1

class LogHighlightCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global is_working
		if is_working:
			return
		lh_thread = LogHighlightThread(self.view, True)
		if ST3:
			lh_thread.start()
		else:
			lh_thread.run()

	# for context menu

	def is_visible(self):
		return self.log_check_visible(self.view.file_name(), self.view.name())

	def log_check_visible(self, file_name, view_name):
		llh_settings = get_settings()
		if not llh_settings.get("context_menu", True):
			return False
		try:
			_name = file_name if view_name == "" else view_name
			ext   = os.path.splitext(_name)[1]
			ext   = ext.lower()
			ext_l = llh_settings.get("log_ext") # [".log"]

			if any(".*" == s for s in ext_l):
				return True

			if any(ext == s for s in ext_l):
				return True
			else:
				return False
		except:
			return False

class LogHighlightEvent(sublime_plugin.EventListener):

	# for ST2
	def on_modified(self, view):
		if ST3:
			return
		global logh_view
		for i, vid in enumerate(logh_view):
			if view.id() == vid[0] or view.is_loading():
				logh_view[i][1] = logh_view[i][1] + 1
				global is_waiting
				if not is_waiting:
					thread = LogHighlightRefreshThread(view)
					thread.run()
				break

	# for ST3
	def on_modified_async(self, view):
		global logh_view
		for i, vid in enumerate(logh_view):
			if view.id() == vid[0] or view.is_loading():
				logh_view[i][1] = logh_view[i][1] + 1
				global is_waiting
				if not is_waiting:
					thread = LogHighlightRefreshThread(view)
					thread.start()
				break
		return

	def on_close(self, view):
		for vid in logh_view:
			if view.id() == vid[0]:
				logh_view.remove(vid);
			break
		global logh_lastv
		if view.id() == logh_lastv:
			if len(logh_view) > 0:
				logh_lastv = logh_view[-1]
			else:
				logh_lastv = -1
		return

class LogHighlightRefreshThread(threading.Thread):
	def __init__(self, view):
		threading.Thread.__init__(self)
		self.view = view

	def run(self):
		global is_waiting
		is_waiting = True
		global logh_view
		for vid in logh_view:
			if self.view.id() == vid[0]:
				self.last_req = vid[1]
				sublime.set_timeout(self.refresh_wait, REFRESH_WAIT) # milliseconds
				break
		return

	def refresh_wait(self):
		global logh_view
		for i, vid in enumerate(logh_view):
			if self.view.id() == vid[0]:
				if self.last_req != vid[1]: # more requests are comming
					self.last_req = vid[1]
					sublime.set_timeout(self.refresh_wait, REFRESH_WAIT) # milliseconds
				else:
					global is_working
					if is_working or self.view.is_loading():
						logh_view[i][1] = logh_view[i][1] + 1
						sublime.set_timeout(self.refresh_wait, REFRESH_WAIT) # milliseconds
						break
					else:
						lh_thread = LogHighlightThread(self.view, False)
						if ST3:
							lh_thread.start()
						else:
							lh_thread.run()
						global is_waiting
						is_waiting = False
				break
		return

class LogHighlightThread(threading.Thread):
	def __init__(self, view, is_first):
		threading.Thread.__init__(self)
		self.view     = view;
		self.is_first = is_first;

	def run(self):
		global is_working
		is_working = True
		log_name   = self.view.file_name()
		# to support unsaved file (like Tail)
		if not log_name:
			log_name   = self.view.settings().get('filepath')
		if not log_name or not os.path.isfile(log_name):
			sublime.status_message("Log Highlight : Unknown name for current view")
			is_working = False
			return

		self.base_dir = ""
		self.try_search_base = False

		if self.is_first:
			global logh_view
			if not any(self.view.id() == vid[0] for vid in logh_view):
				logh_view.append([self.view.id(), 0])

			view_l = sublime.active_window().views()
			for v in view_l:
				if v.settings().get('syntax').endswith('Log Highlight.tmLanguage'):
					v.settings().set('logh_lastv', False)

			global logh_lastv
			logh_lastv = self.view.id()
			self.view.settings().set('logh_lastv', True)

			# set syntax for coloring / set read only
			self.set_syntax_theme(self.view)
			# self.view.set_read_only(True) # cannot call on_modified
			self.view.settings().set("always_prompt_for_file_reload", False)
		else:
			get_base_dir = self.view.settings().get('result_base_dir')
			if get_base_dir == None or get_base_dir == "":
				self.try_search_base = True
				self.search_base(log_name)
				if self.base_dir != "":
					self.view.settings().set('result_base_dir', self.base_dir)
			else:
				self.base_dir = get_base_dir
			self.do_next()
			is_working = False
			return

		# to set base directory
		self.try_search_base = True
		self.search_base(log_name)

		# set base dir & apply 'result_file_regex'
		if self.base_dir != "":
			self.view.settings().set('result_base_dir', self.base_dir)
		self.view.settings().set('result_file_regex', LINK_REGX_RESULT)
		if ST3: # this is for ST3 bug related with 'result_file_regex' which I suspect
			self.view.run_command('revert')
			self.timeout = 0
			sublime.status_message("Log Highlight : Waiting for loading ...")
			self.wait_for_loading()
		else:
			self.do_next()

		is_working = False
		return

	def wait_for_loading(self):
		if self.view.is_loading():
			self.timeout = self.timeout + 1
			if self.timeout > 200:
				sublime.status_message("Log Highlight : Timed out waiting for loading")
				is_working = False
				return
			sublime.set_timeout(self.wait_for_loading, 50)
		else:
			self.do_next()

		is_working = False
		return

	def do_next(self):
		# add bookmarks
		self.goto_line = None
		self.add_bookmarks(self.view, 0)

		llh_settings = get_settings()
		last_only    = llh_settings.get('summary_update_for_last_log', False)

		# summary
		if last_only:
			if logh_lastv == self.view.id():
				self.do_summary(self.view)
		else:
			self.do_summary(self.view)

		# update status message
		if self.try_search_base:
			if self.search_base_success:
				sublime.status_message("Log Highlight : Found Base Directory - " + self.base_dir)
			else:
				sublime.status_message("Log Highlight : Unable to Find Base Directory !")

		sublime.set_timeout(self.go_to_line, 50)
		return

	def go_to_line(self):
		llh_settings = get_settings()
		goto_error   = llh_settings.get('bookmark_goto_error', True)
		# go to 1st error line
		if goto_error and self.goto_line != None:
			self.view.show(self.goto_line)

	def set_syntax_theme(self, view):
		usr_syntax = os.path.join(sublime.packages_path(), 'User/Log Highlight.tmLanguage')
		if os.path.exists(usr_syntax):
			view.set_syntax_file('Packages/User/Log Highlight.tmLanguage')
		else:
			view.set_syntax_file('Packages/Log Highlight/Log Highlight.tmLanguage')

		usr_theme = os.path.join(sublime.packages_path(), 'User/Log Highlight.hidden-tmTheme')
		if os.path.exists(usr_theme):
			view.settings().set('color_scheme', 'Packages/User/Log Highlight.hidden-tmTheme')
		else:
			view.settings().set('color_scheme', 'Packages/Log Highlight/Log Highlight.hidden-tmTheme')
		return

	def get_rel_path_file(self):
		# to support unsaved file (like Tail)
		logn = self.view.file_name()
		if logn:
			text = self.view.substr(sublime.Region(0, self.view.size()))
		else:
			logn = self.view.settings().get('filepath')
			f = open(logn, 'r')
			text = str(f.read())
			f.close()
		files_l  = re.compile(LINK_REGX_RELPATH).findall(text)
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

	def search_base(self, log_name):
		file_name = self.get_rel_path_file()
		self.search_base_success = True
		self.base_dir = ""
		if file_name == "":
			return

		sublime.status_message("Log Highlight : Searching base directory ...")
		old_path  = ["", 0]
		_path     = os.path.dirname(log_name)
		_depth    = _path.count(os.path.sep)
		new_path  = [_path, _depth]
		scan_path = 0
		found     = False
		try:
			for i in range(MAX_STAIR_UP_PATH):
				for _dir in os.walk(new_path[0]):
					if i == 0 or not _dir[0].startswith(old_path[0]):
						sublime.status_message("Log Highlight : Searching - " + _dir[0])
						# print (_dir[0])
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

		self.search_base_success = found
		return

	def add_bookmarks(self, view, sel):
		llh_settings    = get_settings()
		error_pattern   = llh_settings.get('error_pattern')
		warning_pattern = llh_settings.get('warning_pattern')
		bmark_error_only= llh_settings.get('bookmark_error_only', False)

		err_head = ""
		for i, _pat in enumerate(error_pattern):
			_pat[0]  = self.conv_for_regx(_pat[0])
			if i == len(error_pattern) - 1:
				err_head = err_head + _pat[0] + '.*'
			else:
				err_head = err_head + _pat[0] + '.*|'
		warn_head = ""
		for i, _pat in enumerate(warning_pattern):
			_pat[0]  = self.conv_for_regx(_pat[0])
			if i == len(warning_pattern) - 1:
				warn_head = warn_head + _pat[0] + '.*'
			else:
				warn_head = warn_head + _pat[0] + '.*|'

		regions = []
		region_err  = view.find_all(err_head)
		region_warn = view.find_all(warn_head)
		regions.extend(region_err)
		if not bmark_error_only:
			regions.extend(region_warn)

		if sel == 1 and len(regions) > 0: # except for summary title
			for i, _reg in enumerate(regions):
				if view.rowcol(_reg.begin()) == (1,0):
					del regions[i]

		if sel == 0 and len(region_err) > 0: # 1st error line
			self.goto_line = region_err[0]

		if sel == 0:
			if ST3:
				view.add_regions("bookmarks", regions, "bookmarks", "Packages/Log Highlight/icons/apple.png", sublime.HIDDEN | sublime.PERSISTENT)
			else:
				view.add_regions("bookmarks", regions, "bookmarks", "dot", sublime.HIDDEN | sublime.PERSISTENT)
		else:
			view.add_regions("bookmarks", regions, "bookmarks", "", sublime.HIDDEN | sublime.PERSISTENT)

		# # of errors / # of warnings
		if sel == 0:
			self.n_errors = str(len(region_err));
			self.n_warns  = str(len(region_warn));

		return

	def do_summary(self, view):
		llh_settings    = get_settings()
		summary_panel   = llh_settings.get("summary_panel", True)
		error_only      = llh_settings.get("summary_error_only", False)
		if not summary_panel:
			return

		error_pattern   = llh_settings.get('error_pattern')
		warning_pattern = llh_settings.get('warning_pattern')
		show_log_name   = llh_settings.get("summary_show_log_name", True)

		err_msg = ""
		for i, _pat in enumerate(error_pattern):
			_pat[0]  = self.conv_for_regx(_pat[0])
			_pat[1]  = self.conv_for_regx(_pat[1])
			if i == len(error_pattern) - 1:
				err_msg = err_msg + _pat[0] + '.*?' + _pat[1]
			else:
				err_msg = err_msg + _pat[0] + '.*?' + _pat[1] + '|'
		warn_msg = ""
		for i, _pat in enumerate(warning_pattern):
			_pat[0]  = self.conv_for_regx(_pat[0])
			_pat[1]  = self.conv_for_regx(_pat[1])
			if i == len(warning_pattern) - 1:
				warn_msg = warn_msg + _pat[0] + '.*?' + _pat[1]
			else:
				warn_msg = warn_msg + _pat[0] + '.*?' + _pat[1] + '|'

		log_name = view.file_name()
		if log_name:
			log_name = os.path.split(view.file_name())[1];
		else:
			log_name = view.name()

		if error_only:
			filt_msg  = err_msg
			if show_log_name:
				summary   = "\n" + "Log Highlight Summary ( " + str(self.n_errors) + " ) errors   ( " + log_name + " )\n" + "-" * 100 + "\n"
			else:
				summary   = "\n" + "Log Highlight Summary ( " + str(self.n_errors) + " ) errors\n" + "-" * 100 + "\n"
		else:
			filt_msg  = err_msg + '|' + warn_msg
			if show_log_name:
				summary   = "\n" + "Log Highlight Summary ( " + str(self.n_errors) + " ) errors, ( " + str(self.n_warns) + " ) warnings   ( " + log_name + " )\n" + "-" * 100 + "\n"
			else:
				summary   = "\n" + "Log Highlight Summary ( " + str(self.n_errors) + " ) errors, ( " + str(self.n_warns) + " ) warnings\n" + "-" * 100 + "\n"

		text      = view.substr(sublime.Region(0, view.size()))
		text      = text + '\n' # workaround when there is no '\n' at last
		ewtext_l  = re.compile(filt_msg, re.MULTILINE|re.DOTALL).findall(text)

		for _str in ewtext_l:
			_str    = re.sub(re.compile(r'[\r\n]+$'), '', _str);
			summary = summary + _str + '\n\n'

		global g_summary_view
		g_summary_view = view.window().get_output_panel('loghighlight')
		g_summary_view.settings().set('gutter', True);
		g_summary_view.settings().set('line_numbers', False);
		g_summary_view.set_read_only(False)
		view.window().run_command("show_panel", {"panel": "output.loghighlight"})
		g_summary_view.settings().set('result_file_regex', LINK_REGX_RESULT)
		if self.base_dir != "":
			g_summary_view.settings().set('result_base_dir', self.base_dir)
		self.set_syntax_theme(g_summary_view)
		if ST3:
			g_summary_view.run_command("append", {"characters": summary})
		else:
			edit = g_summary_view.begin_edit()
			g_summary_view.erase(edit, sublime.Region(0, g_summary_view.size()))
			g_summary_view.insert(edit, g_summary_view.size(), summary)
			g_summary_view.end_edit(edit)
		g_summary_view.set_read_only(True)

		# add bookmarks
		self.add_bookmarks(g_summary_view, 1)
		return

	def conv_for_regx(self, _str):
		_str = re.sub(r'\{\{\{LINK\}\}\}', LINK_REGX_SUMMARY, _str)
		_str = re.sub(r'\{\{\{QUOTE\}\}\}', QUOTE_REGX_SUMMARY, _str)
		return _str

class LogHighlightPanelCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		try:
			if g_summary_view:
				if bool(g_summary_view.window()):
					self.view.window().run_command("hide_panel", {"panel": "output.loghighlight"})
				else:
					self.view.window().run_command("show_panel", {"panel": "output.loghighlight"})
		except:
			pass

