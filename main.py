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
        # 空文本直接返回
        if not text:
            print(f"跳过空文档：{source}")
            continue

        for index, chunk in enumerate(split_text(text)):
            chunks.append({
                "source": source,
                "chunk_index": index,       # 从 0 开始
                "content": chunk,
            })

    return chunks
def search_chunks(
        query: str,
        chunks: list[dict],
        top_k: int = 3,
)->list[dict]:
   keywords = []
   for word in query.split():
       if word and word not in keywords:
           keywords.append(word)
   scored = []
   for chunk in (chunks):
       content = chunk["content"]
       score = 0
       for word in keywords:
           if word in content:
                score += 1
       if score > 0:
           scored.append((score,chunk))
   scored.sort(key=lambda x: (-x[0], x[1]["source"], x[1]["chunk_index"]))
   results = []
   for score, chunk in scored[:top_k]:
       item = {**chunk, "score": score}  # 复制 chunk，加 score
       results.append(item)
   return results

def main() -> None:
    # 文档路径
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
        save_documents(documents, documents_path)
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

    query = input("请输入查询：").strip()
    # query = "台灯 保修"
    if not query:
        print("查询不能为空！")
        return
    raw = input("请输入返回条数：").strip()
    try:
        top_k = int(raw)
    except ValueError:
        print(f"输入无效：{raw!r} 不是整数")
        return

    if top_k < 0:
        print(f"top_k 不能为负数，收到 {top_k}")
        return
    result =  search_chunks(query, chunks,top_k)
    if not result:
        print("查询结果为空！")
    else:
        print(f"找到了{len(result)}条查询结果：")
        for i, r in enumerate(result,start=1):
            print(f"\n{i}. 来源：{r['source']}（第 {r['chunk_index']} 块）\n   得分为{r['score']}")
            print(f"   {r['content']}")


if __name__ == "__main__":
    main()