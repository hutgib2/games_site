import type { APIRoute } from "astro";
import { env } from "cloudflare:workers";

export const prerender = false;

type ScoreEntry = { username: string; score: number };

export const GET: APIRoute = async ({ params }) => {
  const { game } = params;
  if (!game) {
    return new Response("Unknown game", { status: 404 });
  }
  
  const { results } = await env.DB
    .prepare("SELECT username, score FROM scores WHERE game = ? ORDER BY score DESC, timestamp ASC LIMIT 5")
    .bind(game)
    .all();

  return Response.json(results);
};

export const POST: APIRoute = async ({ request, params }) => {
  const { game } = params;
  if (!game) {
    return new Response("Unknown game", { status: 404 });
  }
  
  const { username, score }: ScoreEntry = await request.json();
  if (typeof username !== "string" || !username.trim()) {
    return new Response("Invalid username", { status: 400 });
  }
  if (typeof score !== "number" || !Number.isInteger(score) || score <= 0) {
    return new Response("Invalid score", { status: 400 });
  }
  
  await env.DB
    .prepare("INSERT INTO scores (game, username, score) VALUES (?, ?, ?)")
    .bind(game, username, score)
    .run();

  return new Response(null, { status: 204 });
};