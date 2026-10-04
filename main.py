from pathlib import Path


def read_document(path: str) -> str:
    """读取 UTF-8 文本文件。"""
    file_path = Path(path)

    if not file_path.is_file():
        raise FileNotFoundError(f"找不到文件：{file_path}")

    return file_path.read_text(encoding="utf-8")


def main() -> None:
    project_dir = Path(__file__).resolve().parent
    document_path = project_dir /"ai-internship"/ "data" / "sample.txt"
    # print(document_path)
    # print(document_path.read_text(encoding="utf-8"))

    try:
        content = read_document(str(document_path))
    except (OSError, UnicodeError) as error:
        print(f"读取失败：{error}")
        return

    print("文档读取成功")
    print(f"字符数：{len(content)}")
    print(f"行数：{len(content.splitlines())}")
    print("内容预览：")
    print(content[:100])


if __name__ == "__main__":
    main()