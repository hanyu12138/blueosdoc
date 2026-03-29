from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import sys
import time
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import asdict, dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, urlencode, urljoin, urlsplit, urlunsplit

try:
    import requests
    from requests.adapters import HTTPAdapter
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少 requests 依赖，请先执行: pip install requests") from exc

try:
    from urllib3.util.retry import Retry
except ImportError as exc:  # pragma: no cover
    raise SystemExit("缺少 urllib3 依赖，requests 通常会自带 urllib3") from exc


BASE_DOC_URL = "https://developers-watch.vivo.com.cn"
DOC_HOST = urlsplit(BASE_DOC_URL).netloc
QUERY_FLAG = ("hastopwindow", "1")
QUICKAPP_PREFIXES = ("/reference/", "/component/", "/api/", "/native/")
QUICKAPP_SEEDS = (
    "/reference/quickstart/introduction/",
    "/component/common/rule/",
    "/api/system/app/",
    "/native/quickstart/introduction/",
)
ASSET_EXTENSIONS = {
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".svg",
    ".webp",
    ".bmp",
    ".ico",
    ".avif",
    ".mp4",
    ".webm",
    ".pdf",
}
HREF_RE = re.compile(r'href=(?P<quote>["\'])(?P<value>.*?)(?P=quote)', re.IGNORECASE | re.DOTALL)
BODY_RE = re.compile(r"<body[^>]*>(?P<body>.*)</body>\s*</html>\s*$", re.IGNORECASE | re.DOTALL)
UPDATE_TIME_RE = re.compile(
    r'<p[^>]*class=(["\'])update-time\1[^>]*>.*?<time[^>]*datetime=(["\'])(?P<time>.*?)\2',
    re.IGNORECASE | re.DOTALL,
)
PAGE_PATH_RE = re.compile(r'window\.pagePath="(?P<path>[^"]+)"')
WHITESPACE_RE = re.compile(r"\s+")
TAG_RE = re.compile(r"<[^>]+>")


@dataclass
class PageRecord:
    path: str
    title: str
    source_url: str
    local_path: str
    update_time: str | None
    links: list[str]
    assets: list[str]


@dataclass
class Node:
    tag: str | None
    attrs: dict[str, str] = field(default_factory=dict)
    children: list["Node"] = field(default_factory=list)
    text: str = ""

    @property
    def classes(self) -> set[str]:
        value = self.attrs.get("class", "")
        return {item for item in value.split() if item}


class DivInnerHTMLExtractor(HTMLParser):
    def __init__(self, target_class: str) -> None:
        super().__init__(convert_charrefs=False)
        self.target_class = target_class
        self.parts: list[str] = []
        self.div_depth = 0
        self.capture_depth: int | None = None

    def extract(self, text: str) -> str:
        self.parts.clear()
        self.div_depth = 0
        self.capture_depth = None
        self.feed(text)
        self.close()
        return "".join(self.parts)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "div":
            self.div_depth += 1
            class_attr = dict(attrs).get("class") or ""
            classes = class_attr.split()
            if self.capture_depth is None and self.target_class in classes:
                self.capture_depth = self.div_depth
                return
        if self.capture_depth is not None:
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if self.capture_depth is not None:
            self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        if self.capture_depth is not None:
            if tag == "div" and self.div_depth == self.capture_depth:
                self.capture_depth = None
                self.div_depth -= 1
                return
            self.parts.append(f"</{tag}>")
        if tag == "div":
            self.div_depth -= 1

    def handle_data(self, data: str) -> None:
        if self.capture_depth is not None:
            self.parts.append(data)

    def handle_comment(self, data: str) -> None:
        if self.capture_depth is not None:
            self.parts.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        if self.capture_depth is not None:
            self.parts.append(f"<!{decl}>")

    def handle_entityref(self, name: str) -> None:
        if self.capture_depth is not None:
            self.parts.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        if self.capture_depth is not None:
            self.parts.append(f"&#{name};")


