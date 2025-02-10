"use client";

import Link from "next/link";
import {
	Card,
	CardHeader,
	CardTitle,
	CardDescription,
	CardContent,
} from "@/components/ui/card";
import { BarChart, GitCompare } from "lucide-react";

export default function Home() {
	return (
		<div className="flex flex-col items-center justify-start p-4 min-h-screen w-screen">
			<div className="flex items-center justify-start mb-8">
				<h1 className="text-3xl font-bold">eCFR Analyzer</h1>
			</div>
			<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 w-full max-w-7xl">
				<Link
					href="/word-counts"
					className="transition-transform hover:scale-105"
				>
					<Card>
						<CardHeader>
							<CardTitle className="flex items-center gap-2">
								<BarChart className="h-6 w-6" />
								Agency Word Counts
							</CardTitle>
							<CardDescription>
								Compare the regulatory footprint of federal agencies by word
								count
							</CardDescription>
						</CardHeader>
						<CardContent>
							<p className="text-sm text-muted-foreground">
								View and analyze the total word count of CFR regulations for
								each federal agency
							</p>
						</CardContent>
					</Card>
				</Link>

				<Link
					href="/agency-titles"
					className="transition-transform hover:scale-105"
				>
					<Card>
						<CardHeader>
							<CardTitle className="flex items-center gap-2">
								<GitCompare className="h-6 w-6" />
								Agency CFR Titles & Text
							</CardTitle>
							<CardDescription>
								Browse the complete CFR titles and full regulatory text for each
								federal agency
							</CardDescription>
						</CardHeader>
						<CardContent>
							<p className="text-sm text-muted-foreground">
								View detailed CFR references and their associated regulatory
								text organized by agency
							</p>
						</CardContent>
					</Card>
				</Link>

				<Link
					href="/title-compare"
					className="transition-transform hover:scale-105"
				>
					<Card>
						<CardHeader>
							<CardTitle className="flex items-center gap-2">
								<GitCompare className="h-6 w-6" />
								Historical Title Changes
							</CardTitle>
							<CardDescription>
								Track how federal regulations have evolved through title changes
								across different years
							</CardDescription>
						</CardHeader>
						<CardContent>
							<p className="text-sm text-muted-foreground">
								Discover regulatory shifts by comparing how CFR part titles have
								been modified, added, or removed over time
							</p>
						</CardContent>
					</Card>
				</Link>
			</div>
		</div>
	);
}
