"use client";

import { WordCountDisplay } from "@/components/ecfr/WordCountDisplay";

export default function WordCountsPage() {
	return (
		<div className="flex flex-col items-center justify-start p-4 min-h-screen w-screen">
			<div className="flex items-center justify-start mb-8">
				<h1 className="text-3xl font-bold">Agency Word Counts</h1>
			</div>
			<div className="w-full">
				<WordCountDisplay />
			</div>
		</div>
	);
}