class DOMBuilder(HTMLParser):
    VOID_TAGS = {"br", "hr", "img", "input", "meta", "link"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.root = Node(tag="document")
        self.stack = [self.root]

    def parse(self, text: str) -> Node:
        self.root = Node(tag="document")
        self.stack = [self.root]
        self.feed(text)
        self.close()
        return self.root

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag=tag.lower(), attrs={k: v or "" for k, v in attrs})
        self.stack[-1].children.append(node)
        if tag.lower() not in self.VOID_TAGS:
            self.stack.append(node)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        node = Node(tag=tag.lower(), attrs={k: v or "" for k, v in attrs})
        self.stack[-1].children.append(node)

    def handle_endtag(self, tag: str) -> None:
        target = tag.lower()
        for index in range(len(self.stack) - 1, 0, -1):
            if self.stack[index].tag == target:
                del self.stack[index:]
                break

    def handle_data(self, data: str) -> None:
        if data:
            self.stack[-1].children.append(Node(tag=None, text=data))

    def handle_entityref(self, name: str) -> None:
        self.handle_data(html.unescape(f"&{name};"))

    def handle_charref(self, name: str) -> None:
        self.handle_data(html.unescape(f"&#{name};"))


class MarkdownRenderer:
    INLINE_BREAK = "<br>"
    SKIP_BLOCK_CLASSES = {
        "warp-content",
        "copy-code-button",
        "copy-button",
        "page-nav",
        "toc",
    }
    SKIP_INLINE_CLASSES = {"anchor"}
    BLOCK_TAGS = {
        "document",
        "html",
        "body",
        "main",
        "article",
        "section",
        "div",
        "p",
        "pre",
        "blockquote",
        "ul",
        "ol",
        "li",
        "table",
        "thead",
        "tbody",
        "tfoot",
        "tr",
        "th",
        "td",
        "h1",
        "h2",
        "h3",
        "h4",
        "h5",
        "h6",
        "hr",
    }

    def __init__(
        self,
        output_dir: Path,
        current_path: str,
        current_url: str,
        asset_map: dict[str, Path],
        allowed_prefixes: tuple[str, ...],
    ) -> None:
        self.output_dir = output_dir
        self.current_path = current_path
        self.current_url = current_url
        self.asset_map = asset_map
        self.allowed_prefixes = allowed_prefixes
        self.current_file = local_page_path(output_dir, current_path)

    def render(self, html_text: str) -> str:
        root = DOMBuilder().parse(html_text)
        body = self.find_body(root) or root
        markdown = self.render_blocks(body.children).strip()
        markdown = re.sub(r"\n{3,}", "\n\n", markdown)
        return markdown + "\n"

    def find_body(self, node: Node) -> Node | None:
        if node.tag == "body":
            return node
        for child in node.children:
            found = self.find_body(child)
            if found is not None:
                return found
        return None

    def render_blocks(self, nodes: Iterable[Node], list_depth: int = 0) -> str:
        parts: list[str] = []
        for node in nodes:
            block = self.render_block(node, list_depth=list_depth)
            if block:
                parts.append(block)
        text = "".join(parts)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    def render_block(self, node: Node, list_depth: int = 0) -> str:
        if node.tag is None:
            text = collapse_ws(node.text)
            return f"{text}\n\n" if text.strip() else ""

        if self.should_skip_block(node):
            return ""

        tag = node.tag
        if tag in {"html", "body", "main", "article", "section", "document"}:
            return self.render_blocks(node.children, list_depth=list_depth)

        if tag == "div":
            highlight = self.render_highlight_block(node)
            if highlight is not None:
                return highlight
            return self.render_blocks(node.children, list_depth=list_depth)

        if tag == "p":
            if "update-time" in node.classes:
                return ""
            content = self.render_inlines(node.children).strip()
            return f"{content}\n\n" if content else ""

        if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
            level = int(tag[1])
            content = normalize_heading_text(self.render_inlines(node.children))
            return f"{'#' * level} {content}\n\n" if content else ""

        if tag == "pre":
            code_node = self.find_first_descendant(node, "code")
            code_text = extract_text_preserve(code_node or node).rstrip("\n")
            language = detect_code_language(code_node or node)
            return f"```{language}\n{code_text}\n```\n\n"

        if tag == "blockquote":
            inner = self.render_blocks(node.children).strip()
            if not inner:
                inner = self.render_inlines(node.children).strip()
            if not inner:
                return ""
            lines = [f"> {line}" if line else ">" for line in inner.splitlines()]
            return "\n".join(lines) + "\n\n"

        if tag == "ul":
            return self.render_list(node, ordered=False, depth=list_depth) + "\n"

        if tag == "ol":
            return self.render_list(node, ordered=True, depth=list_depth) + "\n"

        if tag == "table":
            return self.render_table(node) + "\n\n"

        if tag == "hr":
            return "---\n\n"

        if tag == "img":
            image = self.render_image(node)
            return f"{image}\n\n" if image else ""

        if tag == "br":
            return "\n"

        return self.render_blocks(node.children, list_depth=list_depth)

    def render_list(self, node: Node, ordered: bool, depth: int) -> str:
        items = [child for child in node.children if child.tag == "li"]
        parts: list[str] = []
        for index, item in enumerate(items, start=1):
            prefix = f"{index}. " if ordered else "- "
            parts.append(self.render_list_item(item, prefix, depth))
        return "".join(parts).rstrip("\n")

    def render_list_item(self, node: Node, prefix: str, depth: int) -> str:
        inline_nodes: list[Node] = []
        child_blocks: list[str] = []
        nested_lists: list[str] = []

        for child in node.children:
            if child.tag in {"ul", "ol"}:
                nested_lists.append(self.render_list(child, ordered=child.tag == "ol", depth=depth + 1))
            elif child.tag in {"pre", "table", "blockquote"}:
                rendered = self.render_block(child, list_depth=depth + 1).strip("\n")
                if rendered:
                    child_blocks.append(indent_text(rendered, "  " * (depth + 1)))
            elif child.tag == "p":
                inline_nodes.extend(child.children)
            else:
                inline_nodes.append(child)

        marker = ("  " * depth) + prefix
        line = self.render_inlines(inline_nodes).strip()
        output = marker + line + "\n" if line else marker.rstrip() + "\n"

        for block in child_blocks:
            output += block + "\n"
        for nested in nested_lists:
            output += nested + "\n"
        return output

    def render_table(self, node: Node) -> str:
        rows = self.collect_table_rows(node)
        if not rows:
            return ""

        width = max(len(row) for row in rows)
        normalized_rows = [row + ["-"] * (width - len(row)) for row in rows]

        header = normalized_rows[0]
        body = normalized_rows[1:] if len(normalized_rows) > 1 else []
        header_line = "| " + " | ".join(header) + " |"
        divider = "| " + " | ".join(["---"] * len(header)) + " |"
        lines = [header_line, divider]
        for row in body:
            lines.append("| " + " | ".join(row[: len(header)]) + " |")
        return "\n".join(lines)

    def collect_table_rows(self, node: Node) -> list[list[str]]:
        rows = collect_descendants(node, "tr")
        result: list[list[str]] = []
        for row in rows:
            cells = [cell for cell in row.children if cell.tag in {"th", "td"}]
            if not cells:
                cells = collect_descendants(row, "th") + collect_descendants(row, "td")
            rendered: list[str] = []
            for cell in cells:
                text = self.normalize_table_cell(self.render_inlines(cell.children))
                rendered.append(text)
            if rendered:
                result.append(rendered)
        return result

    def render_inlines(self, nodes: Iterable[Node]) -> str:
        parts: list[str] = []
        for node in nodes:
            parts.append(self.render_inline(node))
        text = "".join(parts)
        text = re.sub(r"[ \t]+\n", "\n", text)
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text

    def render_inline(self, node: Node) -> str:
        if node.tag is None:
            return collapse_ws(node.text)

        if self.should_skip_inline(node):
            return ""

        tag = node.tag
        if tag == "br":
            return self.INLINE_BREAK

        if tag == "a":
            href = node.attrs.get("href", "").strip()
            text = self.render_inlines(node.children).strip()
            rewritten = self.rewrite_target(href)
            if not text:
                return rewritten or ""
            return f"[{escape_md_text(text)}]({rewritten})" if rewritten else escape_md_text(text)

        if tag == "img":
            return self.render_image(node)

        if tag in {"strong", "b"}:
            text = self.render_inlines(node.children).strip()
            return f"**{text}**" if text else ""

        if tag in {"em", "i"}:
            text = self.render_inlines(node.children).strip()
            return f"*{text}*" if text else ""

        if tag in {"del", "s"}:
            text = self.render_inlines(node.children).strip()
            return f"~~{text}~~" if text else ""

        if tag == "code":
            text = extract_text_preserve(node).strip()
            if not text:
                return ""
            escaped = text.replace("`", "\\`")
            return f"`{escaped}`"

        if tag in {"svg", "path", "head", "script", "style"}:
            return ""

        if tag in {"span", "div", "time", "small", "sup", "sub"}:
            return self.render_inlines(node.children)

        return self.render_inlines(node.children)

    def render_image(self, node: Node) -> str:
        src = node.attrs.get("src", "").strip()
        if not src:
            return ""
        rewritten = self.rewrite_target(src)
        alt = escape_md_text(node.attrs.get("alt", "").strip())
        return f"![{alt}]({rewritten})" if rewritten else ""

    def rewrite_target(self, raw_value: str) -> str:
        if not raw_value or raw_value.startswith(("data:", "javascript:", "mailto:", "tel:")):
            return raw_value

        absolute = urljoin(self.current_url, raw_value)
        parsed = urlsplit(absolute)

        doc_path = normalize_doc_path(absolute, self.allowed_prefixes)
        if doc_path:
            target_file = local_page_path(self.output_dir, doc_path)
            result = relative_link(self.current_file, target_file)
            if parsed.fragment:
                result += f"#{parsed.fragment}"
            return result

        asset_key = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
        if asset_key in self.asset_map:
            result = relative_link(self.current_file, self.asset_map[asset_key])
            if parsed.fragment:
                result += f"#{parsed.fragment}"
            return result

        if parsed.scheme in {"http", "https"}:
            return absolute
        return raw_value

    def find_first_descendant(self, node: Node, tag: str) -> Node | None:
        for child in node.children:
            if child.tag == tag:
                return child
            found = self.find_first_descendant(child, tag)
            if found is not None:
                return found
        return None

    def should_skip_block(self, node: Node) -> bool:
        return bool(node.classes & self.SKIP_BLOCK_CLASSES)

    def should_skip_inline(self, node: Node) -> bool:
        return bool(node.classes & self.SKIP_INLINE_CLASSES)

    def render_highlight_block(self, node: Node) -> str | None:
        has_wrapper_hint = (
            "gatsby-highlight" in node.classes
            or bool(node.attrs.get("data-language", "").strip())
            or any(item.startswith("language-") for item in node.classes)
        )
        if not has_wrapper_hint:
            return None

        pre_node = self.find_first_descendant(node, "pre")
        if pre_node is None:
            return None

        code_node = self.find_first_descendant(pre_node, "code")
        code_text = extract_text_preserve(code_node or pre_node).strip("\n")
        language = detect_code_language(code_node or pre_node)
        if not language:
            language = detect_code_language(node)
        if not language:
            language = node.attrs.get("data-language", "").strip()
        return f"```{language}\n{code_text}\n```\n\n"

    def normalize_table_cell(self, text: str) -> str:
        text = text.replace("\xa0", " ")
        text = re.sub(r"\s*<br>\s*", self.INLINE_BREAK, text)
        text = re.sub(r"[ \t\r\f\v]+", " ", text)
        text = re.sub(r"\n+", " ", text)
        text = re.sub(r" +", " ", text).strip()
        text = text.replace("|", r"\|")
        return text or "-"


