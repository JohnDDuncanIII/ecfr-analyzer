import config from '@/app/config';

export type Agency = {
  name: string;
  cfr_word_count: number;
};

export async function getAgencyWordCounts(): Promise<Agency[]> {
  const response = await fetch(`${config.apiBaseUrl}/api/agency/`);
  if (!response.ok) {
    throw new Error('Failed to fetch agencies');
  }
  return await response.json();
} 