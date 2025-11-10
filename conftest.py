import pytest
import datetime
import os
import base64
import re
from utils.excel_writer import update_test_results_in_excel_sheet
from playwright.sync_api import sync_playwright

_ANSI_ESCAPE = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
captured_results = []


@pytest.fixture(scope="function")
def browser_page():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, args=["--start-maximized"])
        context = browser.new_context(no_viewport=True)
        page = context.new_page()
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


def pytest_html_results_table_header(cells):
    cells.append("<th>Logs</th>")


def pytest_html_results_table_row(report, cells):
    screenshot_html = (
        f"<td>{report.extra_html}</td>"
        if hasattr(report, "extra_html")
        else "<td></td>"
    )
    cells.append(screenshot_html)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

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
                report.longrepr = error_msg

        captured_results.append(
            {
                "id": test_id,
                "status": status,
                "error": error_msg,
            }
        )

    if report.when == "call" and report.failed:
        page = item.funcargs.get("browser_page")
        if page:
            screenshot_bytes = page.screenshot(timeout=60000)
            base64_img = base64.b64encode(screenshot_bytes).decode()
            data_uri = f"data:image/png;base64,{base64_img}"
            html = (
                f'<a href="{data_uri}" download="screenshot.png">'
                f'<img src="{data_uri}" width="600" height="300" style="border:1px solid #ccc;" /></a>'
            )
            report.extra_html = html


def clean_text_for_log(value):
    if not isinstance(value, str):
        return value
    # Remove terminal color codes
    value = _ANSI_ESCAPE.sub("", value)
    # Remove other non-printable ASCII characters except tab and newline
    value = "".join(ch for ch in value if ord(ch) >= 32 or ch in ("\t", "\n"))
    return value


def pytest_sessionfinish(session, exitstatus):
    output_file = "logs/test_output.txt"
    if not os.path.exists("logs"):
        os.makedirs("logs")

    with open(output_file, "w") as f:
        for res in captured_results:
            line = f"{res['id']} {res['status']}"
            if res["error"]:
                clean_error = clean_text_for_log(res["error"])
                line += f" | {clean_error}"
            f.write(line + "\n")

    print(f"Test results written to {output_file}")

    # Call your Excel update here
    update_test_results_in_excel_sheet(output_file)
    print("Excel updated with latest test results.")
