import logger
from test_orangehrm import runtest1
from test_demoqa import runtest2
from test_theinternet import runtest3
from test_exception import runtest_exception

if __name__ == '__main__':

    # ── Chrome 主测试 ──────────────────────────────────────
    logger.start()
    runtest1('chrome')
    runtest2('chrome')
    runtest3('chrome')
    logger.summary('chrome')

    # ── Edge 主测试 ────────────────────────────────────────
    logger.start()
    runtest1('edge')
    runtest2('edge')
    runtest3('edge')
    logger.summary('edge')

    # ── Firefox 主测试 ─────────────────────────────────────
    logger.start()
    runtest1('firefox')
    runtest2('firefox')
    runtest3('firefox')
    logger.summary('firefox')

    # ── 异常处理机制验证（不计入主通过率，单独生成报告）──
    logger.start()
    runtest_exception('chrome')
    runtest_exception('edge')
    runtest_exception('firefox')
    logger.summary('exception')