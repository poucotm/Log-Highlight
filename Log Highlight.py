# -*- coding: utf8 -*-
# -----------------------------------------------------------------------------
# Author : yongchan jeon (Kris) poucotm@gmail.com
# File   : Log Highlight.py
# Create : 2017-09-02 09:05:28
# Editor : sublime text3, tab size (4)
# -----------------------------------------------------------------------------

import sublime
import sublime_plugin
import re
import threading
import os
import traceback


##  import Guna  ______________________________________________

try:
    from Guna.core.api import GunaApi
    guna_installed = True
except Exception:
    guna_installed = False


##  global constants / variables  _____________________________

# Sublime text version
ST3 = int(sublime.version()) >= 3000

# Relative path searching
MAX_SCAN_PATH     = 1000
MAX_STAIR_UP_PATH = 10

# Refresh delay
REFRESH_WAIT = 500  # 0.5s

# Extended severity list
severity_list = []


##  global functions  _________________________________________

def plugin_loaded():
    """ plugin_loaded """

    # from default/user settings
    get_severity_list()

    # register callback
    lhs = get_prefs()
    lhs.clear_on_change('lh-prefs')
    lhs.add_on_change('lh-prefs', plugin_loaded)

    # check all log-highlited views
    wins_l = sublime.windows()
    global logh_view
    for w in wins_l:
        view_l = w.views()
        for v in view_l:
            if check_syntax(v):
                logh_view.append([v.id(), 0])
            if v.settings().get('logh_lastv') is True:
                global logh_lastv
                logh_lastv = v.id()


def get_prefs():
    return sublime.load_settings('Log Highlight.sublime-settings')


def get_severity_list():
    """ Getting severity list from settings """

    lhs = get_prefs()
    svt = lhs.get('severity')
    global severity_list
    severity_list = []
    for i, k in enumerate(list(svt.keys())):
        if (svt.get(k)).get('enable', False):
            severity_list.append(k)


def check_syntax(view):
    syn = view.settings().get('syntax', '')
    if isinstance(syn, str):
        if syn.endswith('Log Highlight.tmLanguage'):
            return True
        else:
            return False
    else:
        return False


def is_compile_type():
    ltype = get_prefs().get('log_type', 'compile')
    if isinstance(ltype, str) and ltype.lower() == 'system':
        return False
    else:
        return True


def set_syntax_theme(view):
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


def fwrite(fname, text):
    try:
        if ST3:
            with open(fname, "w", newline="") as f:
                f.write(text)
        else:
            f = open(fname, "w")
            f.write(text)
            f.close()
    except Exception:
        disp_exept()


def fread(fname):
    text = ""
    try:
        if ST3:
            with open(fname, "r") as f:
                text = str(f.read())
        else:
            f = open(fname, "r")
            f.write(text)
            f.close()
    except Exception:
        disp_exept()
        return text


def disp_msg(msg):
    if guna_installed:
        GunaApi.alert_message(2, ' Log Highlight : ' + msg, 5, 0)
    else:
        sublime.status_message(' Log Highlight : ' + msg)


def disp_error(msg):
    if guna_installed:
        GunaApi.alert_message(3, ' Log Highlight : ' + msg, 10, 1)
    else:
        sublime.status_message(' Log Highlight : ' + msg)


def disp_exept():
    print ('LOG HIGHLIGHT : ERROR _______________________________________')
    traceback.print_exc()
    print ('=============================================================')
    disp_error("Error is occured. Please, see the trace-back information in Python console.")


##  class LogHighlightGenCustomSyntaxThemeCommand  ____________

# Regular expresson constants

LINK_REGX_PLIST    = r"""["']?[\w\d\:\\\/\.\-\=]+\.\w+[\w\d]*["']?\s*[,:line\(]{1,5}\s*\d+\)?"""
LINK_REGX_SETTING  = r"""(["']?[\w\d\:\\\/\.\-\=]+\.\w+[\w\d]*["']?\s*[,:line\(]{1,5}\s*\d+\)?)"""
LINK_REGX_RESULT   = r"""["']?([\w\d\:\\\/\.\-\=]+\.\w+[\w\d]*)["']?\s*[,:line\(]{1,5}\s*(\d+)\)?"""
LINK_REGX_RELPATH  = r"""["']?([\w\d\:\\\/\.\-\=]+\.\w+[\w\d]*)["']?\s*[,:line\(]{1,5}\s*\d+\)?"""
LINK_REGX_SUMMARY  = r"""(?:["']?[\w\d\:\\\/\.\-\=]+\.\w+[\w\d]*["']?\s*[,:line\(]{1,5}\s*\d+\)?)"""

