package model

import "errors"

type Book struct {
	name    string
	url     string
	chapter int
	kind    Kind
	status  Status
}

func NewBook(
	name,
	url string,
	chapter int,
	kind Kind,
	status Status,
) (*Book, error) {
	if name == "" {
		return nil, errors.New("name must not be empty")
	}

	if url == "" {
		return nil, errors.New("url must not be empty")
	}

	if kind.IsNil() {
		return nil, errors.New("kind must not be empty")
	}

	if status.IsNil() {
		return nil, errors.New("status must not be empty")
	}

	return &Book{
		name:    name,
		url:     url,
		chapter: chapter,
		kind:    kind,
		status:  status,
	}, nil
}

func (b *Book) Name() string {
	return b.name
}

func (b *Book) URL() string {
	return b.url
}

func (b *Book) Chapter() int {
	return b.chapter
}

func (b *Book) Kind() Kind {
	return b.kind
}

func (b *Book) Status() Status {
	return b.status
}

func (b *Book) String() string {
	return b.name
}
