// Backend origin, used both as the axios baseURL and to build uploaded-file URLs.
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

export { API_BASE_URL }
