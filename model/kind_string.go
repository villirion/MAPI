// Code generated by "stringer -type=Kind -linecomment"; DO NOT EDIT.

package model

import "strconv"

func _() {
	// An "invalid array index" compiler error signifies that the constant values have changed.
	// Re-run the stringer command to generate them again.
	var x [1]struct{}
	_ = x[KindUnknown-0]
	_ = x[KindManhwa-1]
	_ = x[KindManga-2]
}

const _Kind_name = "unknownmanhwamanga"

var _Kind_index = [...]uint8{0, 7, 13, 18}

func (i Kind) String() string {
	if i < 0 || i >= Kind(len(_Kind_index)-1) {
		return "Kind(" + strconv.FormatInt(int64(i), 10) + ")"
	}
	return _Kind_name[_Kind_index[i]:_Kind_index[i+1]]
}