QUOTE_REGX_PLIST   = r"""(["'])(?:(?=(\\?))\2.)*?\1"""
QUOTE_REGX_SETTING = r"""(["'].+?["'])"""
QUOTE_REGX_SUMMARY = r"""(?:["'].+?["'])"""


class LogHighlightGenCustomSyntaxThemeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        self.gen_syntax()
        self.gen_theme()

        disp_msg("Custom syntax & theme files are generated")

    def gen_syntax(self):
        """
        generate custom syntax file : Log Highlight.tmLanguage
        """

        sub_pattern     = ""
        sub_link_quote  = ""
        global severity_list
        for i, k in enumerate(severity_list):
            sub_pattern     += self.gen_syntax_sub_pattern(k)
            sub_link_quote  += self.gen_syntax_sub_link_quote(k)

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
        _tmlang = _tmlang + sub_pattern
        _tmlang = _tmlang + """
    </array>
    <key>repository</key>
    <dict>"""
        _tmlang = _tmlang + sub_link_quote
        _tmlang = _tmlang + """
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

        fwrite(_tmlang_path, _tmlang)

        return

    def gen_syntax_sub_pattern(self, severity):
        svt = get_prefs().get('severity')
        pat = (svt.get(severity)).get('pattern')

        pat_tmlang = ""
        for _str in pat:
            _str[0] = self.conv_for_plist(_str[0])
            _str[1] = self.conv_for_plist(_str[1])
            if _str[1] != "":
                pat_tmlang = pat_tmlang + """
        <dict>
            <key>begin</key>
            <string>""" + self.conv_for_regx(_str[0]) + """</string>""" + self.gen_syntax_sub_capture(_str[0], severity, 0) + """
            <key>end</key>
            <string>""" + self.conv_for_regx(_str[1]) + """</string>""" + self.gen_syntax_sub_capture(_str[1], severity, 1)
            else:
                pat_tmlang = pat_tmlang + """
        <dict>
            <key>match</key>
            <string>""" + self.conv_for_regx(_str[0]) + """</string>""" + self.gen_syntax_sub_capture(_str[0], severity, 2)
            pat_tmlang = pat_tmlang + """
            <key>name</key>
            <string>msg.""" + severity + """</string>
            <key>patterns</key>
            <array>
                <dict>
                    <key>include</key>
                    <string>#""" + severity + """_link</string>
                </dict>
                <dict>
                    <key>include</key>
                    <string>#""" + severity + """_quote</string>
                </dict>
            </array>
        </dict>"""
        return pat_tmlang

    def gen_syntax_sub_capture(self, regx, severity, sel):
        spw  = re.compile(r'\{\{\{LINK\}\}\}|\{\{\{QUOTE\}\}\}').findall(regx)
        if len(spw) == 0:
            return ""
        if sel == 0:
            ret = """
            <key>beginCaptures</key>
            <dict>"""
        elif sel == 1:
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
                    <string>msg.""" + severity + """.""" + lqs + """</string>
                </dict>"""
        ret = ret + """
            </dict>"""
        return ret

    def gen_syntax_sub_link_quote(self, severity):
        lq_tmlang = """
        <key>""" + severity + """_link</key>
        <dict>
            <key>match</key>
            <string>""" + LINK_REGX_PLIST + """</string>
            <key>name</key>
            <string>msg.""" + severity + """.link</string>
        </dict>
        <key>""" + severity + """_quote</key>
        <dict>
            <key>match</key>
            <string>""" + QUOTE_REGX_PLIST + """</string>
            <key>name</key>
            <string>msg.""" + severity + """.quote</string>
        </dict>"""
        return lq_tmlang

    def conv_for_plist(self, _str):
        _str = re.sub('\<', '&lt;', _str)
        _str = re.sub('\>', '&gt;', _str)
        return _str

    def conv_for_regx(self, _str):
        _str = re.sub(r'\{\{\{LINK\}\}\}', LINK_REGX_SETTING, _str)
        _str = re.sub(r'\{\{\{QUOTE\}\}\}', QUOTE_REGX_SETTING, _str)
        return _str

    def gen_theme(self):
        """
        generate custom theme file : Log Highlight.hidden-tmTheme
        """

        lhs = get_prefs()
        svt = lhs.get('severity')
        sub_theme   = ""
        global severity_list
        for i, k in enumerate(severity_list):
            for j, c in enumerate(list((svt.get(k)).get('color'))):
                p = "" if c == 'base' else "." + c
                sub_theme += """
        <dict>
            <key>scope</key>
            <string>msg.""" + k + p + """</string>
            <key>settings</key>
            <dict>
                <key>foreground</key><string>""" + ((svt.get(k)).get('color')).get(c) + """</string>
                <!-- <key>fontStyle</key> -->
                <!-- <string>bold</string> -->
            </dict>
        </dict>"""

        theme_color = lhs.get('theme_color')
        _tmtheme = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>name</key>
    <string>Log Highlight</string>
    <key>settings</key>
    <array>
        <dict>
            <key>settings</key>
            <dict>
                <key>background</key><string>""" + theme_color.get('background') + """</string>
                <key>foreground</key><string>""" + theme_color.get('foreground') + """</string>
                <key>caret</key><string>""" + theme_color.get('caret') + """</string>
                <key>selection</key><string>""" + theme_color.get('selection') + """</string>
                <key>selectionBorder</key><string>""" + theme_color.get('selectionBorder') + """</string>
                <key>lineHighlight</key><string>""" + theme_color.get('lineHighlight') + """</string>
            </dict>
        </dict>"""
        _tmtheme = _tmtheme + sub_theme
        _tmtheme = _tmtheme + """
        <dict>
            <key>scope</key>
            <string>summary.title</string>
            <key>settings</key>
            <dict>
                <key>foreground</key><string>""" + theme_color.get('summary_title') + """</string>
                <!-- <key>fontStyle</key> -->
                <!-- <string>bold</string> -->
            </dict>
        </dict>
    </array>
    <key>uuid</key>
    <string>403e2150-aad4-41ff-86d0-36d87510918e</string>
