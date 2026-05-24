# logger.py
import csv
import os
import time

RESULT_DIR = 'results'
if not os.path.exists(RESULT_DIR):
    os.makedirs(RESULT_DIR)

_results = []
_start_time = None

def start():
    global _results, _start_time
    _results = []
    _start_time = time.time()
    print('='*60)
    print('  Selenium Web 自动化测试 开始执行')
    print(f'  开始时间：{time.strftime("%Y-%m-%d %H:%M:%S")}')
    print('='*60)

def log(tc_id, tc_name, module, result, remark='', duration=0.0):
    row = {
        'tc_id': tc_id,
        'tc_name': tc_name,
        'module': module,
        'result': result,
        'remark': remark,
        'duration': f'{duration:.2f}s'
    }
    _results.append(row)

    flag = '✓' if result == '通过' else '✗'
    print(f'  [{flag}] {tc_id} | {module} | {tc_name} | {result} | {duration:.2f}s | {remark}')

def summary(browser='chrome'):
    total = len(_results)
    passed = sum(1 for r in _results if r['result']=='通过')
    failed = total - passed
    elapsed = time.time() - _start_time if _start_time else 0

    print()
    print('='*60)
    print(f'  测试执行完毕 — 汇总报告 [{browser.upper()}]')
    print('='*60)
    print(f'  总用例数：{total}')
    print(f'  通过：    {passed}')
    print(f'  失败：    {failed}')
    print(f'  通过率：  {passed/total*100:.1f}%' if total>0 else '  通过率：N/A')
    print(f'  总耗时：  {elapsed:.2f}s')
    print('='*60)

    timestamp = time.strftime('%Y%m%d_%H%M%S')
    csv_path = f'{RESULT_DIR}/report_{browser}_{timestamp}.csv'
    with open(csv_path, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=['tc_id','tc_name','module','result','duration','remark'])
        writer.writeheader()
        writer.writerows(_results)

        # ✅ 写入汇总行
        f.write('\n')
        f.write(f'总用例数,{total}\n')
        f.write(f'通过,{passed}\n')
        f.write(f'失败,{failed}\n')
        f.write(f'通过率,{passed/total*100:.1f}%\n' if total>0 else '通过率,N/A\n')
        f.write(f'总耗时,{elapsed:.2f}s\n')
        f.write(f'浏览器,{browser.upper()}\n')

    print(f'  [报告已保存] {csv_path}')
    return {'total':total,'passed':passed,'failed':failed,'elapsed':elapsed,'csv_path':csv_path}