def collapse_ws(text: str) -> str:
    if not text:
        return ""
    return WHITESPACE_RE.sub(" ", text)


def strip_tags(text: str) -> str:
    return html.unescape(WHITESPACE_RE.sub(" ", TAG_RE.sub("", text))).strip()


def escape_md_text(text: str) -> str:
    return text.replace("\n", " ").strip()


def normalize_heading_text(text: str) -> str:
    if not text:
        return ""
    text = text.replace("<br>", " ")
    return WHITESPACE_RE.sub(" ", text).strip()


def indent_text(text: str, prefix: str) -> str:
    return "\n".join(prefix + line if line else line for line in text.splitlines())


def detect_code_language(node: Node) -> str:
    class_value = node.attrs.get("class", "")
    for item in class_value.split():
        if item.startswith("language-"):
            return item.removeprefix("language-")
    return ""


def clean_markdown(text: str) -> str:
    text = re.sub(r"^\s*复制代码\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^\s*Copy code\s*$", "", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s+#\s+(.*)$", r"## \1", text, flags=re.MULTILINE)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip() + "\n"


def extract_text_preserve(node: Node) -> str:
    if node.tag is None:
        return node.text
    if node.tag == "br":
        return "\n"
    return "".join(extract_text_preserve(child) for child in node.children)


def collect_descendants(node: Node, tag: str) -> list[Node]:
    matches: list[Node] = []
    for child in node.children:
        if child.tag == tag:
            matches.append(child)
        matches.extend(collect_descendants(child, tag))
    return matches


def normalize_doc_path(path_or_url: str, allowed_prefixes: tuple[str, ...]) -> str | None:
    if not path_or_url:
        return None
    full_url = urljoin(BASE_DOC_URL, path_or_url)
    parsed = urlsplit(full_url)
    if parsed.scheme not in {"http", "https"}:
        return None
    if parsed.netloc != DOC_HOST:
        return None
    path = re.sub(r"/{2,}", "/", parsed.path or "/")
    if not path.startswith(allowed_prefixes):
        return None
    if not path.endswith("/"):
        path += "/"
    return path


def build_fetch_url(path: str) -> str:
    parsed = urlsplit(urljoin(BASE_DOC_URL, path))
    query_pairs = [(key, value) for key, value in parse_qsl(parsed.query, keep_blank_values=True) if key != QUERY_FLAG[0]]
    query_pairs.append(QUERY_FLAG)
    return urlunsplit((parsed.scheme, parsed.netloc, parsed.path, urlencode(query_pairs), ""))


def make_session() -> requests.Session:
    session = requests.Session()
    session.trust_env = False
    session.headers.update(
        {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Cache-Control": "no-cache",
        }
    )

    retry_strategy = Retry(
        total=3,
        connect=3,
        read=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy, pool_connections=20, pool_maxsize=20)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def fetch_text(session: requests.Session, url: str, timeout: float, retries: int = 3) -> tuple[str, str]:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.text, response.url
        except requests.RequestException as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(2 ** (attempt - 1), 4))
    assert last_error is not None
    raise last_error


