# 工程字符串搜索工具

根据配置文件中的字符串列表，在指定目录中搜索所有文本文件，记录每个字符串出现的文件路径和行号，输出到 CSV 文件。

## 安装依赖

```bash
cd ../../python-toolkit
uv pip install -e .
```

## 使用方法

### 1. 创建配置文件

创建 `config.json` 文件：

```json
{
  "strings": ["要搜索的字符串", "另一个字符串"],
  "directories": ["../src", "./docs"],
  "ignore_dirs": ["test", ".venv"]
}
```

| 字段 | 说明 |
|------|------|
| `strings` | 要搜索的字符串/正则表达式列表 |
| `directories` | 要搜索的目录列表 |
| `ignore_dirs` | （可选）额外忽略的目录 |

### 2. 运行搜索

**普通字符串匹配（默认）：**

```bash
python strings_search.py -c config.json
```

**正则表达式匹配：**

```bash
python strings_search.py -c config.json -r
```

### 3. 查看结果

结果会保存到 `search_results.csv`，包含三列：

| 列名 | 说明 |
|------|------|
| `String` | 匹配到的字符串 |
| `File` | 文件路径 |
| `Line` | 行号 |

## 命令行参数

| 参数 | 说明 |
|------|------|
| `-c, --config` | 配置文件路径（默认：`config.json`） |
| `-o, --output` | 输出 CSV 文件路径（默认：`search_results.csv`） |
| `-r, --regex` | 启用正则表达式匹配模式 |

## 正则表达式示例

启用 `-r` 模式后，`strings` 列表中的内容会作为正则表达式解析：

```json
{
  "strings": [
    "error_\\d+",
    "warning.*deprecated",
    "class \\w+Error"
  ]
}
```

可匹配：
- `error_123`、`error_999` 等
- `warning: this feature is deprecated` 等
- `class MyError`、`class ValueError` 等

## 注意事项

- 默认忽略的目录：`.git`、`.svn`、`.hg`、`__pycache__`、`node_modules`、`dist`、`build`、`venv`、`env`
- 所有文本文件都会被搜索
- 使用 `--regex` 时会提前验证正则表达式有效性，无效则报错退出