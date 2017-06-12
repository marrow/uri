# encoding: utf-8


def test_issue_003_path_like_division_operators():
	from uri import URI
	
	base = URI("http://example.com/foo/")
	assert str(base) == "http://example.com/foo/"
	assert str(base / "bar.html") == "http://example.com/foo/bar.html"
	
	base = URI("http://example.com/foo")
	assert str(base) == "http://example.com/foo"
	assert str(base / "bar.html") == "http://example.com/bar.html"
	
	base = URI("http://example.com/foo/bar.html")
	assert str(base / "baz.html") == 'http://example.com/foo/baz.html'
	assert str(base // "cdn.example.com" / "baz.html") == 'http://cdn.example.com/baz.html'
	assert str(base / "/diz") == 'http://example.com/diz'
	assert str(base / "#diz") == 'http://example.com/foo/bar.html#diz'
	assert str(base / "https://example.com") == 'https://example.com/'
