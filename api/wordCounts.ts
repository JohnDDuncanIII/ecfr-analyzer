export type Agency = {
  name: string;
  cfr_word_count: number;
};

export async function getAgencyWordCounts(): Promise<Agency[]> {
  const response = await fetch('http://localhost:8000/api/agency/');
  if (!response.ok) {
    throw new Error('Failed to fetch agencies');
  }
  return await response.json();
} 