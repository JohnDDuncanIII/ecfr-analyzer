"use client";

import { useState, useEffect } from "react";

// ecfr
import { AgencyWordCount, getAgencyWordCounts } from "@/api/wordCounts";
import { BarChart } from "@/components/ecfr/BarChart";

export default function WordCountDisplay() {
	const [wordCounts, setWordCounts] = useState<AgencyWordCount[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		async function fetchData() {
			try {
				const data = await getAgencyWordCounts();
				setWordCounts(data);
			} catch (err) {
				setError(
					err instanceof Error ? err.message : "Failed to fetch word counts",
				);
			} finally {
				setLoading(false);
			}
		}

		fetchData();
	}, []);

	if (loading) return <div>Loading...</div>;
	if (error) return <div>Error: {error}</div>;

	// Transform data for HighCharts format with explicit tuple typing
	const chartData: [string, number][] = wordCounts.map((agency) => [
		agency.name,
		agency.cfr_word_count,
	]);

	return (
		<div>
			<BarChart
				data={chartData}
				title="Agency CFR Word Counts"
				yAxisTitle="Word Count"
			/>
			<ul>
				{wordCounts.map((agency) => (
					<li key={agency.name}>
						{agency.name}: {agency.cfr_word_count.toLocaleString()} words
					</li>
				))}
			</ul>
		</div>
	);
}

export { WordCountDisplay };
