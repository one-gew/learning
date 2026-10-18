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

# def load_documents(project_dir:Path,file_names:list[str])->dict[str,str]:
#     contents = {}
#     for file_name in file_names:
#         file_path = project_dir / 'data' / file_name
#         if not file_path.is_file():
#             print(f"文件不存在：{file_path}")
#             continue
#         try:
#             content = read_document(str(file_path))
#         except (OSError, UnicodeError) as error:
#             print(f"读取失败：{file_path}（{error}")
#             continue
#         contents[file_name] = content
#     return contents
def load_documents(folder: Path) -> list[dict]:
    documents = []

    for file_path in sorted(folder.glob("*.txt")):
        if not file_path.is_file():
            continue

        try:
            content = read_document(str(file_path))
        except (OSError, UnicodeError) as error:
            print(f"读取失败：{file_path}（{error}）")
            continue
        stats = count_lines(content)

        documents.append({
            "source": file_path.name,
            "content": content,
            "char_count": len(content),
            "line_count": stats["total"],
            "non_empty_lines": stats["non_empty"],
        })

    return documents

def load_documents_v1(project_dir:Path)->list[dict]:
    path = project_dir.glob('*.txt')

def save_documents(contents: dict[str, str], output_path: Path) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(contents, f, ensure_ascii=False, indent=2)

def split_text(
    text: str,
    chunk_size: int = 100,
    overlap: int = 20,
) -> list[str]:
    if chunk_size <= 0:
        raise ValueError(f"chunk_size 必须大于 0，收到 {chunk_size}")
    if not (0 <= overlap < chunk_size):
        raise ValueError(
            f"overlap 必须满足 0 <= overlap < chunk_size，收到 overlap={overlap}, chunk_size={chunk_size}"
        )

    # ② 空文本直接返回
    if not text:
        return []

    chunks = []
    start = 0
    step = chunk_size - overlap          # 每次前进的步长

    while start < len(text):
        end = start + chunk_size         # 最多取 chunk_size 个字符
        chunk = text[start:end]          # 切片自动处理"不足一块"的情况
        chunks.append(chunk)

        if end >= len(text):
            break

        start += step

    return chunks
def build_chunks(documents: list[dict]) -> list[dict]:
    chunks = []

    for document in documents:
        source = document["source"]
        text = document["content"]

        for index, chunk in enumerate(split_text(text)):
            chunks.append({
                "source": source,
                "chunk_index": index,       # 从 0 开始
                "content": chunk,
            })

    return chunks
def main() -> None:
    # 文档路径
    global contents
    project_dir = Path(__file__).resolve().parent
    data_dir = project_dir / "data"
    output_dir = project_dir / "output"
    # print(document_path)
    # print(document_path.read_text(encoding="utf-8"))
    # 读文档
    try:
        documents = load_documents(data_dir)
    except (OSError, UnicodeError) as error:
        print(f"加载失败：{error}")
        return
    # 行数统计
    print(f"共加载 {len(documents)} 份文档：")
    for doc in documents:
        print(f"  【{doc['source']}】字符 {doc['char_count']}，"
              f"总行 {doc['line_count']}，非空行 {doc['non_empty_lines']}")
    # 文件查找
    try:
        file_names = find_txt_file(project_dir)
    except (OSError, UnicodeError) as error:
        print(f"查找失败：{error}")
        return
    chunks = build_chunks(documents)
    print(f"共生成 {len(chunks)} 个分块")

    # 3. 保存到 output/
    documents_path = output_dir / "documents.json"
    chunks_path = output_dir / "chunks.json"

    try:
        save_documents(documents, documents_path)  # 复用你的保存函数（改成存 list）
        save_documents(chunks, chunks_path)
    except OSError as error:
        print(f"保存失败：{error}")
        return

    print(f"已保存：{documents_path}")
    print(f"已保存：{chunks_path}")

    # 4. 用 json.loads() 读回，检查是否与 documents 相等
    try:
        raw = documents_path.read_text(encoding="utf-8")
        loaded = json.loads(raw)
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print(f"读回失败：{error}")
        return

    if loaded == documents:
        print("SON 读回与内存中的 documents 完全一致")
    else:
        print("读回结果与 documents 不一致")


if __name__ == "__main__":
    main()