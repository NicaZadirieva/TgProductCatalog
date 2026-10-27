"use client";

import styles from "./index.module.css";
import { useCallback, useEffect, useState } from "react";
import ProductsViewProps from "./ProductsView.props";
import ProductList from "../ProductList";
import updateProductItems from "@/app/api/utils/updateProductItems";
import { PAGE_SIZES } from '@/app/types/pageSizeValues';
import { usePaginationFilters } from '@/app/hooks/usePaginationFilters';
import { buildPageSize } from '@/app/shared/parsePaginationParams';



export default function ProductsView({
  defaultCount,
  defaultItems
}: ProductsViewProps) {
  const {filters, setFilters} = usePaginationFilters();
  const [count, setCount] = useState(defaultCount);
  const totalPages = Math.max(1, Math.ceil(count / filters.pageSize));
  const [items, updateItems] = useState(defaultItems);

  const handlePageSizeChange = (size: number) => {
    setFilters({...buildPageSize(size), currentPage: 0});
  };
  const onUpdate = useCallback(
    async (page: number, pageSize: number) =>
      updateProductItems(page, pageSize),
    [],
  );

  useEffect(() => {
    onUpdate(filters.currentPage, filters.pageSize)
      .then((data) => {
        setCount(data.count);
        updateItems(data.items);
      })
      .catch((e) => console.error(e));
  }, [filters, onUpdate]);

  return (
    <div className={styles["products-view"]}>
      <form>
        <select
          value={filters.pageSize}
          onChange={(e) => handlePageSizeChange(Number(e.target.value))}
        >
          {PAGE_SIZES.map((s) => (
            <option key={s} value={s}>
              {s} / стр.
            </option>
          ))}
        </select>
        <button
          type="button"
          disabled={filters.currentPage === 0}
          onClick={() => setFilters({
            currentPage: filters.currentPage - 1,
            pageSize: filters.pageSize
          })}
        >
          Назад
        </button>
        <span>
          Стр. {filters.currentPage + 1} из {totalPages}
        </span>
        <button
          type="button"
          disabled={filters.currentPage >= totalPages - 1}
          onClick={() => setFilters({
            currentPage: filters.currentPage + 1,
            pageSize: filters.pageSize
          })}
        >
          Вперёд
        </button>
      </form>
      <ProductList items={items} />
    </div>
  );
}
