from pathlib import Path
import json

def read_document(path: str) -> str:
    """读取 UTF-8 文本文件。"""
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"找不到文件：{file_path}")

    return file_path.read_text(encoding="utf-8")

def count_lines(content:str)->dict[str,int]:
    lines = content.splitlines()
    total = len(lines)
    non_empty = sum(1 for line in lines if line.strip())
    return {"total":total,"non_empty":non_empty,"empty":total-non_empty
            }

def find_txt_file(directory:Path)-> list[str]:
    if not directory.is_dir():
        raise NotADirectoryError(f"不是有效目录：{directory}")
    file_names = []
    for file in directory.rglob('*.txt'):
        if not file.is_file():
            continue
        file_names.append(file.name)
    return file_names

def load_documnets(project_dir:Path,file_names:list[str])->dict[str,str]:
    contents = {}
    for file_name in file_names:
        file_path = project_dir / 'data' / file_name
        if not file_path.is_file():
            print(f"文件不存在：{file_path}")
            continue
        try:
            content = read_document(str(file_path))
        except (OSError, UnicodeError) as error:
            print(f"读取失败：{file_path}（{error}")
            continue
        contents[file_name] = content
    return contents

def save_documents(contents: dict[str, str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=2)
def main() -> None:
    # 文档路径
    global contents
    project_dir = Path(__file__).resolve().parent
    document_path = project_dir / "data" / "sample.txt"
    # print(document_path)
    # print(document_path.read_text(encoding="utf-8"))
    # 读文档
    try:
        content = read_document(str(document_path))
    except (OSError, UnicodeError) as error:
        print(f"读取失败：{error}")
        return
    # 行数统计
    stats = count_lines(content)
    # 文件查找
    try:
        file_names = find_txt_file(project_dir)
    except (OSError, UnicodeError) as error:
        print(f"查找失败：{error}")
        return
    # 文件阅读
    try:
        contents = load_documnets(project_dir, file_names)
    except (OSError, UnicodeError) as error:
        print(f"批量读取失败：{error}")
    print(f"文档读取成功:{project_dir}")
    print(f"字符数：{len(content)}")
    print(f"总行数：{stats['total']}")
    print(f"非空行数：{stats['non_empty']}")
    print(f"空行数：{stats['empty']}")
    print(f"文件名称：{','.join(file_names)}")
    for name, text in contents.items():
        stats = count_lines(text)
        print(f"\n文件名称：【{name}】")
        print(f"文件路径：{project_dir / 'data' / name}")
        print(f"字符数：{len(text)}")
        print(f"总行数：{stats['total']}")
        print(f"非空行数：{stats['non_empty']}")
        print(f"空行数：{stats['empty']}")
        print("文件内容：")
        print(text if text.strip() else "（空文件）")
    output_path = project_dir / "data" / "documents.json"
    try:
        save_documents(contents, output_path)
    except OSError as error:
        print(f"保存失败：{error}")
        return

    print(f"\n已保存到：{output_path}")
if __name__ == "__main__":
    main()