def fetch_bytes(session: requests.Session, url: str, timeout: float, retries: int = 3) -> bytes:
    last_error: Exception | None = None
    for attempt in range(1, retries + 1):
        try:
            response = session.get(url, timeout=timeout)
            response.raise_for_status()
            return response.content
        except requests.RequestException as exc:
            last_error = exc
            if attempt == retries:
                break
            time.sleep(min(2 ** (attempt - 1), 4))
    assert last_error is not None
    raise last_error


def is_not_found_page(final_url: str, html_text: str) -> bool:
    path = urlsplit(final_url).path.rstrip("/")
    if path.endswith("/404"):
        return True
    match = PAGE_PATH_RE.search(html_text)
    return bool(match and match.group("path").rstrip("/") == "/404")


def extract_body_html(fragment: str) -> str:
    match = BODY_RE.search(fragment)
    return match.group("body") if match else fragment


def extract_title(content_html: str, fallback_path: str) -> str:
    root = DOMBuilder().parse(content_html)
    body = root
    renderer = MarkdownRenderer(Path("."), "/", BASE_DOC_URL, {}, QUICKAPP_PREFIXES)
    for node in body.children:
        found = find_heading(node, "h1")
        if found:
            title = normalize_heading_text(renderer.render_inlines(found.children))
            if title:
                return title
    return fallback_path.rstrip("/").split("/")[-1] or "BlueOS 快应用文档"


