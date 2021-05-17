import pytest
from py._xmlgen import html


def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = " 验证演示环境各链接是否活跃"

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("所属部门: 测试部")])
    prefix.extend([html.p("测试人员: 田晨旭")])

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    getattr(report, 'extra', [])
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")  # 解决乱码

@pytest.mark.optionalhook
def pytest_html_results_table_header(cells):
    cells.pop(-1)  # 删除link列


@pytest.mark.optionalhook
def pytest_html_results_table_row(report, cells):
    cells.pop(-1)  # 删除link列
