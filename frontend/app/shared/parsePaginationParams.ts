import { DEFAULT_CURRENT_PAGE } from '../types/defaultPageValue';
import { DEFAULT_PAGE_SIZE, PAGE_SIZES } from "../types/pageSizeValues";
import { CurrentPageParam, PageSizeParam, PaginationParams, SearchParams, SearchParamsValue } from "../types/searchParams.type";

/**
 * Type Guard для проверки значений размера элементов на странице (pageSize)
 * @param pageSize
 * @returns
 */
function isPageSizeParam(pageSize: number): pageSize is PageSizeParam["pageSize"] {
  return (PAGE_SIZES as readonly number[]).includes(pageSize);
}

export function buildPageSize(pageSize: number): PageSizeParam {
	return { pageSize: isPageSizeParam(pageSize) ? pageSize : DEFAULT_PAGE_SIZE };
}
function parsePageSize(searchParamValue: SearchParamsValue): PageSizeParam {
  if (Array.isArray(searchParamValue)) {
	if (!Number.isInteger(searchParamValue[0])) {
		// не валидное значение => выбираем значение по умолчанию
		return buildPageSize(DEFAULT_PAGE_SIZE);
	}
    const pageSizeFromUser = Number.parseInt(searchParamValue[0]);
    return buildPageSize(pageSizeFromUser);
  } else if (searchParamValue && Number.isInteger(searchParamValue)) {
	const pageSizeFromUser = Number.parseInt(searchParamValue);
	return buildPageSize(pageSizeFromUser);
  }
  // если не указано => выбираем значение по умолчанию
  return buildPageSize(DEFAULT_PAGE_SIZE);
}

function isCurrentPageParam(currentPage: number): currentPage is CurrentPageParam["currentPage"] {
	return Number.isInteger(currentPage) && currentPage >= 0;
}
function buildCurrentPage(currentPage: number): CurrentPageParam {
	return { currentPage: isCurrentPageParam(currentPage) ? currentPage : DEFAULT_CURRENT_PAGE };
}
function parseCurrentPage(searchParamValue: SearchParamsValue): CurrentPageParam {
  if (Array.isArray(searchParamValue)) {
	if (!Number.isInteger(searchParamValue[0])) {
		// не валидное значение => выбираем значение по умолчанию
		return buildCurrentPage(DEFAULT_CURRENT_PAGE);
	}
    const pageFromUser = Number.parseInt(searchParamValue[0]);
    return buildCurrentPage(pageFromUser);
  } else if (searchParamValue && Number.isInteger(searchParamValue)) {
	const pageFromUser = Number.parseInt(searchParamValue);
	return buildCurrentPage(pageFromUser);
  }
  // если не указано => выбираем значение по умолчанию
  return buildCurrentPage(DEFAULT_CURRENT_PAGE);
}

export function parsePagination(
  searchParams: SearchParams,
): PaginationParams {
  const { page_size, current_page } = searchParams;
  return {
    ...parsePageSize(page_size),
    ...parseCurrentPage(current_page),
  };
}
