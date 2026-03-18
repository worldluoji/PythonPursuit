#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
工程字符串搜索工具
根据配置文件中的字符串列表，在指定目录中搜索所有文本文件，
记录每个字符串出现的文件路径和行号，输出到CSV文件。
"""

import os
import json
import csv
import argparse
from typing import List, Dict, Tuple

# 默认忽略的目录（可被配置覆盖）
DEFAULT_IGNORE_DIRS = {'.git', '.svn', '.hg', '__pycache__', 'node_modules', 'dist', 'build', 'venv', 'env'}


def load_config(config_path: str) -> Dict:
    """加载JSON配置文件"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        # 验证必要字段
        if 'strings' not in config or not isinstance(config['strings'], list):
            raise ValueError("配置缺少 'strings' 列表或格式错误")
        if 'directories' not in config or not isinstance(config['directories'], list):
            raise ValueError("配置缺少 'directories' 列表或格式错误")
        return config
    except Exception as e:
        raise RuntimeError(f"读取配置文件失败: {e}")


def should_ignore_dir(dir_name: str, ignore_set: set) -> bool:
    """判断目录名是否应被忽略"""
    return dir_name in ignore_set


def search_in_file(file_path: str, strings: List[str]) -> List[Tuple[str, int]]:
    """
    在文件中搜索所有目标字符串
    返回列表，元素为 (匹配到的字符串, 行号)
    """
    matches = []
    try:
        # 以只读方式打开，忽略解码错误
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, start=1):
                for s in strings:
                    if s in line:
                        matches.append((s, line_num))
        return matches
    except (PermissionError, OSError) as e:
        # 权限不足或无法访问时跳过
        print(f"警告：无法读取文件 {file_path} - {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="搜索工程目录中的指定字符串")
    parser.add_argument('--config', '-c', default='config.json',
                        help="配置文件路径 (默认: config.json)")
    parser.add_argument('--output', '-o', default='search_results.csv',
                        help="输出CSV文件路径 (默认: search_results.csv)")
    args = parser.parse_args()

    # 加载配置
    try:
        config = load_config(args.config)
    except RuntimeError as e:
        print(e)
        return 1

    strings = config['strings']
    directories = config['directories']
    # 合并忽略目录：默认忽略 + 配置中指定的额外忽略
    ignore_dirs = DEFAULT_IGNORE_DIRS.union(set(config.get('ignore_dirs', [])))

    # 收集所有结果
    results = []  # 每个元素为 (字符串, 文件路径, 行号)

    for root_dir in directories:
        if not os.path.isdir(root_dir):
            print(f"警告：目录不存在或不可访问，跳过 - {root_dir}")
            continue

        print(f"正在搜索目录: {root_dir}")
        for dirpath, dirnames, filenames in os.walk(root_dir):
            # 修改dirnames以跳过忽略的目录（原地修改影响后续遍历）
            dirnames[:] = [d for d in dirnames if not should_ignore_dir(d, ignore_dirs)]

            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                # 可选：根据扩展名过滤（默认不过滤，全部尝试）
                matches = search_in_file(file_path, strings)
                for s, line_num in matches:
                    results.append((s, file_path, line_num))

    # 写入CSV文件
    try:
        with open(args.output, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            writer.writerow(['String', 'File', 'Line'])
            writer.writerows(results)
        print(f"搜索完成，结果已保存到: {args.output}")
        print(f"共找到 {len(results)} 处匹配。")
    except Exception as e:
        print(f"写入输出文件失败: {e}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())