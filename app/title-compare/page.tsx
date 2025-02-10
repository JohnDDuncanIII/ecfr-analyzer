"use client";

import { useState, useEffect, useRef } from "react";
import { format } from "date-fns";
import { Calendar } from "@/components/ui/calendar";
import {
	Select,
	SelectContent,
	SelectItem,
	SelectTrigger,
	SelectValue,
} from "@/components/ui/select";
import {
	Popover,
	PopoverContent,
	PopoverTrigger,
} from "@/components/ui/popover";
import { Button } from "@/components/ui/button";
import { CalendarIcon } from "lucide-react";
import { cn } from "@/lib/utils";
import { Title, getTitles } from "@/api/titles";
import * as Diff from "diff";

export default function TitleCompare() {
	const [date1, setDate1] = useState<Date>();
	const [date2, setDate2] = useState<Date>();
	const [selectedTitle, setSelectedTitle] = useState<string>();
	const [titles, setTitles] = useState<Title[]>([]);
	const [xmlData1, setXmlData1] = useState<string | null>(null);
	const [xmlData2, setXmlData2] = useState<string | null>(null);
	const [diffResult, setDiffResult] = useState<Diff.Change[]>([]);
	const [loading, setLoading] = useState(true);
	const [error, setError] = useState<string | null>(null);
	const [isLoading1, setIsLoading1] = useState(false);
	const [isLoading2, setIsLoading2] = useState(false);
	const preRef1 = useRef<HTMLPreElement>(null);
	const preRef2 = useRef<HTMLPreElement>(null);

	// Fetch available titles on component mount
	useEffect(() => {
		async function fetchTitles() {
			try {
				const data = await getTitles();
				setTitles(data);
			} catch (err) {
				setError(err instanceof Error ? err.message : "Failed to fetch titles");
			} finally {
				setLoading(false);
			}
		}

		fetchTitles();
	}, []);

	useEffect(() => {
		const fetchXmlData = async () => {
			if (!date1 || !selectedTitle) return;

			setIsLoading1(true);
			try {
				const formattedDate = format(date1, "yyyy-MM-dd");
				const response = await fetch(
					`https://www.ecfr.gov/api/versioner/v1/full/${formattedDate}/title-${selectedTitle}.xml`,
				);
				const data = await response.text();
				setXmlData1(data);
			} catch (err) {
				setError(
					err instanceof Error ? err.message : "Failed to fetch XML data",
				);
			} finally {
				setIsLoading1(false);
			}
		};

		fetchXmlData();
	}, [date1, selectedTitle]);

	useEffect(() => {
		const fetchXmlData = async () => {
			if (!date2 || !selectedTitle) return;

			setIsLoading2(true);
			try {
				const formattedDate = format(date2, "yyyy-MM-dd");
				const response = await fetch(
					`https://www.ecfr.gov/api/versioner/v1/full/${formattedDate}/title-${selectedTitle}.xml`,
				);
				const data = await response.text();
				setXmlData2(data);
			} catch (err) {
				setError(
					err instanceof Error ? err.message : "Failed to fetch XML data",
				);
			} finally {
				setIsLoading2(false);
			}
		};

		fetchXmlData();
	}, [date2, selectedTitle]);

	// Calculate diff when both XMLs are loaded
	useEffect(() => {
		if (xmlData1 && xmlData2 && preRef1.current && preRef2.current) {
			const text1 = preRef1.current.textContent || "";
			const text2 = preRef2.current.textContent || "";

			const diff = Diff.diffLines(text1, text2);
			setDiffResult(diff);
		}
	}, [xmlData1, xmlData2]);

	const renderDiff = (diff: Diff.Change[]) => {
		return diff.map((part, index) => {
			const color = part.added
				? "bg-green-100 text-green-800"
				: part.removed
					? "bg-red-100 text-red-800"
					: "text-gray-800";

			return (
				<span
					key={index}
					className={`${color} ${part.added || part.removed ? "block px-2 py-1" : ""}`}
				>
					{part.value}
				</span>
			);
		});
	};

	return (
		<div className="container mx-auto p-8">
			<h1 className="text-2xl font-bold mb-8">Compare CFR Titles Over Time</h1>

			<div className="flex gap-4 mb-8">
				{loading ? (
					<div>Loading titles...</div>
				) : error ? (
					<div className="text-red-500">Error: {error}</div>
				) : (
					<Select onValueChange={setSelectedTitle} value={selectedTitle}>
						<SelectTrigger className="w-[240px]">
							<SelectValue placeholder="Select a title" />
						</SelectTrigger>
						<SelectContent>
							{titles.map((title) => (
								<SelectItem key={title.number} value={title.number.toString()}>
									{title.number} - {title.name}
								</SelectItem>
							))}
						</SelectContent>
					</Select>
				)}
			</div>

			<div className="grid grid-cols-2 gap-8 mb-8">
				<div>
					<Popover>
						<PopoverTrigger asChild>
							<Button
								variant={"outline"}
								className={cn(
									"w-[240px] justify-start text-left font-normal mb-4",
									!date1 && "text-muted-foreground",
								)}
							>
								<CalendarIcon className="mr-2 h-4 w-4" />
								{date1 ? format(date1, "PPP") : <span>Pick first date</span>}
							</Button>
						</PopoverTrigger>
						<PopoverContent className="w-auto p-0" align="start">
							<Calendar
								mode="single"
								selected={date1}
								onSelect={setDate1}
								initialFocus
							/>
						</PopoverContent>
					</Popover>

					{isLoading1 && <div>Loading XML data...</div>}
					{xmlData1 && (
						<pre
							ref={preRef1}
							className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-[600px] text-sm"
							dangerouslySetInnerHTML={{ __html: xmlData1 }}
						/>
					)}
				</div>

				<div>
					<Popover>
						<PopoverTrigger asChild>
							<Button
								variant={"outline"}
								className={cn(
									"w-[240px] justify-start text-left font-normal mb-4",
									!date2 && "text-muted-foreground",
								)}
							>
								<CalendarIcon className="mr-2 h-4 w-4" />
								{date2 ? format(date2, "PPP") : <span>Pick second date</span>}
							</Button>
						</PopoverTrigger>
						<PopoverContent className="w-auto p-0" align="start">
							<Calendar
								mode="single"
								selected={date2}
								onSelect={setDate2}
								initialFocus
							/>
						</PopoverContent>
					</Popover>

					{isLoading2 && <div>Loading XML data...</div>}
					{xmlData2 && (
						<pre
							ref={preRef2}
							className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-[600px] text-sm"
							dangerouslySetInnerHTML={{ __html: xmlData2 }}
						/>
					)}
				</div>
			</div>

			{/* Diff Display */}
			{xmlData1 && xmlData2 && (
				<div className="mt-8">
					<h2 className="text-xl font-bold mb-4">Differences</h2>
					<pre className="bg-gray-100 p-4 rounded-lg overflow-auto max-h-[600px] text-sm whitespace-pre-wrap">
						{renderDiff(diffResult)}
					</pre>
				</div>
			)}

			{error && <div className="text-red-500 mt-4">Error: {error}</div>}
		</div>
	);
}
