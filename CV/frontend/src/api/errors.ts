import { isAxiosError } from 'axios'

export interface ApiFieldError {
  field: string
  message: string
}

export interface ApiErrorBody {
  code: string
  message: string
  fieldErrors: ApiFieldError[]
  traceId: string
}

/** Extracts the backend's ApiError message, falling back to a generic string for network/unknown errors. */
export function extractErrorMessage(error: unknown): string {
  if (isAxiosError<ApiErrorBody>(error) && error.response?.data?.message) {
    return error.response.data.message
  }
  return 'Something went wrong. Please try again.'
}

export function extractFieldErrors(error: unknown): ApiFieldError[] {
  if (isAxiosError<ApiErrorBody>(error) && error.response?.data?.fieldErrors) {
    return error.response.data.fieldErrors
  }
  return []
}
