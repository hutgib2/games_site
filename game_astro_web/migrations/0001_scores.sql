CREATE TABLE scores(
	id INTEGER PRIMARY KEY,
	game TEXT NOT NULL,
	username TEXT NOT NULL,
	score INTEGER NOT NULL CHECK (score > 0),
	timestamp INTEGER NOT NULL DEFAULT (unixepoch())
);

CREATE INDEX idx_scores ON scores (game, score DESC);