def find_heading(node: Node, tag: str) -> Node | None:
    if node.tag == tag:
        return node
    for child in node.children:
        found = find_heading(child, tag)
        if found is not None:
            return found
    return None


def extract_update_time(content_html: str) -> str | None:
    match = UPDATE_TIME_RE.search(content_html)
    if match:
        return html.unescape(match.group("time")).strip()
    return None


def extract_doc_links(html_text: str, page_url: str, allowed_prefixes: tuple[str, ...]) -> list[str]:
    links: set[str] = set()
    for match in HREF_RE.finditer(html_text):
        raw_value = html.unescape(match.group("value").strip())
        doc_path = normalize_doc_path(urljoin(page_url, raw_value), allowed_prefixes)
        if doc_path:
            links.add(doc_path)
    return sorted(links)


def is_asset_link(url: str) -> bool:
    path = urlsplit(url).path.lower()
    return any(path.endswith(ext) for ext in ASSET_EXTENSIONS)


def extract_asset_urls(content_html: str, page_url: str) -> list[str]:
    urls: set[str] = set()
    root = DOMBuilder().parse(content_html)
    for node in iter_nodes(root):
        if node.tag not in {"a", "img"}:
            continue
        key = "href" if node.tag == "a" else "src"
        raw_value = node.attrs.get(key, "").strip()
        if not raw_value or raw_value.startswith(("data:", "#", "javascript:", "mailto:", "tel:")):
            continue
        absolute = urljoin(page_url, raw_value)
        parsed = urlsplit(absolute)
        absolute = urlunsplit((parsed.scheme, parsed.netloc, parsed.path, parsed.query, ""))
        if parsed.scheme in {"http", "https"} and is_asset_link(absolute):
            urls.add(absolute)
    return sorted(urls)


