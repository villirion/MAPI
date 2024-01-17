package model_test

import (
	"testing"

	"mapi/model"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewKindError(t *testing.T) {
	testCases := map[string]string{
		"empty":         "",
		"not supported": "not supported",
	}

	for name, value := range testCases {
		t.Run(name, func(t *testing.T) {
			_, err := model.NewKind(value)
			require.EqualError(t, err, "Kind not supported")
		})
	}
}

func TestNewKindSuccess(t *testing.T) {
	testCases := map[string]model.Kind{
		"manhwa": model.KindManhwa,
		"manga":  model.KindManga,
	}

	for name, value := range testCases {
		t.Run(name, func(t *testing.T) {
			kind, err := model.NewKind(name)
			require.NoError(t, err)
			require.Equal(t, kind, value)
		})
	}
}

func TestKindIsNilError(t *testing.T) {
	testCases := []model.Kind{
		model.KindManhwa,
		model.KindManga,
	}

	for _, value := range testCases {
		t.Run(value.String(), func(t *testing.T) {
			assert.False(t, value.IsNil())
		})
	}
}

func TestKindIsNilSuccess(t *testing.T) {
	assert.True(t, model.KindUnknown.IsNil())
}
