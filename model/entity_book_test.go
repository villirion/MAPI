package model_test

import (
	"testing"

	"mapi/model"

	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"
)

func TestNewBookError(t *testing.T) {
	testCases := map[string]struct {
		name          string
		url           string
		chapter       int
		kind          model.Kind
		status        model.Status
		expectedError string
	}{
		"name empty": {
			name:          "",
			url:           "https://flamecomics.com/series/omniscient-readers-viewpoint/",
			chapter:       190,
			kind:          model.KindManhwa,
			status:        model.StatusReading,
			expectedError: "name must not be empty",
		},
		"url empty": {
			name:          "Omniscient Reader's Viewpoint",
			url:           "",
			chapter:       190,
			kind:          model.KindManhwa,
			status:        model.StatusReading,
			expectedError: "url must not be empty",
		},
		"kind empty": {
			name:          "Omniscient Reader's Viewpoint",
			url:           "https://flamecomics.com/series/omniscient-readers-viewpoint/",
			chapter:       190,
			kind:          model.KindUnknown,
			status:        model.StatusReading,
			expectedError: "kind must not be empty",
		},
		"status empty": {
			name:          "Omniscient Reader's Viewpoint",
			url:           "https://flamecomics.com/series/omniscient-readers-viewpoint/",
			chapter:       190,
			kind:          model.KindManhwa,
			status:        model.StatusUnknown,
			expectedError: "status must not be empty",
		},
	}

	for name, testCase := range testCases {
		t.Run(name, func(t *testing.T) {
			_, err := model.NewBook(
				testCase.name,
				testCase.url,
				testCase.chapter,
				testCase.kind,
				testCase.status,
			)
			assert.EqualError(t, err, testCase.expectedError)
		})
	}
}

func TestNewBookSuccess(t *testing.T) {
	book, err := model.NewBook(
		"Omniscient Reader's Viewpoint",
		"https://flamecomics.com/series/omniscient-readers-viewpoint/",
		190,
		model.KindManhwa,
		model.StatusReading,
	)
	require.NoError(t, err)

	assert.Equal(t, "Omniscient Reader's Viewpoint", book.Name())
	assert.Equal(t, "https://flamecomics.com/series/omniscient-readers-viewpoint/", book.URL())
	assert.Equal(t, 190, book.Chapter())
	assert.Equal(t, model.KindManhwa, book.Kind())
	assert.Equal(t, model.StatusReading, book.Status())
	assert.Equal(t, "Omniscient Reader's Viewpoint", book.String())
}
