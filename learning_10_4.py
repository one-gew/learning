from pathlib import Path
# current_path = Path('.')
# print(current_path.resolve())
#可以使用resolve来查找绝对路径

# home = Path.home()
# docs = home / 'codex'
# print(docs)
#可以使用 / 来连接两个文件

# path = Path('D:/learning')
# print (path.exists())
# print(path.is_dir())
# print(path.is_file())

#文件的读取与写入

# path = Path('D:/learning/ai-internship/data/sample.txt')
# print (path.exists())
# print(path.is_dir())
# path.write_text('''产品名称：智能台灯
# 保修期限：购买之日起一年。
# 使用说明：长按电源键三秒开机。''')
#
# content = path.read_text()
# print(content)
# 遍历文件夹
# for item in Path('D:/learning').iterdir():
#     print(item)

# path = Path('D:/learning/learning_10_4.py')
# print(path.name)
# print(path.suffix)
# print(path.stem)
# print(path.parent)

#创建文件目录
# path = Path('new.folder')
# path.mkdir(parents=True, exist_ok=True)
#parents=True用于确认有父目录，exist_ok确保目录存在，但是exist_ok不能确保文件存在，还是会提示FileExistsError

#遍历所有匹配文件
# path = Path('.')
# for file in path.glob('*.py'):
#     print(file)
# for file in path.rglob('*.py'):
#     print(file)
#glob是遍历当前层级目录，rglob是遍历当前目录（含子目录）所有层级的匹配项

