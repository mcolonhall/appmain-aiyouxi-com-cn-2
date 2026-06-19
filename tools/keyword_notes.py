from dataclasses import dataclass, field
from typing import List, Optional
from datetime import datetime

SAMPLE_URL = "https://appmain-aiyouxi.com.cn"
SAMPLE_KEYWORD = "爱游戏"


@dataclass
class KeywordNote:
    """A note associated with a keyword and an optional URL."""
    keyword: str
    content: str
    url: Optional[str] = None
    tags: List[str] = field(default_factory=list)
    created_at: Optional[str] = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def short_summary(self, max_length: int = 40) -> str:
        if len(self.content) <= max_length:
            return self.content
        return self.content[:max_length] + "…"


@dataclass
class KeywordNoteCollection:
    """A collection of keyword notes with formatting utilities."""
    notes: List[KeywordNote] = field(default_factory=list)

    def add(self, note: KeywordNote) -> None:
        self.notes.append(note)

    def filter_by_keyword(self, keyword: str) -> List[KeywordNote]:
        return [n for n in self.notes if n.keyword == keyword]

    def filter_by_tag(self, tag: str) -> List[KeywordNote]:
        return [n for n in self.notes if tag in n.tags]

    def format_plain_text(self) -> str:
        lines = []
        for i, note in enumerate(self.notes, 1):
            lines.append(f"Note {i}")
            lines.append(f"  Keyword : {note.keyword}")
            lines.append(f"  Content : {note.content}")
            if note.url:
                lines.append(f"  URL     : {note.url}")
            if note.tags:
                lines.append(f"  Tags    : {', '.join(note.tags)}")
            lines.append(f"  Created : {note.created_at}")
            lines.append("")
        return "\n".join(lines).strip()

    def format_markdown(self) -> str:
        blocks = []
        for note in self.notes:
            keyword_line = f"## {note.keyword}"
            content_line = f"{note.content}"
            meta_parts = [f"_Created: {note.created_at}_"]
            if note.url:
                meta_parts.append(f"[Link]({note.url})")
            if note.tags:
                meta_parts.append("Tags: " + ", ".join(f"`{t}`" for t in note.tags))
            meta_line = " ".join(meta_parts)
            blocks.append(f"{keyword_line}\n\n{content_line}\n\n{meta_line}")
        return "\n\n---\n\n".join(blocks)

    def format_csv(self, delimiter: str = ",") -> str:
        header = delimiter.join(["keyword", "content", "url", "tags", "created_at"])
        rows = [header]
        for note in self.notes:
            tags_str = ";".join(note.tags)
            url_str = note.url if note.url else ""
            row = delimiter.join([
                note.keyword,
                note.content,
                url_str,
                tags_str,
                note.created_at,
            ])
            rows.append(row)
        return "\n".join(rows)


def build_sample_collection() -> KeywordNoteCollection:
    """Create a sample collection using the provided seed and default URL/keyword."""
    collection = KeywordNoteCollection()

    note1 = KeywordNote(
        keyword=SAMPLE_KEYWORD,
        content="爱游戏是一个专注于游戏资讯和社区互动的平台，涵盖最新游戏评测与攻略。",
        url=SAMPLE_URL,
        tags=["游戏", "资讯"],
    )
    note2 = KeywordNote(
        keyword="游戏攻略",
        content="在爱游戏平台可以找到大量热门游戏的详细攻略和隐藏成就解锁方法。",
        url=SAMPLE_URL,
        tags=["攻略", "成就"],
    )
    note3 = KeywordNote(
        keyword="社区动态",
        content="爱游戏社区每日更新玩家讨论、截图分享和赛事消息。",
        url=f"{SAMPLE_URL}/community",
        tags=["社区", "动态"],
    )
    note4 = KeywordNote(
        keyword="评测",
        content="爱游戏编辑团队提供客观公正的游戏评分和深度评测文章。",
        tags=["评测", "专业"],
    )

    collection.add(note1)
    collection.add(note2)
    collection.add(note3)
    collection.add(note4)
    return collection


def main() -> None:
    collection = build_sample_collection()

    print("=== Plain Text Output ===")
    print(collection.format_plain_text())

    print("\n=== Markdown Output ===")
    print(collection.format_markdown())

    print("\n=== CSV Output ===")
    print(collection.format_csv())

    print("\n=== Filtered by keyword '爱游戏' ===")
    filtered = collection.filter_by_keyword(SAMPLE_KEYWORD)
    for note in filtered:
        print(f"  - {note.short_summary(30)}")

    print("\n=== Filtered by tag '攻略' ===")
    filtered = collection.filter_by_tag("攻略")
    for note in filtered:
        print(f"  - {note.short_summary(30)}")


if __name__ == "__main__":
    main()