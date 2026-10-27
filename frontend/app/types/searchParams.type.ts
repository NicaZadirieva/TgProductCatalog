export interface PageSizeParam {
  pageSize: 10 | 25 | 50 | 100;
}

export interface CurrentPageParam {
  currentPage: number;
}

export type SearchParamsValue = string | string[] | undefined;

export type SearchParams = Record<"page_size" | "current_page", SearchParamsValue>;

export type PaginationParams = PageSizeParam & CurrentPageParam;
