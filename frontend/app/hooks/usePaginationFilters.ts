"use client";
import { usePathname, useRouter, useSearchParams } from "next/navigation";
import { useCallback, useMemo } from "react";
import { PaginationParams } from "../types/searchParams.type";
import { parsePagination } from "../shared/parsePaginationParams";

export function usePaginationFilters() {
  const router = useRouter();
  const pathname = usePathname();
  const searchParams = useSearchParams();

  const filters = useMemo<PaginationParams>(() => {
    return parsePagination({
      page_size: searchParams.get("page_size") ?? undefined,
      current_page: searchParams.get("current_page") ?? undefined,
    });
  }, [searchParams]);

  const setFilters = useCallback(
    (patch: Partial<PaginationParams>, opts: { replace?: boolean } = {}) => {
      const next: PaginationParams = { ...filters, ...patch };
      const qs = `page_size=${next.pageSize}&current_page=${next.currentPage}`;
      const url = `${pathname}?${qs}`;
      if (opts.replace) {
        router.replace(url, { scroll: false });
      } else {
        router.push(url, { scroll: false });
      }
    },
    [filters, pathname, router],
  );
  return { filters, setFilters };
}
