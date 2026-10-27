import getProductPhoto from '../image/get_by_product.req';
import getProductsByPage from '../product/get_by_page.req';

export default async function updateProductItems(page: number, pageSize: number) {
	const products_dto = await getProductsByPage({
	  currentPage: page,
	  pageSize,
	});
	const promises = products_dto.items.map((product) =>
	  getProductPhoto({ productId: product.id }),
	);
	const photos = await Promise.all(promises);
	const product_with_photos = products_dto.items.map((product) => {
	  const photo_dto = photos.find((photo) => photo.productId == product.id);
	  return {
		...product,
		// фото уже найдены. Использую Promise.all
		photoLink: photo_dto!.photoLink,
		expiresAt: photo_dto!.expiresAt,
	  };
	});
	return { items: product_with_photos, count: products_dto.count };
}