from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime

#  实用价值：命令模式是实现撤销/重做功能、宏命令、事务处理的理想选择！
class Command(ABC):
    """命令抽象类"""
    @abstractmethod
    def execute(self) -> None:
        pass
    
    @abstractmethod
    def undo(self) -> None:
        pass

class TextEditor:
    """文本编辑器 - 接收者"""
    def __init__(self):
        self.content = ""
        self.history: List[str] = []
    
    def write(self, text: str) -> None:
        self.history.append(self.content)
        self.content += text
        print(f"📝 写入文本: '{text}' -> 当前内容: '{self.content}'")
    
    def delete(self, length: int) -> None:
        if length <= len(self.content):
            self.history.append(self.content)
            deleted_text = self.content[-length:]
            self.content = self.content[:-length]
            print(f"🗑️ 删除 {length} 个字符: '{deleted_text}' -> 当前内容: '{self.content}'")
        else:
            print("❌ 删除长度超过文本长度")
    
    def get_content(self) -> str:
        return self.content

class WriteCommand(Command):
    """写入命令"""
    def __init__(self, editor: TextEditor, text: str):
        self.editor = editor
        self.text = text
        self.previous_state = ""
    
    def execute(self) -> None:
        self.previous_state = self.editor.get_content()
        self.editor.write(self.text)
    
    def undo(self) -> None:
        self.editor.content = self.previous_state
        print(f"↩️ 撤销写入操作 -> 恢复内容: '{self.editor.content}'")

class DeleteCommand(Command):
    """删除命令"""
    def __init__(self, editor: TextEditor, length: int):
        self.editor = editor
        self.length = length
        self.deleted_text = ""
    
    def execute(self) -> None:
        self.deleted_text = self.editor.content[-self.length:] if self.length <= len(self.editor.content) else self.editor.content
        self.editor.delete(self.length)
    
    def undo(self) -> None:
        self.editor.content += self.deleted_text
        print(f"↩️ 撤销删除操作 -> 恢复内容: '{self.editor.content}'")

class CommandInvoker:
    """命令调用者 - 支持撤销/重做"""
    def __init__(self):
        self._command_history: List[Command] = []
        self._undo_history: List[Command] = []
    
    def execute_command(self, command: Command) -> None:
        command.execute()
        self._command_history.append(command)
        self._undo_history.clear()  # 执行新命令时清空重做历史
    
    def undo(self) -> None:
        if self._command_history:
            command = self._command_history.pop()
            command.undo()
            self._undo_history.append(command)
        else:
            print("❌ 没有可撤销的操作")
    
    def redo(self) -> None:
        if self._undo_history:
            command = self._undo_history.pop()
            command.execute()
            self._command_history.append(command)
        else:
            print("❌ 没有可重做的操作")
    
    def show_history(self) -> None:
        print(f"📋 命令历史: {len(self._command_history)} 个命令")

# 测试命令模式
def test_command_pattern():
    print("=== 命令模式测试 ===")
    
    editor = TextEditor()
    invoker = CommandInvoker()
    
    # 执行一系列命令
    write_cmd1 = WriteCommand(editor, "Hello")
    invoker.execute_command(write_cmd1)
    
    write_cmd2 = WriteCommand(editor, " World")
    invoker.execute_command(write_cmd2)
    
    delete_cmd = DeleteCommand(editor, 5)  # 删除"World"
    invoker.execute_command(delete_cmd)
    
    # 撤销操作
    print("\n--- 撤销操作 ---")
    invoker.undo()  # 撤销删除
    invoker.undo()  # 撤销第二次写入
    
    print("\n--- 重做操作 ---")
    invoker.redo()  # 重做第二次写入
    
    invoker.show_history()

test_command_pattern()