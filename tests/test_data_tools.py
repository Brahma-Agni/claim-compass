from tools import download as download_tool
from tools.download import filename_for, read_urls, sha256


def test_download_helpers(tmp_path):
    url_file = tmp_path / "urls.txt"
    url_file.write_text("# official PDFs\n\nhttps://example.test/a%20file.pdf\n")

    assert read_urls(url_file) == ["https://example.test/a%20file.pdf"]
    assert filename_for("https://example.test/a%20file.pdf", {}) == "a-file.pdf"
    assert sha256(b"claim-compass") == "a7049cdf3f48623dc9bfb7fda6e04790703c0b9a13496e7f7f7143caf6d64577"


def test_changed_download_preserves_snapshot(tmp_path, monkeypatch):
    class Response:
        content = b"%PDF changed"

        @staticmethod
        def raise_for_status():
            return None

    url = "https://example.test/document.pdf"
    original = b"%PDF original"
    target = tmp_path / "document.pdf"
    target.write_bytes(original)
    rows = {url: {"local_filename": target.name, "sha256": sha256(original)}}
    monkeypatch.setattr(download_tool, "RAW_DIR", tmp_path)
    monkeypatch.setattr(download_tool, "robots_allows", lambda _: True)
    monkeypatch.setattr(download_tool.requests, "get", lambda *args, **kwargs: Response())

    message = download_tool.download(url, rows)

    assert target.read_bytes() == original
    assert "CHANGED upstream" in message
    assert next(tmp_path.glob("*.changed-*.pdf")).read_bytes() == Response.content
