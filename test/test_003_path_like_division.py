# encoding: utf-8

from uri import URI


def test_issue_003_path_like_division_trailing():
	base = URI("http://example.com/foo/")
	assert str(base) == "http://example.com/foo/"
	assert str(base / "bar.html") == "http://example.com/foo/bar.html"
	
	base = URI("http://example.com/foo")
	assert str(base) == "http://example.com/foo"
	assert str(base / "bar.html") == "http://example.com/bar.html"


def test_issue_003_path_like_division_operators():
	base = URI("http://example.com/foo/bar.html")
	assert str(base / "baz.html") == 'http://example.com/foo/baz.html'
	assert str(base // "cdn.example.com" / "baz.html") == 'http://cdn.example.com/baz.html'
	assert str(base / "/diz") == 'http://example.com/diz'
	assert str(base / "#diz") == 'http://example.com/foo/bar.html#diz'
	assert str(base / "https://example.com") == 'https://example.com/'


def test_issue_003_path_on_path_division():
	base = URI("http://ats.example.com/job/listing")
	
	# scrape the listing, identify a job URL from that listing
	target = URI("detail/sample-job")  # oh no, it's relative!
	
	# And it's resolved.
	assert str(base / target) == "http://ats.example.com/job/detail/sample-job"
