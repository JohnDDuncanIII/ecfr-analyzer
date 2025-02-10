export interface Title {
	number: number;
	name: string;
	latest_amended_on: string;
	latest_issue_date: string;
	up_to_date_as_of: string;
	reserved: boolean;
}

export async function getTitles(): Promise<Title[]> {
	const response = await fetch("http://localhost:8000/api/title/");
	if (!response.ok) {
		throw new Error(`Failed to fetch titles: ${response.statusText}`);
	}
	return response.json();
} 
