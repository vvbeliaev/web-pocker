// src/lib/sounds.ts
// Procedural sound effects via Web Audio API — no audio files needed.
let ctx: AudioContext | null = null;

function getCtx(): AudioContext | null {
	if (typeof window === 'undefined') return null;
	try {
		if (!ctx) ctx = new AudioContext();
		if (ctx.state === 'suspended') ctx.resume();
		return ctx;
	} catch {
		return null;
	}
}

/** Short card-slap noise burst — deal / community card reveal */
export function playCardDeal() {
	const ac = getCtx();
	if (!ac) return;
	try {
		const bufferSize = Math.floor(ac.sampleRate * 0.055);
		const buffer = ac.createBuffer(1, bufferSize, ac.sampleRate);
		const data = buffer.getChannelData(0);
		for (let i = 0; i < bufferSize; i++) {
			data[i] = (Math.random() * 2 - 1) * (1 - i / bufferSize) * 0.9;
		}

		const source = ac.createBufferSource();
		source.buffer = buffer;

		const hpf = ac.createBiquadFilter();
		hpf.type = 'highpass';
		hpf.frequency.value = 1800;

		const gain = ac.createGain();
		gain.gain.setValueAtTime(0.45, ac.currentTime);
		gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.055);

		source.connect(hpf);
		hpf.connect(gain);
		gain.connect(ac.destination);
		source.start();
	} catch { /* ignore */ }
}

/** Two metallic tings — call / raise */
export function playChips() {
	const ac = getCtx();
	if (!ac) return;
	try {
		[0, 0.07].forEach((delay) => {
			const osc = ac.createOscillator();
			osc.type = 'sine';
			osc.frequency.setValueAtTime(880 - delay * 200, ac.currentTime + delay);
			osc.frequency.exponentialRampToValueAtTime(320, ac.currentTime + delay + 0.14);

			const gain = ac.createGain();
			gain.gain.setValueAtTime(0.22, ac.currentTime + delay);
			gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + delay + 0.14);

			osc.connect(gain);
			gain.connect(ac.destination);
			osc.start(ac.currentTime + delay);
			osc.stop(ac.currentTime + delay + 0.14);
		});
	} catch { /* ignore */ }
}

/** Soft descending tone — fold */
export function playFold() {
	const ac = getCtx();
	if (!ac) return;
	try {
		const osc = ac.createOscillator();
		osc.type = 'sine';
		osc.frequency.setValueAtTime(380, ac.currentTime);
		osc.frequency.exponentialRampToValueAtTime(160, ac.currentTime + 0.18);

		const gain = ac.createGain();
		gain.gain.setValueAtTime(0.16, ac.currentTime);
		gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.18);

		osc.connect(gain);
		gain.connect(ac.destination);
		osc.start();
		osc.stop(ac.currentTime + 0.18);
	} catch { /* ignore */ }
}

/** Ascending C-E-G-C arpeggio — pot win */
export function playWin() {
	const ac = getCtx();
	if (!ac) return;
	try {
		[523, 659, 784, 1047].forEach((freq, i) => {
			const osc = ac.createOscillator();
			osc.type = 'sine';
			osc.frequency.value = freq;

			const gain = ac.createGain();
			const t = ac.currentTime + i * 0.11;
			gain.gain.setValueAtTime(0.28, t);
			gain.gain.exponentialRampToValueAtTime(0.001, t + 0.45);

			osc.connect(gain);
			gain.connect(ac.destination);
			osc.start(t);
			osc.stop(t + 0.45);
		});
	} catch { /* ignore */ }
}

/** Neutral descending tone — someone else wins */
export function playHandEnd() {
	const ac = getCtx();
	if (!ac) return;
	try {
		const osc = ac.createOscillator();
		osc.type = 'sine';
		osc.frequency.setValueAtTime(520, ac.currentTime);
		osc.frequency.exponentialRampToValueAtTime(380, ac.currentTime + 0.22);

		const gain = ac.createGain();
		gain.gain.setValueAtTime(0.14, ac.currentTime);
		gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.22);

		osc.connect(gain);
		gain.connect(ac.destination);
		osc.start();
		osc.stop(ac.currentTime + 0.22);
	} catch { /* ignore */ }
}

/** Short metronome click — turn timer urgent (<10 s) */
export function playTimerTick() {
	const ac = getCtx();
	if (!ac) return;
	try {
		const osc = ac.createOscillator();
		osc.type = 'square';
		osc.frequency.value = 1100;

		const gain = ac.createGain();
		gain.gain.setValueAtTime(0.07, ac.currentTime);
		gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.022);

		osc.connect(gain);
		gain.connect(ac.destination);
		osc.start();
		osc.stop(ac.currentTime + 0.022);
	} catch { /* ignore */ }
}

/** Low rumbling boom — player eliminated */
export function playEliminated() {
	const ac = getCtx();
	if (!ac) return;
	try {
		const osc = ac.createOscillator();
		osc.type = 'sine';
		osc.frequency.setValueAtTime(90, ac.currentTime);
		osc.frequency.exponentialRampToValueAtTime(28, ac.currentTime + 0.65);

		const gain = ac.createGain();
		gain.gain.setValueAtTime(0.5, ac.currentTime);
		gain.gain.exponentialRampToValueAtTime(0.001, ac.currentTime + 0.65);

		osc.connect(gain);
		gain.connect(ac.destination);
		osc.start();
		osc.stop(ac.currentTime + 0.65);
	} catch { /* ignore */ }
}
