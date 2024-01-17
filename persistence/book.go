package persistence

import (
	"context"
	"database/sql"
	"fmt"

	"mapi/model"

	"github.com/google/uuid"
)

type Book struct {
	db *sql.DB
}

func NewBook(db *sql.DB) *Book {
	return &Book{
		db: db,
	}
}

func (b *Book) CreateManhwa(ctx context.Context, book model.Book) (finalErr error) {
	defer func() {
		if finalErr != nil {
			finalErr = fmt.Errorf("failed to create book %s in database %w", book.String(), finalErr)
		}
	}()

	databaseID := uuid.New()

	_, err := b.db.ExecContext(
		ctx, `
			INSERT INTO manhwa (id, name, chapter, url, status)
			VALUES ($1, $2, $3, $4, $5)
		`,
		databaseID, book.Name(), book.Chapter(), book.URL(), book.Status(),
	)
	if err != nil {
		return fmt.Errorf("failed to execute insert book query: %w", finalErr)
	}

	return nil
}
