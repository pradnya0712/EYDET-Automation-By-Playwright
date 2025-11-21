import pytest
import datetime
import os
import base64
from pytest_html import extras
import re
from utils.excel_writer import update_test_results_in_excel_sheet
from playwright.sync_api import sync_playwright

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
captured_results = []


@pytest.fixture(scope="function")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True, storage_state="auth.json")
        page = context.new_page()

        # store soft assertion screenshots inside page object
        page._soft_fail_screens = []

        APP_URL = "https://rapidwebcra-det-af.accelya.io/CRA/home.htm"
        page.goto(APP_URL, wait_until="domcontentloaded")
        yield page

        context.close()
        browser.close()


def pytest_configure(config):
    if not os.path.exists("reports"):
        os.makedirs("reports")

    test_paths = config.args
    test_file = (
        os.path.splitext(os.path.basename(test_paths[0]))[0] if test_paths else "report"
    )

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    config.option.htmlpath = f"reports/{test_file}_{timestamp}.html"


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    page = item.funcargs.get("browser_page")

    if report.when == "call":
        test_id = item.name
        status = "PASS" if report.passed else "FAIL"
        error_msg = ""
        if report.failed:
            excinfo = call.excinfo
            if excinfo:
                full_error = str(excinfo.value)
                if "Call log:" in full_error:
                    error_msg = full_error.split("Call log:")[0].strip()
                else:
                    error_msg = full_error.strip()
                # report.longrepr = error_msg

        captured_results.append(
            {
                "id": test_id,
                "status": status,
                "error": error_msg,
            }
        )

    if report.when == "call" and page:
        # Ensure report.extras exists
        if not hasattr(report, "extras"):
            report.extras = []

        # Attach soft failure screenshots
        if hasattr(page, "_soft_fail_screens"):
            for img in page._soft_fail_screens:
                b64 = base64.b64encode(img).decode()
                html = f'<img src="data:image/png;base64,{b64}" width="500" style="border:1px solid #ccc;" />'
                report.extras.append(extras.html(html))


def clean_text_for_log(value):
    if not isinstance(value, str):
        return value
    value = _ANSI_ESCAPE.sub("", value)
    value = "".join(ch for ch in value if ord(ch) >= 32 or ch in ("\t", "\n"))
    return value


def pytest_sessionfinish(session, exitstatus):
    output_file = "logs/test_output.txt"

    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(output_file, "w", encoding="utf-8") as f:
        for res in captured_results:
            line = f"{res['id']} {res['status']}"
            if res["error"]:
                clean_error = clean_text_for_log(res["error"])
                line += f" | {clean_error}"
            f.write(line + "\n")

    print(f"Test results written to {output_file}")
    update_test_results_in_excel_sheet(output_file)
    print("Excel updated with latest test results.")


def pytest_html_results_summary(prefix, summary, postfix):
    prefix.clear()
    summary.clear()
    postfix.clear()


# ------------------------ Keep only screenshots, remove default failure extras ------------------------
def pytest_html_results_table_html(report, data):
    filtered = [d for d in data if "<img" in d]
    data[:] = filtered


# ------------------------ Filter extras globally ------------------------
@pytest.hookimpl(optionalhook=True)
def pytest_html_extras(extra):
    # Keep only HTML extras (screenshots)
    return [e for e in extra if getattr(e, "format", None) == "html"]
