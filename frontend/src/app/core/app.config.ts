export const appConfig = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  apiVersion: 'v1',
  maxQuestionsPerInterview: 5,
};

export const getApiUrl = (path: string): string => {
  const baseUrl = appConfig.apiBaseUrl.replace(/\/$/, '');
  const apiPath = `/api/${appConfig.apiVersion}${path.startsWith('/') ? path : `/${path}`}`;
  return `${baseUrl}${apiPath}`;
};
