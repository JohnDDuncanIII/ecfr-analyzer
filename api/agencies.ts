import config from '@/app/config';

export interface Agency {
    name: string;
    slug: string;
    cfr_word_count: number;
}

export interface CfrReference {
    title?: string;
    subtitle?: string;
    chapter?: string;
    subchapter?: string;
    part?: string;
    subpart?: string;
    section?: string;
    full_text?: string;
}

export interface AgencyReferencesResponse {
    agency_word_count: number;
    references: CfrReference[];
}

export async function getAgencyNames(): Promise<Agency[]> {
    const response = await fetch(`${config.apiBaseUrl}/api/agency-name/`);
    if (!response.ok) {
        throw new Error('Failed to fetch agency names');
    }
    return await response.json();
}

export async function getAgencyCfrReferences(slug: string): Promise<AgencyReferencesResponse> {
    const response = await fetch(`${config.apiBaseUrl}/api/agency/${encodeURIComponent(slug)}/references/`);
    if (!response.ok) {
        throw new Error('Failed to fetch CFR references');
    }
    return await response.json();
}
