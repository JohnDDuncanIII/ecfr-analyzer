"use client";

import { useState, useEffect } from "react";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import {
	Agency,
	CfrReference,
	getAgencyNames,
	getAgencyCfrReferences,
} from "@/api/agencies";

export default function TextComparePage() {
	const [selectedAgencySlug, setSelectedAgencySlug] = useState<string>("");
	const [agencies, setAgencies] = useState<Agency[]>([]);
	const [references, setReferences] = useState<CfrReference[]>([]);
	const [agencyWordCount, setAgencyWordCount] = useState<number | null>(null);
	const [loading, setLoading] = useState(true);
	const [referencesLoading, setReferencesLoading] = useState(false);
	const [error, setError] = useState<string | null>(null);

	useEffect(() => {
		async function fetchAgencies() {
			try {
				const data = await getAgencyNames();
				setAgencies(data);
			} catch (err) {
				setError(
					err instanceof Error ? err.message : "Failed to fetch agencies",
				);
			} finally {
				setLoading(false);
			}
		}

		fetchAgencies();
	}, []);

	useEffect(() => {
		async function fetchReferences() {
			if (!selectedAgencySlug) {
				setReferences([]);
				setAgencyWordCount(null);
				return;
			}

			setReferencesLoading(true);
			setAgencyWordCount(null); // Clear the word count while loading
			try {
				const data = await getAgencyCfrReferences(selectedAgencySlug);
				setReferences(data.references);
				setAgencyWordCount(data.agency_word_count);
			} catch (err) {
				setError(
					err instanceof Error ? err.message : "Failed to fetch references",
				);
			} finally {
				setReferencesLoading(false);
			}
		}

		fetchReferences();
	}, [selectedAgencySlug]);

	const renderReferenceDetails = (ref: CfrReference) => {
		const details: { label: string; value: string | undefined }[] = [
			{ label: "Title", value: ref.title },
			{ label: "Subtitle", value: ref.subtitle },
			{ label: "Chapter", value: ref.chapter },
			{ label: "Subchapter", value: ref.subchapter },
			{ label: "Part", value: ref.part },
			{ label: "Subpart", value: ref.subpart },
			{ label: "Section", value: ref.section },
		];

		return (
			<div className="space-y-1">
				{details
					.filter((detail) => detail.value)
					.map((detail, idx) => (
						<p key={idx} className="text-sm">
							<span className="font-medium">{detail.label}:</span>{" "}
							<span className="text-muted-foreground">{detail.value}</span>
						</p>
					))}
				{ref.full_text && (
					<div className="mt-4">
						<p className="font-medium text-sm">Full Text:</p>
						<p className="text-sm text-muted-foreground whitespace-pre-wrap">
							{ref.full_text}
						</p>
					</div>
				)}
			</div>
		);
	};

	return (
		<div className="flex flex-col items-center justify-start p-4 min-h-screen w-screen">
			<div className="flex items-center justify-start mb-8">
				<h1 className="text-3xl font-bold">Agency CFR Titles & Text</h1>
			</div>

			<Card className="w-full max-w-7xl mb-8">
				<CardHeader>
					<CardTitle>Agency</CardTitle>
				</CardHeader>
				<CardContent>
					{loading ? (
						<div>Loading agencies...</div>
					) : error ? (
						<div className="text-red-500">Error: {error}</div>
					) : (
						<div className="w-full max-w-xs">
							<Select
								value={selectedAgencySlug}
								onValueChange={setSelectedAgencySlug}
							>
								<SelectTrigger>
									<SelectValue placeholder="Select an agency">
										{selectedAgencySlug
											? agencies.find((a) => a.slug === selectedAgencySlug)
													?.name
											: "Select an agency"}
									</SelectValue>
								</SelectTrigger>
								<SelectContent>
									{agencies.map((agency) => (
										<SelectItem key={agency.slug} value={agency.slug}>
											{agency.name}
										</SelectItem>
									))}
								</SelectContent>
							</Select>
						</div>
					)}

					{selectedAgencySlug && agencyWordCount !== null && (
						<div className="mt-4 p-3 bg-muted rounded-lg">
							<p className="text-sm">
								<span className="font-medium">Total Word Count:</span>{" "}
								<span className="text-muted-foreground">
									{agencyWordCount.toLocaleString()} words
								</span>
							</p>
						</div>
					)}

					{selectedAgencySlug && (
						<div className="mt-6">
							<h3 className="text-lg font-semibold mb-4">CFR References</h3>
							{referencesLoading ? (
								<div>Loading references...</div>
							) : references.length > 0 ? (
								<div className="space-y-2">
									{references.map((ref, index) => (
										<div key={index} className="p-3 bg-muted rounded-lg">
											{renderReferenceDetails(ref)}
										</div>
									))}
								</div>
							) : (
								<p>No CFR references found for this agency.</p>
							)}
						</div>
					)}
				</CardContent>
			</Card>
		</div>
	);
}
