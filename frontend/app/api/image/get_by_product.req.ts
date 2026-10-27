import { API_URL } from '../shared/api_config';
import parseErrorMessage from '../shared/parseErrorMessage';
import RequestError from '../shared/RequestError';
import { ProductPhotoRequest, ProductPhotoResponse } from './get_by_product.schema';

export default async function getProductPhoto(dto: ProductPhotoRequest) : Promise<ProductPhotoResponse> {
	const res = await fetch(`${API_URL}/product/${dto.productId}/image`, {
		method: "GET",
		cache: "no-store",
		
	});
	if (!res.ok) {
		const message = await parseErrorMessage(res);
		throw new RequestError(message, res.status);
	}
	const data = await res.json();
	return {
		productId: data.product_id, 
		photoLink: data.photo_link, 
		expiresAt: data.expires_at
	};
}