def iter_nodes(node: Node) -> Iterable[Node]:
    yield node
    for child in node.children:
        yield from iter_nodes(child)


def local_page_path(output_dir: Path, doc_path: str) -> Path:
    return output_dir / doc_path.strip("/") / "index.md"


def local_asset_path(output_dir: Path, asset_url: str) -> Path:
    parsed = urlsplit(asset_url)
    target = output_dir / "_assets" / parsed.netloc / parsed.path.lstrip("/")
    if not target.suffix:
        target = target.with_name(f"{target.name or 'asset'}.bin")
    if parsed.query:
        digest = hashlib.sha1(parsed.query.encode("utf-8")).hexdigest()[:10]
        target = target.with_name(f"{target.stem}-{digest}{target.suffix}")
    return target


def relative_link(from_file: Path, to_file: Path) -> str:
    return os.path.relpath(to_file, start=from_file.parent).replace(os.sep, "/")


def render_page_markdown(
    title: str,
    source_url: str,
    update_time: str | None,
    content_html: str,
    output_dir: Path,
    page_path: str,
    asset_map: dict[str, Path],
    allowed_prefixes: tuple[str, ...],
) -> str:
    renderer = MarkdownRenderer(
        output_dir=output_dir,
        current_path=page_path,
        current_url=build_fetch_url(page_path),
        asset_map=asset_map,
        allowed_prefixes=allowed_prefixes,
    )
    body = renderer.render(content_html).strip()

    meta_lines = [f"> 来源：[{source_url}]({source_url})"]
    if update_time:
        meta_lines.append(f"> 更新时间：{update_time}")

    if not body.startswith("# "):
        body = f"# {title}\n\n{body}"

    return clean_markdown("\n".join(meta_lines) + "\n\n" + body + "\n")


def save_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def save_bytes(path: Path, content: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content)


