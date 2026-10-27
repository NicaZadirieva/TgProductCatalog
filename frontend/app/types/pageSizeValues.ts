import { PageSizeParam } from './searchParams.type';

export const PAGE_SIZES: PageSizeParam["pageSize"][] = [10, 25, 50, 100] as const;
export const DEFAULT_PAGE_SIZE = 10 as const;