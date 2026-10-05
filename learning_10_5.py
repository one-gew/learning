from pathlib import Path

# project_dir = Path(__file__).parent.absolute()
# path = project_dir /'data'/'sample.txt'
# content = path.read_text(encoding='utf-8')
# print(content)
# unempty = sum((1 for line in content.splitlines() if line.strip()))
# # unempty = sum((1 for line in content.splitlines() if content.strip())),这种写法是错误的，这种结果是整个文本的行数（包含非空行）
# print(unempty)

#列表使用【】，元素可以修改，元组使用（），元素不可修改

# def find_txt_file(directory:Path)-> list[str]:
#     file_name = []
#     for file in directory.rglob('*.txt'):
#         if file.is_file():
#             file_name.append(file.name)
#
#     return file_name
# 其中directory（参数）:Path（类型），-> list[str]（返回元素类型），rglob遍历所有文件夹，包含子文件夹，glob只遍历当前当前层级文件夹

# try:
#     file_name = find_txt_file(project_dir)
# except (OSError, UnicodeError) as error:
#     print(f"查找失败：{error}")
#     return
# 以后都可以考虑这样写，便于找到错误提示
#     print(f"文件名称：{','.join(file_names)}"),记住这种列表输出方式，美化结果输出