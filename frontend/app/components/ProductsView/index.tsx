import styles from "./index.module.css";
import { useCallback, useEffect, useState } from "react";
import ProductsViewProps from './ProductsView.props';
import ProductList from '../ProductList';
import getProductsByPage from '@/app/api/product/get_by_page.req';
import getProductPhoto from '@/app/api/image/get_by_product.req';

const PAGE_SIZES = [10, 25, 50, 100];

export default function ProductsView({defaultCount, defaultItems}: ProductsViewProps) {
  const [page, setPage] = useState(0);
  const [pageSize, setPageSize] = useState(10);
  const [count, setCount] = useState(defaultCount);
  const totalPages = Math.max(1, Math.ceil(count / pageSize));
  const [items, updateItems] = useState(defaultItems);

  const handlePageSizeChange = (size: number) => {
    setPageSize(size);
    setPage(0);
  };
  const onUpdate = useCallback(async (page: number, pageSize: number) => {
	const products_dto = await getProductsByPage({currentPage: page, pageSize});
	const promises = products_dto.items.map((product) => getProductPhoto(
		{productId: product.id}
	));
	const photos = await Promise.all(promises);
	const product_with_photos = products_dto.items.map((product) => { 
		const photo_dto = photos.find((photo) => photo.productId == product.id);
		return {
		...product,
		// фото уже найдены. Использую Promise.all
		photoLink: photo_dto!.photoLink,
		expiresAt: photo_dto!.expiresAt,	
	}});
	return { items: product_with_photos, count: products_dto.count};
  }, []);

  useEffect(() => {
	onUpdate(page, pageSize).then((data) => {
		setCount(data.count);
		updateItems(data.items);
	}).catch((e) => console.error(e))
  }, [page, pageSize, onUpdate]);

  return (
    <div className={styles["products-view"]}>
      <form>
        <select
          value={pageSize}
          onChange={(e) => handlePageSizeChange(Number(e.target.value))}
        >
          {PAGE_SIZES.map((s) => (
            <option key={s} value={s}>
              {s} / стр.
            </option>
          ))}
        </select>
		<button type="button" disabled={page === 0} onClick={() => setPage(p => p - 1)}>
          Назад
        </button>
		<span>Стр. {page + 1} из {totalPages}</span>
		<button
          type="button"
          disabled={page >= totalPages - 1}
          onClick={() => setPage(p => p + 1)}
        >
          Вперёд
        </button>
      </form>
	  <ProductList items={items}/>
    </div>
  );
}
