// Centralized API config for backend integration

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export function getApiUrl(path: string) {
  return `${API_BASE_URL}${path}`;
}
