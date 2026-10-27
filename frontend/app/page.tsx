import updateProductItems from "./api/utils/updateProductItems";
import ProductsView from "./components/ProductsView";
import { parsePagination } from "./shared/parsePaginationParams";
import { SearchParams } from "./types/searchParams.type";

export default async function Home({
  searchParams,
}: {
  searchParams: Promise<SearchParams>;
}) {
  const { pageSize, currentPage } = await parsePagination(await searchParams);
  const data = await updateProductItems(currentPage, pageSize);

  return (
    <>
      <header>Каталог</header>
      {data.count > 0 && (
        <ProductsView defaultCount={data.count} defaultItems={data.items} />
      )}
      {data.count == 0 && <p>Данных нет. Повторите позже</p>}
    </>
  );
}
