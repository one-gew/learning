import json
from pathlib import Path

from main import search_chunks


BASE_DIR = Path(__file__).resolve().parent


def evaluate(cases: list[dict], chunks: list[dict], top_k: int = 3) -> dict:
    if top_k <= 0:
        raise ValueError("top_k 必须大于 0")

    answerable_total = 0
    hit_count = 0
    no_answer_total = 0
    empty_result_count = 0
    details = []

    for case in cases:
        query = case["query"]
        expected_sources = set(case["expected_sources"])
        results = search_chunks(query, chunks, top_k=top_k)
        actual_sources = {item["source"] for item in results}

        if expected_sources:
            answerable_total += 1
            # 多个期望来源表示：任意一个来源命中即可。
            passed = bool(expected_sources & actual_sources)
            if passed:
                hit_count += 1
            case_type = "有答案"
        else:
            no_answer_total += 1
            passed = len(results) == 0
            if passed:
                empty_result_count += 1
            case_type = "无匹配"

        details.append({
            "query": query,
            "case_type": case_type,
            "expected_sources": sorted(expected_sources),
            "actual_sources": sorted(actual_sources),
            "passed": passed,
            "results": results,
        })

    return {
        "top_k": top_k,
        "answerable_total": answerable_total,
        "hit_count": hit_count,
        "hit_rate": hit_count / answerable_total if answerable_total else None,
        "no_answer_total": no_answer_total,
        "empty_result_count": empty_result_count,
        "details": details,
    }


def main() -> None:
    cases = json.loads((BASE_DIR / "eval_queries.json").read_text(encoding="utf-8"))
    chunks = json.loads((BASE_DIR / "output" / "chunks.json").read_text(encoding="utf-8"))
    report = evaluate(cases, chunks, top_k=3)

    for item in report["details"]:
        status = "通过" if item["passed"] else "未通过"
        print(f"[{status}] {item['query']}")
        print(f"  期望来源：{item['expected_sources']}")
        for result in item["results"]:
            print(f"  实际：{result['source']}，块 {result['chunk_index']}，分数 {result['score']}")

    if report["hit_rate"] is None:
        print(f"Hit@{report['top_k']}：无有答案案例，暂不计算")
    else:
        print(f"Hit@{report['top_k']} = {report['hit_count']}/{report['answerable_total']} = {report['hit_rate']:.1%}")
    print(f"无匹配查询正确返回空列表：{report['empty_result_count']}/{report['no_answer_total']}")

    output_path = BASE_DIR / "output" / "eval_report.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"完整片段与评测记录已保存：{output_path}")


if __name__ == "__main__":
    main()
