// news-image-20261120 entry (Node 22, standard library only).
//
// The image is drawn by generate.py (Pillow, run at build time) and committed
// as entry.png beside this file. This program only copies it to the output
// directory, so both graded runs write identical bytes, with no network.
import { copyFileSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

// The gate reads exactly one file, so the output name is fixed here and
// nowhere else: entry.png, whether the bytes are PNG or JPEG.
const repoRoot = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
copyFileSync(join(repoRoot, "entry.png"), join(outDir, "entry.png"));
