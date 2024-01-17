package model

import "errors"

type Kind int

//go:generate stringer -type=Kind -linecomment
const (
	KindUnknown Kind = iota // unknown
	KindManhwa              // manhwa
	KindManga               // manga
)

func NewKind(kind string) (Kind, error) {
	switch kind {
	case KindUnknown.String():
		return KindUnknown, nil
	case KindManhwa.String():
		return KindManhwa, nil
	case KindManga.String():
		return KindManga, nil
	default:
		return KindUnknown, errors.New("Kind not supported")
	}
}

func (k Kind) IsNil() bool {
	return k == KindUnknown
}
