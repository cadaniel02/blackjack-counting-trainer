import {
    FetchOptions,
    SuccessCallback,
    ErrorCallback,
  } from "../interfaces/types";

export async function fetchData<
T
>(url: string, options: FetchOptions, onSuccess: SuccessCallback<T>, onError: ErrorCallback): Promise<void> {
try {
  const response = await fetch(url, options);
  if (!response.ok) {
    throw new Error(`Failed to fetch from ${url}`);
  }
  const data = (await response.json()) as T;
  onSuccess(data);
} catch (error) {
  if (error instanceof Error) {
    console.error(error.message);
    onError(error.message);
  } else {
    console.error("An unknown error occurred");
    onError("An unknown error occurred");
  }
}
}