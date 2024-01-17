package model_test

import (
	"testing"

	"mapi/model"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewStatusError(t *testing.T) {
	testCases := map[string]string{
		"empty":         "",
		"not supported": "not supported",
	}

	for name, value := range testCases {
		t.Run(name, func(t *testing.T) {
			_, err := model.NewStatus(value)
			require.EqualError(t, err, "Status not supported")
		})
	}
}

func TestNewStatusSuccess(t *testing.T) {
	testCases := map[string]model.Status{
		"ended":   model.StatusEnded,
		"reading": model.StatusReading,
		"onHold":  model.StatusOnHold,
		"drop":    model.StatusDrop,
	}

	for name, value := range testCases {
		t.Run(name, func(t *testing.T) {
			status, err := model.NewStatus(name)
			require.NoError(t, err)
			require.Equal(t, status, value)
		})
	}
}

func TestStatusIsNilError(t *testing.T) {
	testCases := []model.Status{
		model.StatusEnded,
		model.StatusReading,
		model.StatusOnHold,
		model.StatusDrop,
	}

	for _, value := range testCases {
		t.Run(value.String(), func(t *testing.T) {
			assert.False(t, value.IsNil())
		})
	}
}

func TestStatusIsNilSuccess(t *testing.T) {
	assert.True(t, model.StatusUnknown.IsNil())
}
