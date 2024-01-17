package model

import "errors"

type Status int

//go:generate stringer -type=Status -linecomment
const (
	StatusUnknown Status = iota // unknown
	StatusEnded                 // ended
	StatusReading               // reading
	StatusDrop                  // drop
	StatusOnHold                // onHold
)

func NewStatus(status string) (Status, error) {
	switch status {
	case StatusUnknown.String():
		return StatusUnknown, nil
	case StatusEnded.String():
		return StatusEnded, nil
	case StatusReading.String():
		return StatusReading, nil
	case StatusDrop.String():
		return StatusDrop, nil
	case StatusOnHold.String():
		return StatusOnHold, nil
	default:
		return StatusUnknown, errors.New("Status not supported")
	}
}

func (s Status) IsNil() bool {
	return s == StatusUnknown
}
