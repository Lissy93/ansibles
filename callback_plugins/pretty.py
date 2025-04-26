# pretty.py
DOCUMENTATION = r"""
callback: pretty
type: stdout
short_description: Emoji + colored status stdout callback
extends_documentation_fragment:
  - default_callback
  - result_format_callback
"""

from ansible.plugins.callback.default import CallbackModule as DefaultCb
from ansible.utils.color import colorize, hostcolor
import json

class CallbackModule(DefaultCb):
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE    = "stdout"
    CALLBACK_NAME    = "pretty"
    CALLBACK_NEEDS_WHITELIST = True

    STATUS_EMOJI = {
        "ok":          ("✅", "green"),
        "changed":     ("🔄️", "yellow"),
        "skipped":     ("⏭️", "blue"),
        "failed":      ("❌", "red"),
        "unreachable": ("🚫", "red"),
        "warning":     ("⚠️", "yellow"),
        "info":        ("ℹ️", "cyan"),
    }

    LABELS = {
        "ok":          "Successful",
        "changed":     "Changes",
        "skipped":     "Skipped",
        "failed":      "Failed",
        "unreachable": "Unreachable",
        "warning":     "Warnings",
        "info":        "Info",
    }

    # —— Silence any default banners/starts —— #
    def v2_playbook_on_task_start(self, task, is_conditional):
        return

    def v2_runner_on_start(self, host, task):
        return

    def v2_playbook_on_handler_task_start(self, task):
        return

    def v2_playbook_on_play_start(self, play):
        title = play.get_name().strip() or play._file_name or 'Mystery Playbook'
        self._display.display("", screen_only=True)
        self._display.display(title, color='magenta')
        self._display.display('─' * len(title), color='magenta')

    # —— Override includes to get an emoji —— #
    def v2_playbook_on_include(self, included_file):
        hosts = ", ".join(h.name for h in included_file._hosts)
        emoji, color = self.STATUS_EMOJI["info"]
        self._display.display(f"[{hosts}] {emoji} Included: {included_file._filename} ", color=None, newline=False)
        self._display.display(f"(Done)", color=color)

    # —— Per‐task callbacks —— #
    def v2_runner_on_ok(self, result):
        
        action = result._task.action
        if action.endswith("debug"):
            host = result._host.get_name()
            args = result._task.args or {}
            data = result._result
            # 1) msg: ... 
            if "msg" in args and data.get("msg") not in (None, ""):
                for line in str(data["msg"]).splitlines():
                    self._display.display(f" {' ' * len(host)}  {line}", color="dark gray")
            # 2) var: my_var
            elif "var" in args:
                varname = args["var"]
                val = data.get(varname)
                # print each element if it’s a list
                if isinstance(val, (list, tuple)):
                    for line in val:
                        self._display.display(f" {' ' * len(host)}  {line}")
                else:
                    self._display.display(f" {' ' * len(host)}  {varname} = {val}")
            # nothing else to do
            return

        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        e, c  = self.STATUS_EMOJI["ok"]
        self._display.display(f"[{host}] {e} {task} ", color=None, newline=False)
        self._display.display(f"(Success)", color=c)

    def v2_runner_on_changed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        e, c  = self.STATUS_EMOJI["changed"]
        self._display.display(f"[{host}] {e} {task} ", color=None, newline=False)
        self._display.display(f"(Changed)", color=c)

    def v2_runner_on_failed(self, result, ignore_errors=False):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        e, c  = self.STATUS_EMOJI["failed"]
        self._display.display(f"[{host}] {e} {task} ", color=None, newline=False)
        self._display.display(f"(Failed)", color=c)

    def v2_runner_on_skipped(self, result):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        e, c  = self.STATUS_EMOJI["skipped"]
        self._display.display(f"[{host}] {e} {task} ", color=None, newline=False)
        self._display.display(f"(Skipped)", color=c)

    def v2_runner_on_unreachable(self, result):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        e, c  = self.STATUS_EMOJI["unreachable"]
        self._display.display(f"[{host}] {e} {task} ", color=None, newline=False)
        self._display.display(f"(Unreachable)", color=c)

    # —— Loop‐item callbacks —— #
    def _print_item_details(self, result, host):
        """Helper to print msg, item.key/value, and diff.before→after."""
        indent = " " * (len(host) + 3)  # align under “[host] ”
        res = result._result

        # 1) msg
        msg = res.get("msg")
        if msg:
            self._display.display(f"{indent}{msg}", color="dark gray")

        # 2) item.key = item.value
        item = res.get("item")
        if isinstance(item, dict):
            key = item.get("key")
            val = item.get("value")
            if key and (val is not None and val != ""):
                self._display.display(f"{indent}{key} = {val}", color="dark gray")

        # 3) diff entries
        for d in res.get("diff", []):
            before = d.get("before")
            after  = d.get("after")
            if before and after:
                self._display.display(f"{indent}{before} → {after}", color="dark gray")


    def v2_runner_item_on_ok(self, result):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        changed = result._result.get("changed", False)
        key = "changed" if changed else "ok"
        label = "Changed" if changed else "Success"
        emoji, color = self.STATUS_EMOJI[key]

        # Summary line
        self._display.display(f"[{host}] {emoji} {task} ", color=None, newline=False)
        self._display.display(f"({label})", color=color)
        
        # Details
        self._print_item_details(result, host)


    def v2_runner_item_on_failed(self, result):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        emoji, color = self.STATUS_EMOJI["failed"]
        self._display.display(f"[{host}] {emoji} {task} ", color=None, newline=False)
        self._display.display(f"(Failed)", color=color)
        self._print_item_details(result, host)


    def v2_runner_item_on_skipped(self, result):
        host = result._host.get_name()
        task = result.task_name or result.task.get_name()
        emoji, color = self.STATUS_EMOJI["skipped"]
        self._display.display(f"[{host}] {emoji} {task} ", color=None, newline=False)
        self._display.display(f"(Skipped)", color=color)
        self._print_item_details(result, host)


    def v2_playbook_on_stats(self, stats):
        self._display.display('', screen_only=True)
        header = 'Summary'
        self._display.display(header, screen_only=True, color='magenta')
        self._display.display('─' * len(header), screen_only=True, color='magenta')

        for host in sorted(stats.processed.keys()):
            data = stats.summarize(host)
            self._display.display(hostcolor(host, data), screen_only=True)
            for key in ("ok", "changed", "unreachable", "failed", "skipped"):
                e, color = self.STATUS_EMOJI[key]
                count = data["failures"] if key == "failed" else data.get(key, 0)
                label = self.LABELS[key]
                if count == 0:
                  color = "dark gray"

                self._display.display(f"  {e} {count} {label}", color=color, screen_only=True)
            self._display.display("", screen_only=True)
