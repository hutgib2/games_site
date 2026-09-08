import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

export const prerender = false;

type ScoreEntry = { username: string; score: number };

const ALLOWED_ORIGINS = ["http://localhost:4321", "http://localhost:8787"]; // add your prod domain here once deployed

function corsHeaders(request: Request): Record<string, string> {
  const origin = request.headers.get("Origin") ?? "";
  const allowed = ALLOWED_ORIGINS.includes(origin) ? origin : ALLOWED_ORIGINS[0];
  return {
    "Access-Control-Allow-Origin": allowed,
    "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
    "Access-Control-Allow-Headers": "Content-Type",
  };
}

// Browsers preflight the POST (it has a JSON body) before sending it
export const OPTIONS: APIRoute = async ({ request }) => {
  return new Response(null, { headers: corsHeaders(request) });
};

// Returns the top 5 high scores for a given game
export const GET: APIRoute = async ({ request, params }) => {
  const { game } = params;
  const headers = corsHeaders(request);

  if (!game) {
    return new Response("Unknown game", { status: 404, headers });
  }

  const { results } = await env.DB
    .prepare("SELECT username, score FROM scores WHERE game = ? ORDER BY score DESC, timestamp ASC LIMIT 5")
    .bind(game)
    .all();

  return Response.json(results, { headers });
};

// Add a score to the database
export const POST: APIRoute = async ({ request, params }) => {
  const { game } = params;
  const headers = corsHeaders(request);

  if (!game) {
    return new Response("Unknown game", { status: 404, headers });
  }

  const { username, score }: ScoreEntry = await request.json();
  if (typeof username !== "string" || !username.trim()) {
    return new Response("Invalid username", { status: 400, headers });
  }
  if (typeof score !== "number" || !Number.isInteger(score) || score <= 0) {
    return new Response("Invalid score", { status: 400, headers });
  }

  await env.DB
    .prepare("INSERT INTO scores (game, username, score) VALUES (?, ?, ?)")
    .bind(game, username, score)
    .run();

  return new Response(null, { status: 204, headers });
};