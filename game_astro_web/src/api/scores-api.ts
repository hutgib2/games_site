const BASE_URL = '/api/scores';
type ScoreEntry = { username: string; score: number };

export async function fetchScores(game: string): Promise<ScoreEntry[]> {
  const res = await fetch(`${BASE_URL}/${game}`);
  if (!res.ok) {
	throw new Error(`Failed to fetch scores: ${res.status}`);
  }
  
  return res.json();
}

export async function postScore(game: string, username: string, score: number)  {
	return await fetch(`${BASE_URL}/${game}`, {
		method: "POST",
		headers: { "Content-Type": "application/json" },
		body: JSON.stringify({username: username, score: score}),
	});
}