def crawl(args: argparse.Namespace) -> int:
    output_dir = Path(args.output).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    extractor = DivInnerHTMLExtractor("html-content")
    session = make_session()
    allowed_prefixes = QUICKAPP_PREFIXES
    raw_seeds = args.seed if args.seed else list(QUICKAPP_SEEDS)

    queue: deque[str] = deque()
    for seed in raw_seeds:
        doc_path = normalize_doc_path(seed, allowed_prefixes)
        if doc_path:
            queue.append(doc_path)

    visited: set[str] = set()
    pages: dict[str, PageRecord] = {}
    errors: list[dict[str, str]] = []

    while queue:
        page_path = queue.popleft()
        if page_path in visited:
            continue
        if args.max_pages and len(visited) >= args.max_pages:
            break

        visited.add(page_path)
        fetch_url = build_fetch_url(page_path)
        print(f"[抓取] {page_path}")

        try:
            html_text, final_url = fetch_text(session, fetch_url, timeout=args.timeout)
        except Exception as exc:
            errors.append({"path": page_path, "error": str(exc)})
            print(f"[失败] {page_path} -> {exc}", file=sys.stderr)
            continue

        if is_not_found_page(final_url, html_text):
            errors.append({"path": page_path, "error": "页面不存在或已重定向到 404"})
            print(f"[跳过] {page_path} -> 404", file=sys.stderr)
            continue

        discovered_links = extract_doc_links(html_text, final_url, allowed_prefixes)
        for discovered in discovered_links:
            if discovered not in visited:
                queue.append(discovered)

        fragment = extractor.extract(html_text)
        if not fragment:
            errors.append({"path": page_path, "error": "未找到 html-content 正文容器"})
            print(f"[失败] {page_path} -> 未找到正文容器", file=sys.stderr)
            continue

        body_html = extract_body_html(fragment)
        title = extract_title(body_html, page_path)
        update_time = extract_update_time(body_html)
        source_url = urlunsplit(
            (urlsplit(final_url).scheme, urlsplit(final_url).netloc, urlsplit(final_url).path, "", "")
        )

        asset_map: dict[str, Path] = {}
        if not args.skip_assets:
            for asset_url in extract_asset_urls(body_html, final_url):
                target_path = local_asset_path(output_dir, asset_url)
                if not target_path.exists():
                    try:
                        content = fetch_bytes(session, asset_url, timeout=args.timeout)
                        save_bytes(target_path, content)
                    except Exception as exc:
                        errors.append({"path": page_path, "error": f"资源下载失败: {asset_url} -> {exc}"})
                        print(f"[资源失败] {asset_url} -> {exc}", file=sys.stderr)
                        continue
                asset_map[asset_url] = target_path

        markdown = render_page_markdown(
            title=title,
            source_url=source_url,
            update_time=update_time,
            content_html=body_html,
            output_dir=output_dir,
            page_path=page_path,
            asset_map=asset_map,
            allowed_prefixes=allowed_prefixes,
        )
        local_file = local_page_path(output_dir, page_path)
        save_text(local_file, markdown)

        pages[page_path] = PageRecord(
            path=page_path,
            title=title,
            source_url=source_url,
            local_path=local_file.relative_to(output_dir).as_posix(),
            update_time=update_time,
            links=discovered_links,
            assets=sorted(path.relative_to(output_dir).as_posix() for path in asset_map.values()),
        )

        if args.delay > 0:
            time.sleep(args.delay)

    manifest = {
        "base_url": BASE_DOC_URL,
        "doc_scope": "blueos-common-docs",
        "output_format": "markdown",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "page_count": len(pages),
        "error_count": len(errors),
        "pages": [asdict(pages[key]) for key in sorted(pages)],
        "errors": errors,
    }
    save_text(output_dir / "manifest.json", json.dumps(manifest, ensure_ascii=False, indent=2))

    print(f"[完成] 成功保存 {len(pages)} 篇 Markdown 文档到: {output_dir}")
    if errors:
        print(f"[提示] 共有 {len(errors)} 个失败项，详情见: {output_dir / 'manifest.json'}", file=sys.stderr)
    return 0 if pages else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="抓取 BlueOS 快应用开发文档并保存为 Markdown。")
    parser.add_argument(
        "-o",
        "--output",
        default="docs",
        help="输出目录，默认: docs",
    )
    parser.add_argument(
        "--seed",
        action="append",
        help="自定义起始页面，可传相对路径或完整 URL，可重复传入。",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=0,
        help="最多抓取多少篇页面，0 表示不限。",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=0.2,
        help="每次请求后的延时秒数，默认: 0.2",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="单次请求超时时间（秒），默认: 30",
    )
    parser.add_argument(
        "--skip-assets",
        action="store_true",
        help="只抓页面正文，不下载图片等资源文件。",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return crawl(args)


if __name__ == "__main__":
    raise SystemExit(main())
