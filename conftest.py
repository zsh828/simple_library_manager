import sys
import os

# 将项目根目录添加到 Python 路径中，以便 tests 可以导入 src 包
# sys.path[0] 通常是当前执行脚本的目录，对于 pytest 来说，
# 这通常是运行 pytest 命令的目录（即项目根目录）。
if os.getcwd() not in sys.path:
    sys.path.insert(0, os.getcwd())