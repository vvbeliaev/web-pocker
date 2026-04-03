// src/lib/evaluator.ts
// Port of poker/game/evaluator.py — best 5-card hand from 5–7 cards.
import type { CardData } from './types';

const HAND_NAMES = [
	'High Card',
	'One Pair',
	'Two Pair',
	'Three of a Kind',
	'Straight',
	'Flush',
	'Full House',
	'Four of a Kind',
	'Straight Flush',
] as const;

export interface HandEval {
	rank: number;
	name: string;
	/** Indices into the input cards array that form the best 5-card hand */
	bestIndices: number[];
}

function evaluate5(cards: CardData[]): number[] {
	const ranks = cards.map((c) => c.rank);
	const suits = cards.map((c) => c.suit);
	const isFlush = new Set(suits).size === 1;

	const rankCounts = new Map<number, number>();
	for (const r of ranks) rankCounts.set(r, (rankCounts.get(r) ?? 0) + 1);

	// Sort groups by (count desc, rank desc) — primary group first
	const groups = [...rankCounts.entries()]
		.sort(([rA, cA], [rB, cB]) => (cA !== cB ? cB - cA : rB - rA))
		.map(([r]) => r);
	const counts = groups.map((r) => rankCounts.get(r)!);
	const sortedRanks = [...ranks].sort((a, b) => b - a);

	const unique = [...new Set(ranks)].sort((a, b) => b - a);
	let isStraight = false;
	let straightHigh = 0;
	if (unique.length === 5) {
		if (unique[0] - unique[4] === 4) {
			isStraight = true;
			straightHigh = unique[0];
		} else if (
			unique[0] === 14 &&
			unique[1] === 5 &&
			unique[2] === 4 &&
			unique[3] === 3 &&
			unique[4] === 2
		) {
			// Wheel: A-2-3-4-5
			isStraight = true;
			straightHigh = 5;
		}
	}

	if (isStraight && isFlush) return [8, straightHigh];
	if (counts[0] === 4) return [7, groups[0], groups[1]];
	if (counts[0] === 3 && counts.length > 1 && counts[1] === 2) return [6, groups[0], groups[1]];
	if (isFlush) return [5, ...sortedRanks];
	if (isStraight) return [4, straightHigh];
	if (counts[0] === 3) return [3, groups[0], groups[1], groups[2]];
	if (counts[0] === 2 && counts.length > 1 && counts[1] === 2)
		return [2, groups[0], groups[1], groups[2]];
	if (counts[0] === 2) return [1, groups[0], groups[1], groups[2], groups[3]];
	return [0, ...sortedRanks];
}

function compareTuples(a: number[], b: number[]): number {
	const len = Math.max(a.length, b.length);
	for (let i = 0; i < len; i++) {
		const diff = (a[i] ?? 0) - (b[i] ?? 0);
		if (diff !== 0) return diff;
	}
	return 0;
}

function combinations(n: number, k: number): number[][] {
	const result: number[][] = [];
	function helper(start: number, current: number[]) {
		if (current.length === k) {
			result.push([...current]);
			return;
		}
		for (let i = start; i < n; i++) {
			current.push(i);
			helper(i + 1, current);
			current.pop();
		}
	}
	helper(0, []);
	return result;
}

/**
 * Returns the best 5-card hand from 5–7 cards.
 * Returns null if fewer than 5 cards are provided.
 */
export function evaluateBestHand(cards: CardData[]): HandEval | null {
	if (cards.length < 5) return null;

	const combos = combinations(cards.length, 5);
	let bestScore: number[] | null = null;
	let bestCombo: number[] | null = null;

	for (const combo of combos) {
		const hand = combo.map((i) => cards[i]);
		const score = evaluate5(hand);
		if (!bestScore || compareTuples(score, bestScore) > 0) {
			bestScore = score;
			bestCombo = combo;
		}
	}

	if (!bestScore || !bestCombo) return null;

	return {
		rank: bestScore[0],
		name: HAND_NAMES[bestScore[0]],
		bestIndices: bestCombo,
	};
}