</dict>
</plist>
"""
        _user_path   = os.path.join(sublime.packages_path(), 'User')
        if not os.path.exists(_user_path):
            os.makedirs(_user_path)
        _tmtheme_path = os.path.join(_user_path, 'Log Highlight.hidden-tmTheme')

        fwrite(_tmtheme_path, _tmtheme)

        return


##  class LogHighlightEraseCustomSyntaxThemeCommand  __________

class LogHighlightEraseCustomSyntaxThemeCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        ret = sublime.ok_cancel_dialog('Erase Customized Log Highlight Syntax & Theme ?')
        if ret:
            try:
                wins_l = sublime.windows()
                for w in wins_l:
                    s_view = w.get_output_panel('loghighlight')
                    if s_view:
                        w.run_command("hide_panel", {"panel": "output.loghighlight"})
                        s_view.set_syntax_file('Packages/Log Highlight/Log Highlight.tmLanguage')
                        s_view.settings().set('color_scheme', 'Packages/Log Highlight/Log Highlight.hidden-tmTheme')
                    view_l = w.views()
                    for v in view_l:
                        if check_syntax(v):
                            v.set_syntax_file('Packages/Log Highlight/Log Highlight.tmLanguage')
                            v.settings().set('color_scheme', 'Packages/Log Highlight/Log Highlight.hidden-tmTheme')

                usr_syntax = os.path.join(sublime.packages_path(), 'User/Log Highlight.tmLanguage')
                if os.path.exists(usr_syntax):
                    os.remove(usr_syntax)

                usr_theme = os.path.join(sublime.packages_path(), 'User/Log Highlight.hidden-tmTheme')
                if os.path.exists(usr_theme):
                    os.remove(usr_theme)

            except Exception:
                disp_exept()

##  Log Highlight  ____________________________________________

# to prevent re-run in short time
is_working  = False

# for refresh
is_waiting  = False
req_refresh = []

# managin vies
logh_view   = []
logh_lastv  = -1

# summary view
smry_view  = None

##  class LogHighlightCommand  ________________________________

class LogHighlightCommand(sublime_plugin.TextCommand):

    def run(self, edit):

        # check log type
        ltype = get_prefs().get('log_type', 'compile')
        if isinstance(ltype, str) and ltype.lower() == 'system':
            set_syntax_theme(self.view)
            return

        # workaround for ST3 result_file_regex bug
        use_link = get_prefs().get('use_link', True)
        if ST3 and use_link:
            resfr_wa = self.view.settings().get('resfr_wa', False)
            if not resfr_wa:
                self.view.settings().set('result_file_regex', LINK_REGX_RESULT)
                text = self.view.substr(sublime.Region(0, self.view.size()))
                self.view.erase(edit, sublime.Region(0, self.view.size()))
                self.view.insert(edit, 0, text)
                self.view.settings().set('resfr_wa', True)
                self.view.settings().set('need_to_save', True)

        global is_working
        if is_working:
            return

        lhthread = LogHighlightThread(self.view, True)
        if ST3:
            lhthread.start()
        else:
            lhthread.run()

    def is_visible(self):
        """ context menu visible """

        lhs = get_prefs()
        if not lhs.get("context_menu", True):
            return False

        is_summary = self.view.settings().get('loghighlight_summary', False)
        if is_summary:
            return False

        try:
            ext_l = lhs.get("log_ext")  # [".log"]
            if any(".*" == s for s in ext_l):
                return True

            # unknow view also passed (like output window)
            if self.view.file_name() is None:
                return True

            _name = self.view.file_name() if self.view.name() == "" else self.view.name()
            ext   = os.path.splitext(_name)[1]
            ext   = ext.lower()

            if any(ext == s for s in ext_l):
                return True
            else:
                return False
        except Exception:
            return False


##  class LogHighlightEvent  __________________________________

class LogHighlightEvent(sublime_plugin.EventListener):

    # for ST2
    def on_load(self, view):
        if ST3:
            return
        self.auto_highlight(view)

    def on_activated(self, view):  # for open directly
        if ST3:
            return
        if not check_syntax(view):
            self.auto_highlight(view)

    def on_modified(self, view):
        if is_compile_type():  # nothing to do
            return

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
    def on_load_async(self, view):
        self.auto_highlight(view)

    def on_activated_async(self, view):  # for open directly
        if not check_syntax(view):
            self.auto_highlight(view)

    def on_modified_async(self, view):
        if is_compile_type():  # nothing to do
            return

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

    def on_post_window_command(self, view, command_name, args):
        if command_name == 'show_panel' and 'panel' in args.keys() and args['panel'] == 'output.exec':
            lhs = get_prefs()
            aut_h = lhs.get("auto_highlight", False)
            if not aut_h:
                return
            bwin = view.get_output_panel('exec')
            if not check_syntax(bwin):
                bwin.run_command("log_highlight")
        return

    def on_close(self, view):
        for vid in logh_view:
            if view.id() == vid[0]:
                logh_view.remove(vid)
            break
        global logh_lastv
        if view.id() == logh_lastv:
            if len(logh_view) > 0:
                logh_lastv = logh_view[-1]
            else:
                logh_lastv = -1
        return

    def auto_highlight(self, view):
        lhs = get_prefs()
        aut_h = lhs.get("auto_highlight", False)
        if not aut_h:
            return
        ext_l = lhs.get("log_ext")  # [".log"]
        if any(".*" == s for s in ext_l):
                return
        _name = "" if view.file_name() is None else view.file_name()
        ext   = os.path.splitext(_name)[1]
        ext   = ext.lower()
        if any(ext == s for s in ext_l):
            view.run_command("log_highlight")


##  class LogHighlightRefreshThread  __________________________

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
                sublime.set_timeout(self.refresh_wait, REFRESH_WAIT)  # milliseconds
                break
        return

    def refresh_wait(self):
        global logh_view
        for i, vid in enumerate(logh_view):
            if self.view.id() == vid[0]:
                if self.last_req != vid[1]:  # more requests are comming
                    self.last_req = vid[1]
                    sublime.set_timeout(self.refresh_wait, REFRESH_WAIT)  # milliseconds
                else:
                    global is_working
                    if is_working or self.view.is_loading():
                        logh_view[i][1] = logh_view[i][1] + 1
                        sublime.set_timeout(self.refresh_wait, REFRESH_WAIT)  # milliseconds
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


##  class LogHighlightThread  _________________________________

class LogHighlightThread(threading.Thread):

    def __init__(self, view, is_first):
        threading.Thread.__init__(self)
        self.view     = view
        self.is_first = is_first

    def run(self):
        try:
            self.run_imp()
        except Exception:
            global is_working
            is_working = False
            disp_exept()

    def run_imp(self):
        """
        Log Highligh Main Process
        """

        global is_working
        is_working = True
        log_name   = self.view.file_name()
        use_link   = get_prefs().get('use_link', True)

        # to support unsaved file (like Tail)
        if not log_name:
            log_name   = self.view.settings().get('filepath', '')
        if not log_name or not os.path.isfile(log_name):
            self.view.settings().set('floating', True)
            if use_link:
                sublime.status_message("Log Highlight : This is a floating (or unsaved) view. Can't use the relative link.")
        else:
            self.view.settings().set('floating', False)
            # workaround for ST3 result_file_regex bug
            if ST3 and use_link:
                save = self.view.settings().get('need_to_save', False)
                if save:
                    self.view.run_command('save')
                    self.view.settings().set('need_to_save', False)

        self.base_dir = ""
        self.try_search_base = False

        # workaround for output panel
        if self.is_first or self.view.file_name() is None:
            # set syntax for coloring / set read only
            set_syntax_theme(self.view)
            # self.view.set_read_only(True) # cannot call on_modified
            self.view.settings().set("always_prompt_for_file_reload", False)

        if self.is_first:
            global logh_view
            if not any(self.view.id() == vid[0] for vid in logh_view):
                logh_view.append([self.view.id(), 0])
            wins_l = sublime.windows()
            for w in wins_l:
                view_l = w.views()
                for v in view_l:
                    if check_syntax(v):
                        v.settings().set('logh_lastv', False)

            global logh_lastv
            logh_lastv = self.view.id()
            self.view.settings().set('logh_lastv', True)
        else:
            if use_link:
                get_base_dir = self.view.settings().get('result_base_dir', '')
                if get_base_dir is None or get_base_dir == "":
                    self.try_search_base = True
                    self.search_base(log_name)
                    if self.base_dir != "":
                        self.view.settings().set('result_base_dir', self.base_dir)
                else:
                    self.base_dir = get_base_dir

            # bookmark & summary
            self.do_next()
            is_working = False
            return

        if use_link:
            # to set base directory
            self.try_search_base = True
            self.search_base(log_name)

            # set base dir & apply 'result_file_regex'
            if self.base_dir != "":
                self.view.settings().set('result_base_dir', self.base_dir)
            self.view.settings().set('result_file_regex', LINK_REGX_RESULT)

        # bookmark & summary
        self.do_next()
        is_working = False
        return

    def do_next(self):
        # enumerate severity
        self.enum_severity(self.view)

        # add bookmarks
        self.goto_line = None
        self.add_bookmarks(self.view)

        # summary
        self.do_summary(self.view)

        # update status message
        if self.try_search_base:
            if self.search_base_success:
                floating  = self.view.settings().get('floating', True)
                srch_opt  = get_prefs().get('search_base', [])
                srcn_en   = srch_opt.get('enable', True)
                if (not floating) and srcn_en:
                    sublime.status_message("Log Highlight : Found Base Directory - " + self.base_dir)
                else:
                    sublime.status_message("Log Highlight : Skipped to search base directory")
            else:
                sublime.status_message("Log Highlight : Unable to Find Base Directory !")

        lhs = get_prefs()
        goto_error = lhs.get('bookmark_goto_error', True)
        if goto_error:
            sublime.set_timeout(self.go_to_line, 50)
        return

    def go_to_line(self):
        # go to 1st error line
        if self.goto_line is not None:
            self.view.show(self.goto_line)

    def get_rel_path_file(self):
        # to support unsaved file (like Tail)
        logn = self.view.file_name()
        if logn:
            text = self.view.substr(sublime.Region(0, self.view.size()))
        else:
            logn = self.view.settings().get('filepath', '')
            text = fread(logn)

        files_l  = re.compile(LINK_REGX_RELPATH).findall(text)
        rel_path = False
        if len(files_l) > 0:
            for file_name in files_l:
                if not os.path.isabs(file_name):  # use the first in relative path list
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
        srch_opt = get_prefs().get('search_base', [])
        srcn_en  = srch_opt.get('enable', True)
        floating = self.view.settings().get('floating', True)

        if floating or (not srcn_en):
            self.search_base_success = True
            self.base_dir = "."
            sublime.status_message("Log Highlight : Skipped to search base directory")
            return

        file_name = self.get_rel_path_file()
        self.search_base_success = True
        self.base_dir = ""
        if file_name == "":
            return

        excludes  = srch_opt.get('ignore_dir', [])
        max_scan  = srch_opt.get('max_scan_path', MAX_SCAN_PATH)
        old_path  = ["", 0]
        _path     = os.path.dirname(log_name)
        _depth    = _path.count(os.path.sep)
        new_path  = [_path, _depth]
        scan_path = 0
        found     = False
        try:
            # check open folder first
            for root in sublime.active_window().folders():
                if os.path.isfile(os.path.join(root, file_name)):
                    self.base_dir = root
                    found = True
                    break

            if not found:
                # scanning near the log
                for i in range(MAX_STAIR_UP_PATH):
                    for root, dirs, files in os.walk(new_path[0]):
                        dirs[:] = [d for d in dirs if (d not in excludes) and d[0] != '.']
                        if i == 0 or not root.startswith(old_path[0]):
                            sublime.status_message("Log Highlight : Searching - " + root)
                            # print (root)
                            if os.path.isfile(os.path.join(root, file_name)):
                                self.base_dir = root
                                found = True
                                break
                            else:
                                scan_path = scan_path + 1
                                if scan_path > max_scan - 1:
                                    break
                    if found or scan_path > max_scan - 1:
                        break
                    else:
                        # print ("Searching Uppder Directory")
                        old_path = [new_path[0], new_path[0].count(os.path.sep)]
                        _path    = os.path.dirname(old_path[0])
                        _depth   = _path.count(os.path.sep)
                        if old_path[1] == _depth or _depth < 1:  # to stop level 1 (old_path[1] == _depth == 1)
                            break
                        else:
                            new_path = [_path, _depth]
            pass

        except Exception:
            disp_exept()

        if found:
            sublime.status_message("Log Highlight : Found base directory (" + str(scan_path) + ") - " + self.base_dir)
        else:
            sublime.status_message("Log Highlight : Fail to find (" + str(scan_path) + ") - " + file_name)

        self.search_base_success = found
        return

    def enum_severity(self, view):
        lhs = get_prefs()
        svt = lhs.get('severity')

        self.messages = {}
        self.regions  = {}
        self.n_errors = 0
        self.n_warns  = 0

        global severity_list
        for i, k in enumerate(severity_list):
            head = ""
            msg  = ""
            pat  = (svt.get(k)).get('pattern')
            for i, _pat in enumerate(pat):
                _pat[0]  = self.conv_for_regx(_pat[0])
                _pat[1]  = self.conv_for_regx(_pat[1])
                _tail    = '' if i == len(pat) - 1 else '|'
                head    += '(' + _pat[0] + ')' + _tail if _pat[1] == '' else '(' + _pat[0] + '.*?[\\r\\n])' + _tail
                msg     += '(' + _pat[0] + ')' + _tail if _pat[1] == '' else '(' + _pat[0] + '.*?' + _pat[1] + ')' + _tail
            region = view.find_all(head)
            self.messages[k] = msg
            self.regions[k]  = region
            if k == 'error':
                self.n_errors   = str(len(region))
            elif k == 'warning':
                self.n_warns    = str(len(region))

        return

    def add_bookmarks(self, view):
        lhs = get_prefs()
        svt = lhs.get('severity')
        bmark_enable = lhs.get('bookmark_enable', True)
        if not bmark_enable:
            return

        # goto 1st error line
        region = self.regions['error']
        if len(region) > 0:
            self.goto_line = region[0]

        # bookmark icon
        if ST3:
            for i, k in enumerate(severity_list):
                icon = (svt.get(k)).get('icon')
                if icon:
                    if icon == 'dot' or icon == 'circle' or icon == 'bookmark':
                        icon = icon
                    else:
                        icon = "Packages/Log Highlight/icons/" + icon
                    view.add_regions(k, self.regions[k], "bookmarks", icon, sublime.HIDDEN | sublime.PERSISTENT)
        else:
            for i, k in enumerate(severity_list):
                icon = (svt.get(k)).get('icon')
                if icon:
                    if icon == 'dot' or icon == 'circle' or icon == 'bookmark':
                        view.add_regions(k, self.regions[k], "bookmarks", icon, sublime.HIDDEN | sublime.PERSISTENT)
                    else:
                        view.add_regions(k, self.regions[k], "bookmarks", "dot", sublime.HIDDEN | sublime.PERSISTENT)

        return

    def do_summary(self, view):
        lhs = get_prefs()
        summary_panel = lhs.get("summary_panel", True)
        if not summary_panel:
            return

        # skip summary for unsaved view
        log_name = view.file_name()
        if log_name:
            log_name = os.path.split(view.file_name())[1]
        else:
            return

        # summary title
        filt_msg  = ""
        global severity_list
        svt = lhs.get('severity')
        sml = []
        for i, k in enumerate(severity_list):
            if (svt.get(k)).get('summary', False):
                sml.append(k)
        for i, k in enumerate(sml):
            if i == len(sml) - 1:
                filt_msg  += self.messages.get(k)
            else:
                filt_msg  += self.messages.get(k) + '|'
        summary   = "\n" + "Log Highlight Summary ( " + str(self.n_errors) + " ) errors, ( " + str(self.n_warns) + " ) warnings   ( " + log_name + " )\n" + "-" * 100 + "\n"

        # summary
        text     = view.substr(sublime.Region(0, view.size()))
        text     = text + '\n'  # workaround when there is no '\n' at last
        ewtext_l = re.compile(filt_msg, re.MULTILINE | re.DOTALL).findall(text)

        for txt in ewtext_l:
            if isinstance(txt, tuple):
                for _str in txt:
                    if _str != '':
                        _str    = re.sub(re.compile(r'[\r\n]+$'), '', _str)
                        summary = summary + _str + '\n\n'
            elif isinstance(txt, str):
                if txt != '':
                    _str    = re.sub(re.compile(r'[\r\n]+$'), '', txt)
                    summary = summary + _str + '\n\n'

        global smry_view
        smry_view = view.window().get_output_panel('loghighlight')
        smry_view.settings().set('loghighlight_summary', True)
        smry_view.settings().set('gutter', True)
        smry_view.settings().set('line_numbers', False)
        smry_view.set_read_only(False)
        view.window().run_command("show_panel", {"panel": "output.loghighlight"})
        if lhs.get('use_link', True):
            smry_view.settings().set('result_file_regex', LINK_REGX_RESULT)
            if self.base_dir != "":
                smry_view.settings().set('result_base_dir', self.base_dir)
        set_syntax_theme(smry_view)
        if ST3:
            smry_view.run_command("append", {"characters": summary})
        else:
            edit = smry_view.begin_edit()
            smry_view.erase(edit, sublime.Region(0, smry_view.size()))
            smry_view.insert(edit, smry_view.size(), summary)
            smry_view.end_edit(edit)
        smry_view.set_read_only(True)

        return

    def conv_for_regx(self, _str):
        _str = re.sub(r'\{\{\{LINK\}\}\}', LINK_REGX_SUMMARY, _str)
        _str = re.sub(r'\{\{\{QUOTE\}\}\}', QUOTE_REGX_SUMMARY, _str)
        return _str


##  class LogHighlightPanelCommand  ___________________________

class LogHighlightPanelCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        try:
            global smry_view
            if smry_view:
                if bool(smry_view.window()):
                    self.view.window().run_command("hide_panel", {"panel": "output.loghighlight"})
                else:
                    self.view.window().run_command("show_panel", {"panel": "output.loghighlight"})
        except Exception:
            disp_exept()


##  class LogHighlightSetAsBaseCommand  _______________________

class LogHighlightSetAsBaseCommand(sublime_plugin.TextCommand):

    def run(self, edit, **args):
        try:
            path = args.get('paths', [])[0]
            if os.path.isfile(path):
                path = os.path.dirname(path)

            view = sublime.active_window().active_view()
            if check_syntax(view):
                disp_msg('base directory of current log is set as : ' + path)
                self.view.settings().set('result_base_dir', path)
                global smry_view
                if smry_view is not None:
                    smry_view.settings().set('result_base_dir', path)
            pass

        except Exception:
            disp_exept()
