run-db:
	docker-compose up --quiet-pull -d db

deps:
	go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
	go install golang.org/x/tools/cmd/stringer@latest

generate:
	go generate -run stringer ./...
	go generate ./...

test:
	go clean -testcache
	go test -count=1 ./model/... -coverprofile cover.out