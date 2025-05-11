/*
  utils.ts for the Balkonsolar Dashboard
  - Provides a cn() utility to merge Tailwind and conditional class names
*/
import { clsx, type ClassValue } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
