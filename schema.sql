CREATE TABLE "manhwa" (
    "id" UUID PRIMARY KEY,
    "name" VARCHAR(255) UNIQUE NOT NULL,
    "chapter" INT,
    "url" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
)

CREATE TABLE "manga" (
    "id" UUID PRIMARY KEY,
    "name" VARCHAR(255) UNIQUE NOT NULL,
    "chapter" INT,
    "url" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
)